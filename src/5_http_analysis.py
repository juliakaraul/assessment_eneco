import base64
import json
import datetime

# JSON web token here
token = """eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyIsImtpZCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyJ9.eyJhdWQiOiJodHRwczovL0VuZWNvLm9ubWljcm9zb2Z0LmNvbS9lY3Nhei1hcGlnZWUtb2RwLXQiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9lY2EzNjA1NC00OWE5LTQ3MzEtYTQyZi04NDAwNjcwZmMwMjIvIiwiaWF0IjoxNjE2NDE2NzA1LCJuYmYiOjE2MTY0MTY3MDUsImV4cCI6MTYxNjQyMDYwNSwiYWlvIjoiRTJaZ1lFZzNWZG1mNmhzcHYvdVBNYmZmOC9NQ0FBPT0iLCJhcHBpZCI6IjFlMGZiMzU0LWE3OGQtNGY1Yi05OTY2LWVkNjIzYTYyNDU5OSIsImFwcGlkYWNyIjoiMSIsImlkcCI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0L2VjYTM2MDU0LTQ5YTktNDczMS1hNDJmLTg0MDA2NzBmYzAyMi8iLCJvaWQiOiJkYjZlODlmOS1kYjE2LTQyNTItOTQyOS1jNGQ1ZTQ4YWRhYmQiLCJyaCI6IjAuQVFVQVZHQ2o3S2xKTVVla0w0UUFad19BSWxTekR4Nk5wMXRQbVdidFlqcGlSWmtGQUFBLiIsInJvbGVzIjpbIlJlYWRXb29uRW5lcmdpZSIsIlJlYWRFbmVjbyIsIlJlYWRPeHhpbyIsIlJlYWRFbmVjb0J1c2luZXNzIiwiUmVhZEFsbCJdLCJzdWIiOiJkYjZlODlmOS1kYjE2LTQyNTItOTQyOS1jNGQ1ZTQ4YWRhYmQiLCJ0aWQiOiJlY2EzNjA1NC00OWE5LTQ3MzEtYTQyZi04NDAwNjcwZmMwMjIiLCJ1dGkiOiJTZ0JhN1EzS1RVeTNRZjhoek9ZM0FBIiwidmVyIjoiMS4wIn0.AZRHBIxtI9uOT99Q0WRII1wPLKbrcBU-BHmQfUvaCCAnKApOZyrH3kxxtYjejgDTnoPIS0I1NnH0pxNd2ATN_50fcHjsXkCr3DaspJggLS_p2rT2nBMkTDyPBKIzw6rZ9tRrwsuFVXh2cYP1kIgoX-_PxpWfzIsyXctcSzbgYnLOJpiVDiZuz_hi4YWbmvc_lO5iezLLpXvQ0ER034tco9An6LtAGH0mK0-4FHW4McQGLpWPXhwAVLRzNdCXx4TNnOK7eDAVyvxf_fD_lbG9OSmd-PnLbFJKHwWNan06D7hTC8yQa4k-k0gcnHjDYKirG7CfnR5b6dKSst-BCa3X9w"""

# decode base64 encoded token
def decode_base64url(data):
    # Fix padding
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

# split the token
header_b64, payload_b64, signature_b64 = token.split('.')

# decode the header and payload
header_json = decode_base64url(header_b64).decode('utf-8')
payload_json = decode_base64url(payload_b64).decode('utf-8')

print("HEADER:")
print(json.dumps(json.loads(header_json), indent=2))

print("\nPAYLOAD:")
print(json.dumps(json.loads(payload_json), indent=2))


exp = json.loads(payload_json).get("exp")

if exp:
    exp_time = datetime.datetime.fromtimestamp(exp)
    now = datetime.datetime.now()

    print("Expires at (UTC):", exp_time)
    print("Current time (UTC):", now)

    if now > exp_time:
        print("Result: Token is EXPIRED -> probably the reason for the 401 error")
    else:
        print("Result: Token is still valid")
