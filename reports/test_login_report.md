# Login Test Summary

## Test Objective
To verify that valid users can successfully log into the web application using correct credentials.  
This ensures that the authentication flow works correctly and grants access to authorized areas of the site.

## Test Methodology
- Implemented using **Pytest** and **Selenium WebDriver**.  
- The test follows the **Page Object Model (POM)** structure for better maintainability.  
- Fixture `driver` handles browser setup and teardown.  
- Fixture `login_page` abstracts login interactions.  
- Credentials are stored in `utils/constants.py` and imported as test data.  

### Test Scenario:
| Step | Action | Expected Result |
|------|---------|----------------|
| 1 | Navigate to login page | Login form is visible |
| 2 | Enter valid credentials | Form fields accept input |
| 3 | Click “Login” button | Page redirects to home/shop page |
| 4 | Verify presence of “Logout” button | Confirms user is logged in |

## Test Results (latest run)
| Scenario | Expected Behavior | Actual Behavior | Result |
|-----------|-------------------|-----------------|---------|
| Valid login | User should be redirected and “Logout” button visible | Works as expected | **Pass** |

## Known Issues / Defects
None detected during the latest test run.  
Test passed consistently across multiple runs with stable locators and expected timing.

## Conclusion
The login functionality works as expected for valid credentials.  
The test can be extended to include **invalid credential scenarios**, **locked accounts**, and **error message validation** in future iterations.

---

### Short English Summary (for README)
This automated test validates the **Login** functionality using **Pytest + Selenium**.  
It confirms that valid users can sign in successfully and see the “Logout” button after authentication.  

Passed on all recent runs.  
The test is **stable, maintainable, and suitable for CI/CD integration**.
