import krakenex
import time
from datetime import datetime
k=krakenex.API()
k.load_key('krakenkey.key')
def getTicketInformation(currPair,runAlways):
        while (1==1):
                time.sleep(2)
                try:
                        ticker= k.query_public('Ticker',{'pair':currPair})
                except Exception as e:
                        print "An Error occured while fetching" + currPair + str(e)
                        time.sleep(2)
                ask=float(ticker['result']['XXBTZEUR']['a'][0])
                bid=float(ticker['result']['XXBTZEUR']['b'][0])
                print "Ask:%s || Bid:%s" %(ask,bid)
                if runAlways=='no':
                        return [ask,bid]
def trade(tradetype,leverage):
        coins=raw_input('BTC to %s:' %tradetype)
        limitPrice=raw_input('Limit price:')
        ask=0
        bid=0
#       [ask,bid]==getTicketInformation('XXBTZEUR','no')
#       print "Ask:%s || Bid:%s" %(ask,bid)
        print "%sing crypto for you:" %tradetype
        if not leverage=='0':
                print "here"
                order={'pair': 'XXBTZEUR',
                        'type': tradetype,
                        'ordertype': 'limit',
                        'price': limitPrice,
                        'leverage':leverage,
                        'volume': coins,
                        'trading_agreement' : 'agree'}
        else:
                order={'pair': 'XXBTZEUR',
                        'type': tradetype,
                        'ordertype': 'limit',
                        'price': limitPrice,
                        'volume': coins}

        try:
                print "sending order now:%s" %str(datetime.now())
                result=k.query_private('AddOrder', order)
#                        'close[pair]': 'XXBTZEUR',
#                       'close[type]': 'sell',
#                       'close[ordertype]': 'limit',
#                       'close[price]': '9001',
#                       'close[volume]': '1'})
                print "Received result at:%s" %str(datetime.now())
                print result
        except Exception as e:
                print "Error:" + str(e)
while (1==1):
        task=str(raw_input('Enter b for Buy | s for Sell | t for Ticker information ')).lower()

        if task == 't':
                getTicketInformation('XXBTZEUR','y')

        if task=='b':
                leverage=str(raw_input('Leverage y or n?'))
                if leverage=='y':
                        trade('buy','5')
                else:
                        trade('buy','0')
        if task=='s':
                trade('sell','0')
