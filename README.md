#  Smoke Test Summary — MarketMate Automation Suite

## Overview
This smoke test suite verifies the most essential user flows of the **MarketMate** application.  
It ensures that critical functionalities such as login, age verification, shipping rules, and rating restrictions work as expected.  
The suite is implemented using **Pytest**, **Selenium WebDriver**, and the **Page Object Model (POM)** design pattern.

---

## 1. Login Test

### Objective
Verify that valid users can log in successfully and the logout option becomes visible.

### Result
| Scenario | Expected Behavior | Actual Behavior | Result |
|-----------|-------------------|-----------------|---------|
| Login with valid credentials | Dashboard is displayed, logout visible | Works as expected | ✅ **Pass** |

### Notes
- Stable across multiple runs.  
- Forms the foundation for subsequent tests.  
- Verified via explicit wait for the logout button element.

---

## 2. Age Verification Test

### Objective
Validate that users must confirm their age before accessing alcohol-related products in the shop.

### Methodology
Tested multiple DOB inputs using **parametrized Pytest** cases.

| Scenario | Expected Message | Actual Behavior | Result |
|-----------|------------------|-----------------|---------|
| Valid adult date | Modal closes, no error toast (or success toast) | Works as expected | ✅ **Pass** |
| Underage date | “You are underage…” warning | Works as expected | ✅ **Pass** |
| Empty / Invalid / Unrealistic DOBs | Validation message displayed | App shows unexpected toasts → known issue | ⚠️ **XFail (App Bug)** |

### Notes
- The system currently shows incorrect toasts for some invalid DOBs (known UI issue).  
- Automated logic and assertions are working correctly.

---

## 3. Rating Restriction Test

### Objective
Ensure that only users who have purchased a product can rate it.

| Scenario | Expected Behavior | Actual Behavior | Result |
|-----------|-------------------|-----------------|---------|
| Attempt to rate without purchase | Rating blocked, restriction message displayed | Works as expected | ✅ **Pass** |

### Notes
- Negative path validated.  
- To be extended with positive flow (rating after purchase).

---

## 4. Shipping Cost Rule (Cart)

### Objective  
Verify the cart’s shipping rule logic:  
- **Free shipping** when *product total ≥ €20*  
- **€5 shipping fee** when *product total < €20*  
- **Grand total = product total + shipping*

### Methodology  
From the **Shop** page, add items to the cart until just below and just above the threshold; read the **Product Total**, **Shipment**, and **Total** values from the checkout summary.

### Result
| Scenario | Product Total | Expected Shipment | Expected Total | Actual | Result |
|---|---:|---:|---:|---|---|
| Below €20 (e.g., €19.xx) | < €20 | €5.00 | Product + €5.00 | Matches | ✅ **Pass** |
| At/Above €20 (e.g., €20.00+) | ≥ €20 | €0.00 | Product | Matches | ✅ **Pass** |

### Notes
- Test navigates via **Shop** (no Add-to-Cart on product detail pages).  
- Handles the **Age Verification Modal** if it appears.  
- Locators are resilient (class-based/XPath with fallbacks).  
- Implemented in: `tests/test_cart.py` using `CartPage` methods.

---

## ⚙️ Technical Summary

| Component | Description |
|------------|-------------|
| **Framework** | Pytest |
| **Automation Tool** | Selenium WebDriver |
| **Design Pattern** | Page Object Model (POM) |
| **Browser** | Google Chrome |
| **Execution Time** | ~35–60 seconds per run |
| **Environment** | Local (macOS, PyCharm) |

---

## Conclusion

- **Core flows validated:** Login, Age Verification, Shipping Rule, and Rating Restriction.  
- **Age Verification:** Adult and underage paths pass; 3 negative validations marked as **xfail** due to known UI issues.  
- **Result Summary:** 3 tests pass outright, 1 (Age Verification) partially passes with known UI bugs.  

> The automation suite is **stable, maintainable, and ready for CI/CD integration.**  
> Minor UI inconsistencies have been logged as known issues.
