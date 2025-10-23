# Rating Test Summary

## Test Objective
To verify that users **can only rate a product after purchasing it**.  
This ensures that the rating feature maintains credibility by restricting reviews to verified buyers.

## Test Methodology
- Automated with **Pytest** and **Selenium WebDriver**.  
- Implemented following the **Page Object Model (POM)** pattern for clean structure.  
- The test simulates the user flow:
  1. Logging in with valid credentials.
  2. Navigating to a product page.
  3. Attempting to submit a rating without prior purchase.
- The system’s behavior is validated by checking for the correct warning or restriction message.

### Test Scenario:
| Step | Action | Expected Result |
|------|---------|----------------|
| 1 | Log in as a valid user | User is authenticated |
| 2 | Navigate to a product detail page | Product info is displayed |
| 3 | Try to submit a rating without purchase | System displays a message restricting rating access |

## Test Results (latest run)
| Scenario | Expected Behavior | Actual Behavior | Result |
|-----------|-------------------|-----------------|---------|
| Submit rating without purchase | Rating should be rejected, message displayed | Works as expected |  **Pass** |

## Known Issues / Defects
No issues detected during the latest run.  
Toast message and restrictions behaved as designed.

## Conclusion
The rating restriction works correctly — users cannot rate products they haven’t purchased.  
This test can be extended to include:
- Rating **after** purchase (positive path)
- UI validation of the **star rating component**
- Edge cases like multiple ratings from the same user.
