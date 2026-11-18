<?php
/**
 * Run the blueprint pricing fixtures and the release's own price-calculation vectors.
 * Usage: php tools/verify-upstream-price-vectors.php /path/to/dolibarr
 */

require __DIR__.'/verify-upstream-pricing.php';

$testFile = dirname(DOL_DOCUMENT_ROOT).'/test/phpunit/PricesTest.php';
$dictionary = DOL_DOCUMENT_ROOT.'/install/mysql/data/llx_c_tva.sql';
foreach ([
    $testFile => '4e1c277907668ffbbd6c09d2e48c017a862e632d36e970afa3f0f809d0a7db63',
    $dictionary => '26602801be84a03ca91b159d3a1ecf38cb5b69c0caef05246b4fcb347bbf2919',
] as $file => $digest) {
    if (!is_file($file) || hash_file('sha256', $file) !== $digest) {
        throw new RuntimeException('Expected Dolibarr 24.0.3 source for '.$file);
    }
}

class CommonClassTest
{
    public $savconf, $savuser, $savlangs, $savdb;
    public $checked = 0;

    public function assertEquals(array $expected, array $actual, string $case): void
    {
        if (array_keys($expected) !== array_keys($actual)) {
            throw new RuntimeException($case.' returned unexpected component keys');
        }
        foreach ($expected as $component => $value) {
            if (!is_numeric($actual[$component]) || (float) $value !== (float) $actual[$component]) {
                throw new RuntimeException($case.' component '.$component.' expected '.$value
                    .' got '.json_encode($actual[$component]));
            }
        }
        ++$this->checked;
    }
}

$user = (object) ['id' => 1];
define('MAIN_DB_PREFIX', '');
$db = new PricingTestDatabase();
$db->store->exec('CREATE TABLE c_tva (
    fk_pays INTEGER, taux REAL, recuperableonly INTEGER, localtax1 TEXT DEFAULT 0,
    localtax1_type INTEGER DEFAULT 0, localtax2 TEXT DEFAULT 0, localtax2_type INTEGER DEFAULT 0,
    note TEXT, active INTEGER, entity INTEGER
)');
// Load the seed rows used by the FR, ES and CI regression vectors.
foreach (file($dictionary) as $statement) {
    if (preg_match("/^insert into llx_c_tva.*values \(\s*(1|4|21),\s*'(10|18)'/i", $statement)) {
        $db->store->exec(str_replace(['llx_c_tva', '__ENTITY__'], ['c_tva', '1'], $statement));
    }
}

// The pinned suite resolves its bootstrap and assertion base relative to its own file.
// Give it an isolated tree with those two services supplied above and the real release libraries.
$work = sys_get_temp_dir().'/dolibarr-price-vectors-'.bin2hex(random_bytes(12));
if (!mkdir($work, 0700)) {
    throw new RuntimeException('Unable to create temporary directory');
}
try {
    foreach (['htdocs', 'test', 'test/phpunit'] as $directory) {
        if (!mkdir($work.'/'.$directory, 0700)) {
            throw new RuntimeException('Unable to create '.$directory);
        }
    }
    foreach (['core', 'compta'] as $directory) {
        if (!symlink(DOL_DOCUMENT_ROOT.'/'.$directory, $work.'/htdocs/'.$directory)) {
            throw new RuntimeException('Unable to expose source directory '.$directory);
        }
    }
    foreach (['htdocs/master.inc.php', 'test/phpunit/CommonClassTest.class.php'] as $path) {
        if (!touch($work.'/'.$path)) {
            throw new RuntimeException('Unable to prepare bootstrap file '.$path);
        }
    }
    if (!copy($testFile, $work.'/test/phpunit/PricesTest.php')) {
        throw new RuntimeException('Unable to stage upstream test');
    }
    require $work.'/test/phpunit/PricesTest.php';
    $suite = new PricesTest();
    if ($suite->testCalculPriceTotal() !== true || $suite->checked !== 14) {
        throw new RuntimeException('Incomplete upstream pricing run: '.$suite->checked.' assertions');
    }
    echo 'PASS PricesTest::testCalculPriceTotal (14 upstream result arrays)'.PHP_EOL;
} finally {
    foreach (['test/phpunit/PricesTest.php', 'test/phpunit/CommonClassTest.class.php',
        'htdocs/master.inc.php', 'htdocs/core', 'htdocs/compta'] as $path) {
        if (is_file($work.'/'.$path) || is_link($work.'/'.$path)) {
            unlink($work.'/'.$path);
        }
    }
    foreach (['/test/phpunit', '/test', '/htdocs', ''] as $path) {
        if (is_dir($work.$path)) {
            rmdir($work.$path);
        }
    }
}
