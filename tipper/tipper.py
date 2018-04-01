import requests
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

rpc_username = 'bitcoinwspectrumrpc'
rpc_password = 'fi2WNfpBZA2ajiw2qrRcps1BkazgRuVMu3Z1iNgAdNaj'
rpc_ip = '127.0.0.1'
rpc_port = 46646

con = AuthServiceProxy('http://%s:%s@%s:%i'%(rpc_username, rpc_password, rpc_ip, rpc_port))
api = requests.get('https://www.southxchange.com/api/price/BWS/BTC')

#Tip commands
def validateAddress(address):
    validate = con.validateaddress(address)
    return validate['isvalid']

def getAddress(account):
    return con.getaccountaddress(account)

def getBalance(account,minconf=1):
    return con.getbalance(account,minconf)

def withdraw(account,destination,amount):
    if amount > getBalance(account) or amount <= 0:
        raise ValueError("Invalid amount.")
    else:
        return con.sendfrom(account,destination,amount)

def tip(account,destination,amount):
    if amount > getBalance(account) or amount <= 0:
        raise ValueError("Invalid amount.")
    else:
        con.move(account,destination,amount)

def rain(account,amount):
    if amount > getBalance(account) or amount <= 0:
        raise ValueError("Invalid amount.")
    else:
        accounts = con.listaccounts()
        eachTip = amount / len(accounts)
        for ac in accounts:
            tip(account,ac,eachTip)
        return eachTip

#API commands
def getPrice(amount=1,full=0,satoshi=0,refresh=0):
    r = api.json()[0]
    price = float(r['price_usd'])
    price_btc = float(r['price_btc'])

    if refresh:
        global api
        api = requests.get('https://www.southxchange.com/api/price/BWS/BTC')
        r = api.json()[0]
        price = float(r['price_usd'])
        price_btc = float(r['price_btc'])
    if satoshi:
        return float("%.8f"%(price_btc*amount))
    elif full:
	return price*amount
    else:
        return float("%.2f"%(price*amount))
