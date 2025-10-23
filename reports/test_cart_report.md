#  Cart / Shipping Cost Smoke Test

## Overview

This automated test verifies the **shipping cost rule** introduced in the MarketMate Store.  
It ensures that the correct shipping fee is applied based on the cart total:

| Cart Total (€)        | Expected Shipping (€) |
|-----------------------:|----------------------:|
| Less than 20.00        | 5.00                 |
| 20.00 or more          | 0.00 (Free Shipping) |

---

## 🔍 Test Scenario

**Test Name:** `test_shipping_rule_smoke`  
**File:** `tests/test_cart.py`

### Steps:
1. Log in using a valid test account  
2. Navigate to the **Shop** section  
3. Add items to the cart until the total amount is around or above €20  
4. Open the cart  
5. Verify that:
   - The correct shipping fee is displayed
   - `Total = Product Total + Shipment` holds true

---

##  How to Run the Test

Run the following command from your project root:

```bash
pytest tests/test_cart.py --html=reports/cart_test_report.html --self-contained-html -v
