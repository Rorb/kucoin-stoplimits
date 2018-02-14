import interface
import time

# Bot class, includes various levels of bots which inherit from each other to perform progressively more complex actions

'''
        Level 5 bot - the core Bot class.
        This class sets up a standardized work-loop and lays the framework for other bots to follow 
'''
class Bot(object):
    def __init__(self):
        self._greeting()
        self.looping = True
        self.__main__()

    # Define ultra-generic main loop
    def __main__(self):
        # Initializes child-bots
        self._init_()

        # Performs generic loop actions
        while self.looping: # 'self.looping' is the trigger to exit the loop
            time.sleep(self.SHORT)
            self._loop_()

        self._end_()

    def _greeting(self):
        pass

    def _init_(self):
        pass

    def _loop_(self):
        pass

    def _end_(self):
        pass

    # Class constants
    SHORT = 3
    LONG = 5

    ## Public functions
    # Generic "[Time] Bot: Hey" updating system
    def msg(self, text):
        # Print the message with the time
        timestamp = time.strftime('%I:%M:%S %p')
        botName = self.__class__.__name__
        message = '[%s] %s: %s' % (timestamp, botName, text)
        print message

'''
        Level 3 bot - StopLimit bots
        Class allows users to set stop-orders on KuCoin.

        This is all you'll be getting, sorry!
'''

# Trigger stop-orders
class StopLimitBot(Bot):
    def __init__(self, symbol, callAPI, stop, limit, amount):
        self.symbol = symbol
        self.callAPI = callAPI
        self.stop = float(stop)
        self.amount = float(amount)
        self.limit = float(limit)
        self.on = False

        # Purely for some english interfacing
        if callAPI == interface.buy:
            self.action = 'buy'
        else:
            self.action = 'sell'

        super(StopLimitBot, self).__init__()

    ## Private functions
    def __fulfillOrder(self):
        # Get current price
        self.price = interface.getPrice(self.symbol)
        return ((self.startedLower and self.price >= self.stop) or (self.price <= self.stop and not self.startedLower))

    ## Protected functions
    def _greeting(self):
        self.msg('Hello. Setting a stop-limit-%s order at %s after the price crosses %s.' % (self.action, self.limit, self.stop))

    # The initialization - stuff the bot does when it comes online after greeting the user
    def _init_(self):
        # Determine whether we are triggering BELOW or ABOVE the target
        self.price = interface.getPrice(self.symbol)
        if self.price < self.stop:
            self.startedLower = True
        else:
            self.startedLower = False

    # The logic for every iteration of the bot's loop
    def _loop_(self):
        # Trigger the stop order if necessary
        if self.__fulfillOrder():
            self.looping = False
            return

        # Inform user
        message = 'Awaiting stop ({:.8f}). Price: {:.8f}.'.format(self.stop, self.price)
        self.msg(message)

    # Closing up shop - set the limit order
    def _end_(self):
        message = 'Stop triggered ({:.8f}). Creating a limit-{} order for {:.8f}.'.format(self.price, self.action, self.limit)
        self.msg(message)
        self.callAPI(self.symbol, self.limit, self.amount)