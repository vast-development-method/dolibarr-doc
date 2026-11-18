# Pricing verification against Dolibarr 24.0.3

The executable check uses the release's unmodified line calculator, decimal helper and invoice total updater. For each positive pricing fixture it inserts the calculated components in a temporary SQLite table, runs the upstream invoice aggregation, and asserts both the returned totals and the sum of the persisted lines. The test adapter supplies a disabled hook dispatcher and the database methods used by this operation. It skips writing the invoice header. The header values reported here are the upstream invoice object's calculated totals.

Run from the blueprint repository root with Git, PHP CLI, SQLite3 and a writable temporary directory that supports symbolic links. These commands verify the release commit, run the four blueprint fixtures, then execute the 14 upstream regression vectors.

```sh
set -e
checkout=$(mktemp -d)
git clone --quiet --depth 1 --branch 24.0.3 https://github.com/Dolibarr/dolibarr.git "$checkout/dolibarr"
test "$(git -C "$checkout/dolibarr" rev-parse HEAD)" = 5c6c7ff6a5112413b1c27221c8d11750afad56f8
php tools/verify-upstream-price-vectors.php "$checkout/dolibarr"
```

The driver verifies the SHA-256 digests of the pinned pricing implementation, the complete upstream test file and its tax dictionary. It reads test inputs and expected arrays directly from that release. A source or amount mismatch exits nonzero. The final success line is `PASS PricesTest::testCalculPriceTotal (14 upstream result arrays)`. To run just the four blueprint fixtures, use `php tools/verify-upstream-pricing.php "$checkout/dolibarr"`. [Regression driver](../../tools/verify-upstream-price-vectors.php) · [Fixture harness](../../tools/verify-upstream-pricing.php) · [Calculator][price] · [Document updater][update]

| Executed fixture | Net | VAT | Gross | Retained line totals |
| --- | ---: | ---: | ---: | --- |
| 3 × 20.00 net, 10% discount, 15% VAT | 54.00 | 8.10 | 62.10 | Match |
| Two lines of 0.03 net, 20% VAT, per-line rounding | 0.06 | 0.02 | 0.08 | Match |
| Same inputs, per-rate rounding | 0.06 | 0.01 | 0.07 | Match |
| 2 × 11.50 including 15% VAT | 20.00 | 3.00 | 23.00 | Match |

On 18 November 2026 all four fixtures and all 14 upstream result arrays passed under PHP 8.5.12 CLI (WebAssembly build) and in-memory SQLite. The upstream vectors include negative prices, currency conversion and local taxes on goods and services. The driver stages the unmodified `PricesTest.php` in a temporary directory and runs its `testCalculPriceTotal` method against the release libraries. It supplies the test method with the release's relevant French, Spanish and Ivorian tax dictionary rows and checks the keys and numerical values of every result component. Running the complete upstream suite through PHPUnit requires the application/test-database setup. [Upstream test vectors][official] · [Tax dictionary][tax]

This execution covers arithmetic and the updater's database operations on invoice lines. Full invoice submission, bank and payment operations, real extension hooks and complete MariaDB/PostgreSQL transactions require a running ERP instance. Their chapter acceptance scenarios remain source-traced specifications.

[price]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/lib/price.lib.php#L90-L473
[update]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/class/commonobject.class.php#L4079-L4417
[official]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/test/phpunit/PricesTest.php#L68-L233
[tax]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/install/mysql/data/llx_c_tva.sql
