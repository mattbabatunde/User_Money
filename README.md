## Project Features

**Deposit Functionality**  
Users can securely deposit funds into their account.

**Withdrawal Limit**  
Users can withdraw a **maximum of 300 units** per transaction.

**Transaction Recording**  
All **deposit** and **credit** transactions are automatically recorded for accountability.

**Daily Withdrawal Cap**  
Each user is limited to **six withdrawals per day** to ensure fair usage.









|-----------------------------------------------------------|




##  Personal Note

**For debugging JWT tokens in dependencies:**

###  Algorithm (HS256)
- Defines how the token is **signed and verified** (HMAC using SHA-256).

### Expiration (`exp`)
- Located inside the token payload, it defines **when the token expires**.
- Always use **UTC time** for consistency.
- Printing the algorithm (e.g., `print(token.header['alg'])`) **won’t show expiration issues** — that's tied to the payload.

---

###  Why Print the Payload?

## Using:
- print("DEBUG:: payload:", payload)


### Helps You:

- **Verify Expiration (`exp`)**  
  Ensure the expiration is set correctly and falls within the expected timeframe.

-  **Validate User Data**  
  Confirm that user-specific information (e.g., `email`, `user_id`, etc.) is properly encoded in the token.


