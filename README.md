# Intro

This is a simple bot that will create stop-limit buy and sell orders for you, at the request of some community members on Reddit.
In current state of this fork, this fork fixed a bug which  in helpers.py from original codes at https://github.com/Rorb/kucoin-stoplimits
In future, I might add a GUI interface.

## Warning

For this bot to work, you will need to input your KuCoin API keys into the script. If you did not read the source yourself or you do not trust me, **don't do this**. If this script were configured to steal your KuCoin API keys, I could then use them to **steal all of your funds**.  

If you do trust me, **don't trust any source of this script other than this github** (eg, other githubs, pastebin, etc.). Seriously, I don't want to hear from people how they downloaded this script from pastebin and had their stuff stolen. If you don't trust me or can't verify the script yourself, **don't use this**.  

## Requisites 

python2  
requests.py (`pip install requests`)   

# Installation  

### Linux/Mac Instructions

Anyone using Linux/Mac should know how to use Python and this will be very easy for you.  

`pip install requests`  
`./kcsl.py --help`  or `python kcsl.py --help`


### Windows Instructions

#### From nothing to Python2 (skip if you have Python & Requests)  

##### For somebody who has never used Python before, but understands the basics of windows command line.  

1. Visit https://www.python.org/downloads/ and download Python2 (such as 2.7.14 or newer)  
2. On the third page of the installation, make sure you opt into "Add python.exe to Path." This allows you to run Python from anywhere on your machine simply by typing "python" into the windows commandline, rather than having to navigate to the folder that houses the python.exe file. Image of the option: https://i.imgur.com/o38ycXs.png - make sure it's set to "Will be installed on local hard drive."  
3. After Python is finished installing, open a Windows command line (e.g., windows key + R).  
4. Type `pip install requests` - this allows Python to retrieve a public library that the bot uses to connect to websites.  
5. Your python is now configured!  

#### From Python2 to API keys (skip to step #10 if you've already downloaded the source & have KuCoin API keys)  

##### For somebody who already has Python2.x with the `requests` library, or knows how to do it on their own. This step will assist you in configuring the bot with your KuCoin access keys (so it can place buy&sell orders for you)

6. Download the source code in this repro. The easiest way to do this is to hit the big green "Clone or download" button on the main page, download it as a ZIP file, and unzip it.
7. Visit the following URL: https://www.kucoin.com/#/user/setting/api (and sign into KuCoin obviously)
8. Press the "Create" button. This will create an API Key & a Secret Key. Have those handy.
9. Open a windows command line. Navigate to the /src/ sub-directory where you downloaded the source code (step #6) by using the `cd` command. Example: `cd C:/Users/JohnnyTwoByFour/Desktop/bots/src`
10. Run kcsl.py (`python kcsl.py`). The initial setup will run you through the 'configure' process. Basically, you just copy and paste your Key and Secret Key (obtained in step #8), one at a time, into it. Doing this creates a file names "api-creds.txt" in your /src/ folder, which is how the script knows where to look. Once you're done with this step, you're ready to use the bot!


#### Creating stop-limit orders  

##### Here is the `--help` documentation:

    usage: python kcsl.py [-hX] [-B|-S] <coin> <stop> <limit> <amount>
    
    You can also rearrange the order using the following switches:
    -h  --help     : exit normal execution and display this help menu
    -X  --configure: enter configuration menu to update KuCoin API keys
    -B  --buy      : define the order as a BUY order (-B or -S required)
    -S  --sell     : define the order as a SELL order (-B or -S required)
    -c  --coin     : the symbol of the coin to initiate the order. (eg. XRB-BTC)
    -s  --stop     : the stop-price; reaching this price triggers the limit order
    -l  --limit    : the actual buy/sell price after the stop-price is reached
    -a  --amount   : the quantity of coin you wish to purchase/sell
    
    Example 1: `python kcsl.py -S XRB-BTC 0.00099999 0.0009 500`
    (same as)
    Example 2: `python kcsl.py -a 500 -s 0.00099999 -c XRB-BTC -S -l 0.0009`
    
    Either of the above will SELL (-S) 500 (-a) XRB into BTC (-c) for a limit
    of 90k satoshis (-l) if the price falls under 99.999k (-s) satoshis  
    
If you have no experience with command line, this may look a little overwhelming. I will break it down.  

Typing `python kcsl.py` invokes the Python script. KCSL stands for "KuCoinStopLimit" - I gave it a short name so it'll be easier for you to type. When you invoke the script, you also invoke a bunch of "switches" or "options" afterwards (such as -B or -S), which tell the script what kind of order you want. For example, if you want to make it a sell order, it needs the `-S` or `--sell` switch (there is no functional difference between the 'short names' and the 'long names'. In order to create a stop limit, you will need to provide the script with the following data fields:  

1. Knowledge of whether to buy (-B/--buy) or sell (-S/--sell). This means -B or -S must **always** be present.  
2. The coin (-c/--coin) that the script is looking to buy or sell. An example of this would be XRB-BTC or BTC-USDT. To determine the name of your coin, simply look into the URL of the page. For example, buying on the page `https://www.kucoin.com/#/trade.pro/**XRB-BTC**` is obviously **XRB-BTC** because it's right there in the URL.  
3. The stop price (-s/--stop). This is the price that the script will wait for before triggering. It can be higher or lower than the current price, and your limit order will execute once you cross it. Thus, if you are currently above it, the stop-limit will not trigger until you cross below it. If you are currently below it, the stop-limit will not trigger until you pass above it.  
4. The limit price (-s/--limit). This is the **price you will actually sell for**. Remember that the order-book uses order matching. As a result, if you have a stop-order trigger @ 100k and a sell-limit @ 90k, an order like 99k **will also be sold** (which is good for you!). The limit price sets an effective minimum/maximum you are willing to accept.  
5. The amount (-a/--amount). This is the amount you wish to sell or purchase **denominated in whatever coin appears first in the pairing**. For example, **XRB-BTC** has **XRB** as the first coin of the pair, and thus `-B` indicates you are **buying** XRB and `-a` is the **amount** of XRB you are purchasing. On the other hand, **BTC-USDT** has **BTC** as the first coin of the pair. As a result, `-S` would indicate you are **selling BTC**, and `-B` would indicate you are **purchasing BTC**. If you get confused, just consult the KuCoin sell page.  

Additionally, there is a shorthand variant of the script which will assume the parameters `coin stop limit amount` in that order. An example would be something as simple as:  

    kcsl.py -B BTC-USDT 7800 7950 1.1  

The above example would set a stop-order @ 7800 USDT. If the stop order were triggered (the most recent price crosses 7800), a limit-buy would be set for buying 1.1 BTC for 7950 USD (per BTC), or roughly ~8700 USDT would be spent to purchase 1.1 BTC. If you get used to this short-hand, it will make your life easier. The reason I included the other method (with all the switches) is because it can be easy to forget which number is which, and better to be safe than sorry.  

If you have any questions, you can probably find me on Reddit in r/nanotrade.  

## No feature requests, please.  

Original code forked from https://github.com/Rorb/kucoin-stoplimits and my main purpose of forking it was to fixed a bug in it.

Fork it or do whatever you want with it, but I won't be updating it (aside from maybe adding GUI to it). It's only a small part of a larger bot ecosystem Rorb already forked and trimmed down to give to the (nano) subreddit.
