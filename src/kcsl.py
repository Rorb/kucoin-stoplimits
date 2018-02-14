'''

        Made for the r/nanotrade community by u/--orb
        Make sure you downloaded it off of https://github.com/Rorb/kucoin-stoplimits for safety
        And check out the readme. --help is also descriptive

        KuCoin APIs are glitchy as heck so gl

'''

import sys, getopt
import bots


# Error out and inform user
# Particularly for errors regarding CLI usage
def error(msg):
    print 'usage error: %s' % msg
    print 'usage error: python kcsl.py --help for more info'
    sys.exit(1)

# Help user in configuring their api-creds.txt file
def configure():
    credFile = bots.interface.apis.signer.credFile

    key = 'None'
    secret = 'None'
    try:
        with open(credFile, 'r') as creds:
            key = creds.readline()[0:4].rstrip('\n') + '...'
            secret = creds.readline()[0:4].rstrip('\n') + '...'
    except:
        pass

    print 'Here, you enter API keys assigned on `https://www.kucoin.com/#/user/setting/api`\n'
    key = raw_input('KuCoin API Key [%s]: ' % key)
    secret = raw_input('KuCoin Secret Key [%s]: ' % secret)

    with open(credFile, 'w') as creds:
        creds.write(key)
        creds.write('\n')
        creds.write(secret)

    print 'Credential file updated. You should be good to go.'
    sys.exit(0)

# Handle -h/--help switch, since it's such a blob of text
def displayHelp():
    print   'usage: python kcsl.py [-hX] [-B|-S] <coin> <stop> <limit> <amount>\n\n' \
            'You can also rearrange the order using the following switches:\n' \
            '-h  --help     : exit normal execution and display this help menu\n' \
            '-X  --configure: enter configuration menu to update KuCoin API keys\n' \
            '-B  --buy      : define the order as a BUY order (-B or -S required)\n' \
            '-S  --sell     : define the order as a SELL order (-B or -S required)\n' \
            '-c  --coin     : the symbol of the coin to initiate the order. (eg. XRB-BTC)\n' \
            '-s  --stop     : the stop-price; reaching this price triggers the limit order\n' \
            '-l  --limit    : the actual buy/sell price after the stop-price is reached\n' \
            '-a  --amount   : the quantity of coin you wish to purchase/sell\n' \
            '\n' \
            'Example 1: `python kcsl.py -S XRB-BTC 0.00099999 0.0009 500`\n' \
            '(same as)\n' \
            'Example 2: `python kcsl.py -a 500 -s 0.00099999 -c XRB-BTC -S -l 0.0009`\n' \
            '\n' \
            'Either of the above will SELL (-S) 500 (-a) XRB into BTC (-c) for a limit\n' \
            'of 90k satoshis (-l) if the price falls under 99.999k (-s) satoshis'
    sys.exit(0)

## Main function; handle args, initiate bots
def main(argv):
    print '\n'
    try:
        options, args = getopt.getopt(argv, 'hBSc:s:l:a:', ['help', 'buy', 'sell', 'coin=', 'stop=', 'limit=', 'amount='])
    except getopt.GetoptError:
        error('invalid option')
        sys.exit(1)

    credFile = bots.interface.apis.signer.credFile
    try:
        open(credFile, 'r')
    except:
        print 'Launch without credential file detected. Routing to `python kcsl.py --configure`.\n'
        configure()

    coin = API = stop = limit = amount = -1
    for opt, arg in options:
        if opt in ['-h', '--help']:
            displayHelp()

        if opt in ['-X', '--configure']:
            configure()

        elif opt in ['-c', '--coin']:
            coin = arg

        elif opt in ['-B', '--buy']:
            if API == bots.interface.sell:
                error('select --buy OR --sell (not both)')
                sys.exit(1)
            API = bots.interface.buy

        elif opt in ['-S', '--sell']:
            if API == bots.interface.buy:
                error('select --buy OR --sell (not both)')
                sys.exit(1)
            API = bots.interface.sell

        elif opt in ['-s', '--stop']:
            stop = arg

        elif opt in ['-l', '--limit']:
            limit = arg

        elif opt in ['-a', '--amount']:
            amount = arg

    if len(args) == 4:
        coin, stop, limit, amount = args

    if API == -1:
        error('transaction type is required (-B or -S)')

    if coin == -1:
        error('coin symbol (-c/--coin) required; make sure you hyphenate (eg. "XRB-BTC")')

    if stop == -1:
        error('stop value (-s/--stop) is required; this is the trigger price to set the limit order')

    if limit == -1:
        error('limit price (-l/--limit) is required; this is your buy/sell price')

    if amount == -1:
        error('amount (-a/--amount) is required; this is the amount you wish to purchase/sell')

    bots.StopLimitBot(coin, API, stop, limit, amount)

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print '\nKeyboardInterrupt: okbye'
        sys.exit(0)