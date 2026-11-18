<?php
/**
 * Execute the pinned line calculator and invoice total updater against the blueprint fixtures.
 * Usage: php tools/verify-upstream-pricing.php /path/to/dolibarr
 * Dependencies: PHP CLI with SQLite3, a checkout of Dolibarr 24.0.3.
 */

if (PHP_SAPI !== 'cli' || $argc !== 2 || !extension_loaded('sqlite3')) {
    fwrite(STDERR, "Usage: php (with SQLite3) tools/verify-upstream-pricing.php /path/to/dolibarr\n");
    exit(2);
}
define('DOL_DOCUMENT_ROOT', realpath($argv[1]).'/htdocs');
$files = [
    'core/lib/price.lib.php' => 'cbf0196d78eb5d09b67bca0d9f070fac6f97956e9ea599e2028635d87816d84c',
    'core/lib/functions.lib.php' => 'b88b148fda12377d71b6324b03b11fa97043ef9eba9ef2d890c8a3d05834c1d1',
    'core/class/commonobject.class.php' => '4d3992e132f941910ac86ab74d8141b97176f3b7c4bec6697d4f661762c5159e',
];
foreach ($files as $path => $digest) {
    $file = DOL_DOCUMENT_ROOT.'/'.$path;
    if (!is_file($file) || hash_file('sha256', $file) !== $digest) {
        throw new RuntimeException('Expected Dolibarr 24.0.3 source for '.$path);
    }
}

// Dolibarr normally boots these services through an installed site.
$conf = (object) ['global' => (object) ['MAIN_MAX_DECIMALS_UNIT' => 5], 'entity' => 1];
$hookmanager = new class {
    public function executeHooks(...$args) { return 0; }
};
require_once DOL_DOCUMENT_ROOT.'/core/lib/functions.lib.php';
require_once DOL_DOCUMENT_ROOT.'/core/lib/price.lib.php';
require_once DOL_DOCUMENT_ROOT.'/compta/facture/class/facture.class.php';

class PricingTestDatabase
{
    public $store;

    public function __construct()
    {
        $this->store = new SQLite3(':memory:');
        $this->store->enableExceptions(true);
        $this->store->exec('CREATE TABLE facturedet (
            rowid INTEGER PRIMARY KEY, fk_facture INTEGER DEFAULT 1, qty REAL, subprice REAL,
            remise_percent REAL, tva_tx REAL, total_ht REAL, total_tva REAL, total_ttc REAL,
            localtax1_tx REAL DEFAULT 0, localtax2_tx REAL DEFAULT 0,
            localtax1_type INTEGER DEFAULT 0, localtax2_type INTEGER DEFAULT 0,
            total_localtax1 REAL DEFAULT 0, total_localtax2 REAL DEFAULT 0,
            info_bits INTEGER DEFAULT 0, product_type INTEGER DEFAULT 0, description TEXT,
            situation_percent REAL DEFAULT 100, multicurrency_total_ht REAL,
            multicurrency_total_tva REAL, multicurrency_total_ttc REAL
        )');
    }

    public function prefix() { return ''; }
    public function sanitize($identifier) {
        if (!preg_match('/^[a-z_][a-z0-9_]*$/D', $identifier)) {
            throw new InvalidArgumentException('Unexpected SQL identifier '.$identifier);
        }
        return $identifier;
    }
    public function query($sql) { return $this->store->query($sql); }
    public function begin() { $this->store->exec('BEGIN'); }
    public function commit() { $this->store->exec('COMMIT'); }
    public function rollback() { $this->store->exec('ROLLBACK'); }
    public function free($result) { $result->finalize(); }
    public function fetch_object($result) { return (object) $result->fetchArray(SQLITE3_ASSOC); }
    public function num_rows($result) {
        $rows = 0;
        while ($result->fetchArray(SQLITE3_NUM) !== false) {
            ++$rows;
        }
        $result->reset();
        return $rows;
    }
}

function requireAmounts($case, $actual, $expected, $scale)
{
    $rendered = array_map(static function ($value) use ($scale) {
        return number_format((float) $value, $scale, '.', '');
    }, $actual);
    if ($rendered !== $expected) {
        throw new RuntimeException($case.' got '.json_encode($rendered).' expected '.json_encode($expected));
    }
    echo $case.' '.implode(' / ', $rendered).PHP_EOL;
}

$fixtures = glob(dirname(__DIR__).'/examples/finance/pricing-case--*.valid.json');
if (!$fixtures) {
    throw new RuntimeException('No positive pricing fixtures found');
}
$seller = (object) ['country_id' => 1];
foreach ($fixtures as $file) {
    $case = json_decode(file_get_contents($file), true, 512, JSON_THROW_ON_ERROR);
    $scale = $case['amountScale'];
    $conf->global->MAIN_MAX_DECIMALS_TOT = $scale;
    $db = new PricingTestDatabase();
    $insert = $db->store->prepare('INSERT INTO facturedet
        (qty, subprice, remise_percent, tva_tx, total_ht, total_tva, total_ttc,
         multicurrency_total_ht, multicurrency_total_tva, multicurrency_total_ttc)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)');
    foreach ($case['lines'] as $line) {
        $components = calcul_price_total($line['quantity'], $line['unitPrice'], $line['discountPercent'],
            $line['vatPercent'], 0, 0, 0, $line['basis'] === 'gross' ? 'TTC' : 'HT', 0, 0,
            $seller, [0, 0, 0, 0]);
        $values = [$line['quantity'], $components[3], $line['discountPercent'], $line['vatPercent'],
            $components[0], $components[1], $components[2], $components[16], $components[17], $components[18]];
        foreach ($values as $index => $value) {
            $insert->bindValue($index + 1, (float) $value, SQLITE3_FLOAT);
        }
        $insert->execute()->finalize();
        $insert->reset();
    }

    $invoice = new Facture($db);
    $invoice->id = 1;
    $mode = $case['vatRounding'] === 'perRate' ? '1' : '0';
    // Final argument selects the seller. Flag 1 skips only writing the header row.
    if ($invoice->update_price(0, $mode, 1, $seller) < 1) {
        throw new RuntimeException('Document calculation failed: '.$invoice->error);
    }
    $expected = [$case['expected']['net'], $case['expected']['vat'], $case['expected']['gross']];
    requireAmounts(basename($file), [$invoice->total_ht, $invoice->total_tva, $invoice->total_ttc], $expected, $scale);
    $sum = $db->store->querySingle('SELECT sum(total_ht) AS net, sum(total_tva) AS vat,
        sum(total_ttc) AS gross FROM facturedet', true);
    requireAmounts('stored lines', array_values($sum), $expected, $scale);
}
