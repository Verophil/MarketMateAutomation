# Age Verification Test Summary (EN)

This automated test validates the behavior of the Age Verification (Age Gate) modal on the shop page.
It checks multiple input cases (valid, underage, empty, invalid format, unrealistic) using Pytest + Selenium and follows the Page Object Model for maintainability.

Two cases pass as expected (adult and underage).
Three are marked as expected failures (xfail) due to known application bugs — validation does not properly handle empty or malformed inputs.

The test is robust, parameterized, and ready for CI/CD integration.