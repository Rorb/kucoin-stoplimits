import hashlib
import hmac
import base64

# Keys are stored in an api-creds.txt file
# These are all in outer scope because several are referenced cross-file
credFile = 'api-creds.txt'
try:
    with open(credFile) as creds:
        key = creds.readline().rstrip('\n')
        secret = creds.readline().rstrip('\n')
except:
    pass

# Generates signature for KuCoin's signing authentication
stsFormat = '%s/%s/%s'
def sign(path, timestamp, params):
    stringToSign = stsFormat % (path, timestamp, params)
    b64StringToSign = base64.b64encode(stringToSign)
    signature = hmac.new(secret, b64StringToSign, hashlib.sha256).hexdigest()
    return signature