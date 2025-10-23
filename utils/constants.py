# utils/constants.py
BASE_URL = "https://grocerymate.masterschool.com"
STORE_URL = f"{BASE_URL}/store"
LOGIN_URL = f"{BASE_URL}/auth"

# Product detail URLs (non-alcoholic/alcoholic)
ALCOHOL_PRODUCT_URL = f"{BASE_URL}/product/66b3a57b3fd5048eacb47a7b"
NON_ALCOHOL_PRODUCT_URL = f"{BASE_URL}/product/66b3a57b3fd5048eacb479a6"


FREE_SHIPPING_THRESHOLD = 20.00
SHIPPING_FEE = 5.00

#  Nimm hier deine gültigen Test-Creds
VALID_USER = {
    "email": "sisko@mail.com",
    "password": "DeepSpace9",
}

INVALID_USER = {
    "email": "invaliduser@example.com",
    "password": "wrongpass",
}

# Messages (an dein UI angepasst)
ERROR_INVALID_LOGIN = "Invalid username or password"