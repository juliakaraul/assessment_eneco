# Exercise 5: HTTP API Integration - JWT Troubleshooting

## Question 1: What could this snippet represent and how is it typically used?

**Answer:** This snippet is a **JWT (JSON Web Token)** - a standard for secure API authentication.

### What is it?
- **Format:** Three Base64-encoded parts separated by dots: `header.payload.signature`
- **Algorithm:** RS256 (RSA Signature with SHA-256) 
- **Purpose:** Authentication token for API requests

### How is it used?
The token is sent in the HTTP `Authorization` header of API requests:
```http
GET /api/endpoint HTTP/1.1
Host: api.eneco.com
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGci...
```

The API server:
1. Validates the signature using Azure AD's public key
2. Checks the token hasn't expired (`exp` claim)
3. Verifies the audience (`aud`) matches the API
4. Extracts user roles/permissions from the `roles` claim
5. Grants or denies access based on these checks

### Token Details (from decoded payload):
- **Issued:** March 22, 2021 13:45:05 UTC
- **Expires:** March 22, 2021 14:43:25 UTC (1 hour lifespan)
- **Audience:** `https://Eneco.onmicrosoft.com/ecsaz-apigee-odp-t`
- **Roles:** ReadWoonEnergie, ReadEneco, ReadOxxio, ReadEnecoBusiness, ReadAll
- **Azure AD Tenant:** eca36054-49a9-4731-a42f-8400670fc022

---

## Question 2: Steps to analyze Bob's issue before responding

### Step 1: Decode and Inspect the JWT Token

Decode the Base64-encoded header and payload (see `src/5_http_analysis.py`):
```python
import base64
import json
import datetime

def decode_base64url(data):
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

header_b64, payload_b64, signature = token.split('.')
payload = json.loads(decode_base64url(payload_b64).decode('utf-8'))

exp_time = datetime.datetime.fromtimestamp(payload['exp'])
print(f"Token expires: {exp_time}")
```

**Finding:** Token expired on March 22, 2021 at 14:43:25 UTC

### Step 2: Compare Timeline

- **Bob's email:** March 23, 2021 10:21:58 AM CET
- **Token expiration:** March 22, 2021 14:43:25 UTC (15:43:25 CET)
- **Time difference:** ~19 hours after expiration

**Conclusion:** Bob is using yesterday's demo token, which expired overnight.

### Step 3: Verify Token Claims Match API Requirements

Check the decoded payload for:
- **Audience (`aud`):** `https://Eneco.onmicrosoft.com/ecsaz-apigee-odp-t`
- **Issuer (`iss`):** Azure AD tenant eca36054...
- **Roles:** ReadAll, ReadEneco, ReadWoonEnergie, ReadOxxio, ReadEnecoBusiness

**Finding:** All claims are valid - expiration is the only issue.

### Step 4: Check for Other Potential Issues

- **Clock skew:** APIs typically allow 5 minutes tolerance - this token is 19 hours expired, well beyond that
- **nbf (not before):** 1616416705 - token was valid to use when issued
- **Signature validation:** RS256 algorithm requires Azure AD public key - likely configured correctly since it worked yesterday

**Finding:** No other issues detected - expiration is the root cause.

### Step 5: Reproduce the Issue
```bash
# Test with the expired token
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGci..." \
     https://api.eneco.com/endpoint

# Expected: 401 Unauthorized (due to expiration)
```

---

## Root Cause Analysis

**Problem:** Token expired 19 hours before Bob's API call

**Impact:** All API calls return 401 Unauthorized

**Evidence:** Server logs show 401 responses with the expired token in the Authorization header

---

## Response to Bob

**Subject:** RE: Your API is broken!

Hi Bob,

Good news - the API isn't broken! I found the issue in the logs.

**The problem:** Your access token expired yesterday at 14:43 UTC. JWT tokens have a short lifespan (1 hour) for security reasons.

**The solution:** You need to request a new token before making API calls. Here's how:
```python
import msal

# Configure the Azure AD client
app = msal.ConfidentialClientApplication(
    client_id="1e0fb354-a78d-4f5b-9966-ed623a624599",
    client_credential="",
    authority="https://login.microsoftonline.com/eca36054-49a9-4731-a42f-8400670fc022"
)

# Get a fresh token
result = app.acquire_token_for_client(
    scopes=["https://Eneco.onmicrosoft.com/ecsaz-apigee-odp-t/.default"]
)

if "access_token" in result:
    token = result["access_token"]
    # Use this token in your API calls
else:
    print("Error:", result.get("error_description"))
```

**Best practice:** Implement token refresh logic - when you get a 401, automatically request a new token and retry.

Let me know if you need help setting this up!

Best,  
Julia

---

## Implementation

**Script:** `src/5_http_analysis.py`

**Approach:**
1. Split JWT into header, payload, signature
2. Base64-decode header and payload (with proper padding)
3. Parse JSON and extract expiration timestamp
4. Compare expiration time with current time

**Output:**
```
HEADER:
{
  "typ": "JWT",
  "alg": "RS256",
  "x5t": "nOo3ZDrODXEK1jKWhXslHR_KXEg",
  "kid": "nOo3ZDrODXEK1jKWhXslHR_KXEg"
}

PAYLOAD:
{
  "aud": "https://Eneco.onmicrosoft.com/ecsaz-apigee-odp-t",
  "iss": "https://sts.windows.net/eca36054-49a9-4731-a42f-8400670fc022/",
  "iat": 1616416705,
  "nbf": 1616416705,
  "exp": 1616420605,
  "roles": ["ReadWoonEnergie", "ReadEneco", "ReadOxxio", "ReadEnecoBusiness", "ReadAll"],
  ...
}

Expires at (UTC): 2021-03-22 14:43:25
Current time (UTC): 2026-02-12 11:11:30
Result: Token is EXPIRED -> probably the reason for the 401 error
```

**Conclusion:** Bob's token expired ~19 hours before his API call. He needs to request a fresh token from Azure AD.