import krakenex
import time
from datetime import datetime
k=krakenex.API()
#change the path to your krakenkey file. 
k.load_key('kraken.key')
pripub={'Time':'pub','Assets':'pub','AssetPairs':'pub','Ticker':'pub','OHLC':'pub','Depth':'pub','Trades':'pub','Spread':'pub','Balance':'pri','TradeBalance':'pri','OpenOrders':'pri','ClosedOrders':'pri','QueryOrders':'pri','TradesHistory':'pri','QueryTrades':'pri','OpenPositions':'pri','Ledgers':'pri','QueryLedgers':'pri','TradeVolume':'pri','AddOrder':'pri','CancelOrder':'pri',}
def callFunction(funName):
        if pripub[funName]=='pri':
                try:
                        result=k.query_private(funName)
                except Exception as e:
                        print "An Error occured while calling %s" +  str(e) %funName
                        return '0'
        else:
                try:
                        result=k.query_public(funName)

                except Exception as e:
                        print "An Error occured while calling %s" +  str(e) %funName
        return result
def getAccountBalance():
        result=callFunction('Balance')
        if not result=='0':
                print 'EUR:',result['result']['ZEUR'],'\nXBT',result['result']['XXBT'],'\nETH:',result['result']['XETH']
def getOpenOrders():
        result=callFunction('OpenOrders')
        openOrders=result['result']['open']
        orderlist=[]
        i=0
        for refid, value in openOrders.iteritems() :
                orderlist.append(refid)
                i+=1
                print i,'. Open:',refid, value['descr']['order'], 'Vol Rem', float(value['vol'])-float(value['vol_exec'])
        if not len(orderlist)>0:
                print "No open orders! Create some"
                return
        while(1==1):
                inp=raw_input('Cancel? Enter number or all to cancel all orders, q quit:')
                if inp=='q':
                        break
                elif inp=='all':
                        for txid in orderlist:
                                cancelOpenOrder(txid)
                elif inp.isdigit():
                        cancelOpenOrder(orderlist[int(inp)-1])
                else:
                        print "Invalid selection:"
def getOpenPositions():
        try:
                result=k.query_private('OpenPositions')
                volume=0.0000
                cost=0.0000
                for refid, value in result['result'].iteritems() :
                        volume+=float(value['vol'])
                        cost+=float(value['cost'])
                if not volume==0.00:
                        print 'Volume:',volume, '@', cost/volume
                else:
                        print "No open position."

        except Exception as e:
                print "An Error occured while fetching orders" +  str(e)

def cancelOpenOrder(txid):
        try:
                result=k.query_private('CancelOrder',{'txid':txid})
                print result
        except Exception as e:
                print "An Error occured while cancelling order" +  str(e)
def getTicketInformation(currPair,runAlways):
        while (1==1):
                time.sleep(2)
                try:
                        ticker= k.query_public('Ticker',{'pair':currPair})
                        print ticker
                except Exception as e:
                        print "An Error occured while fetching" + currPair + str(e)
                        time.sleep(2)
                ask=float(ticker['result']['XXBTZEUR']['a'][0])
                bid=float(ticker['result']['XXBTZEUR']['b'][0])
                print "Ask:%s || Bid:%s" %(ask,bid)
                if runAlways=='no':
                        return [ask,bid]
def trade(tradetype,leverage,coins):
        #coins=raw_input('BTC to %s:' %tradetype)
        if not leverage=='5m':
                limitPrice=raw_input('Limit price:')
                if float(limitPrice)<1000.000 or float(limitPrice)>1300.000:
                        print "Probably wrong selection!"
                        return
                coins=raw_input('BTC to %s:' %tradetype)
        ask=0
        bid=0
#       [ask,bid]==getTicketInformation('XXBTZEUR','no')
#       print "Ask:%s || Bid:%s" %(ask,bid)
        print "%sing crypto for you:" %tradetype
        if leverage=='5':
                order={'pair': 'XXBTZEUR',
                        'type': tradetype,
                        'ordertype': 'limit',
                        'price': limitPrice,
                        'leverage':leverage,
                        'volume': coins,
                        'trading_agreement' : 'agree'}
        elif leverage=='5m':
                leverage=5
                order={'pair': 'XXBTZEUR',
                        'type': tradetype,
                        'ordertype': 'market',
                        'leverage':leverage,
                        'volume': coins,
                        'trading_agreement' : 'agree'}

        elif leverage=='0':
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
        task=str(raw_input('b=buy,s=sell,bl=buy lev, sl=sell lev, oo=open orders, op=open positions,c=cancel,bal=balance ')).lower()
#Input:xy1234.000
#x=b or s. b for buy. s for sell
#y=l or m. L for limit , m for market

        if task == 't':
                getTicketInformation('XXBTZEUR','y')

        if task=='b':
                trade('buy','0','0')
        if task=='bl':
                trade('buy','5','0')
        if task=='s':
                trade('sell','0','0')
        if task=='sl':
                trade('sell','5','0')
        if task=='oo': #query open orders
                getOpenOrders()
        if task=='op': #query open positions
                getOpenPositions()
        if task=='c': #to cancel open orders
                cancelOpenOrder()
        if task=='bal': #get asset info
                getAccountBalance()
        if task=='q':
                exit()
