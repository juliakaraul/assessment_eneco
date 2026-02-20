import base64
import json
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# JSON web token here
token = os.getenv("JWT_TOKEN")

# decode base64 encoded token
def decode_base64url(data):
    # Fix padding
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

# split the token
header_b64, payload_b64, signature_b64 = token.split('.')

# decode the header and payload
header = json.loads(decode_base64url(header_b64).decode('utf-8'))
payload = json.loads(decode_base64url(payload_b64).decode('utf-8'))

print("HEADER:")
print(json.dumps(header, indent=2))

print("\nPAYLOAD:")
print(json.dumps(payload, indent=2))

exp_time = datetime.datetime.fromtimestamp(payload['exp'])

if exp_time:
    now = datetime.datetime.now()

    print("Expires at (UTC):", exp_time)
