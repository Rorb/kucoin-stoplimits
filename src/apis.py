# Direct help with the API
import helpers
import signer

class API(object):
    # Base variables for all APIs
    __host           = 'https://api.kucoin.com%s?%s'    # KuCoin host
    __host_no_params = 'https://api.kucoin.com%s'       # KuCoin host without any ? URL parameters
    _path            = ''                               # This path will be overwritten by every API
    _method          = 'GET'                            # Most APIs use GET, but some use POST
    _payload         = {}                               # APIs' payloads come as dictionaries

    # Call an API generically
    def call(self):
        # Build the URL for the API (they are RESTful)
        kvFormat = '{}={}'
        params = ''

        # Now turn JSON like ``"a":"b"`` into URL parameters like ``a=b``
        if self._payload is not {}:
            params = '&'.join([kvFormat.format(key, str(self._payload[key])) for key in sorted(self._payload.keys())])
            url = self.__host % (self._path, params)
        else:
            url = self.__host_no_params

        # Obtain the request signature
        timestamp = str(int((helpers.time.time() + helpers.timeOffset) * 1000))
        signature = signer.sign(self._path, timestamp, params)

        # Generate the headers, fill with the request signature
        headers = {
            'KC-API-KEY'        : signer.key,
            'KC-API-NONCE'      : timestamp,
            'KC-API-SIGNATURE'  : signature,
            'Content-Type'      : 'application/x-www-form-urlencoded'
        }

        # Pass the actual request off to helpers, since they do error checking and more
        return helpers.request(self._method, url, headers, self)

## Individual APIs
# Get ticker information of a symbol (eg, 'XRB-BTC')
class getTick(API):
    def __init__(self, symbol):
        self._payload = {
            'symbol': symbol
        }

    _path = '/v1/open/tick'

# Create a buy/sell limit order
class transact(API):
    def __init__(self, transaction, symbol, price, amount):
        self._payload = {
            'symbol':   symbol,
            'type':     transaction,
            'amount':   amount,
            'price':    price
        }

    _path = '/v1/order'
    _method = 'POST'