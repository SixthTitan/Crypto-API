import nicehash
import requests
from datetime import date, timedelta

# For testing purposes use api-test.nicehash.com. Register here: https://test.nicehash.com

# When ready, uncomment line bellow, to run your script on production environment
# host = 'https://api2.nicehash.com'

# How to create key, secret and where to get organisation id please check:

# Production - https://www.nicehash.com
host = 'https://api2.nicehash.com'
organisation_id = ''
key = ''
secret = ''
rig = ''
deviceId = ''

# Withdraw Settings
address = ''
limit = '0.0005'


def setPowerMode(action, op):
    # Create private api object
    private_api = nicehash.private_api(host, organisation_id, key, secret, True)

    current_mode = private_api.get_rig(rig)

    request = private_api.miner_request(rigId=rig, action=action, op_mode=op)
    return request


def withdraw():
    # Create private api object
    private_api = nicehash.private_api(host, organisation_id, key, secret, True)
    public_api = nicehash.public_api(host, True)

    # Get balance for BTC address
    currencies = public_api.get_currencies()
    account = private_api.get_accounts_for_currency(currencies['currencies'][0]['symbol'])
    account_balance = account['totalBalance']

    if account_balance >= limit:
        request = private_api.withdraw_request(address, account_balance, "BTC")
        return print(request)


#    else:
#        return print("You do not have enough funds to withdraw from this account \n" +
#                     "Account Balance:", account_balance)


def myAccountInfo():
    # Create private api object
    private_api = nicehash.private_api(host, organisation_id, key, secret, True)

    # Create public api object
    public_api = nicehash.public_api(host, True)

    # Get balance for BTC address
    rigs = private_api.get_rig(rig)

    # Format the result to a decimal
    daily = rigs['profitability']
    monthly = daily * 30
    yearly = monthly * 12

    # Get balance for BTC address
    currencies = public_api.get_currencies()
    my_account = private_api.get_accounts_for_currency(currencies['currencies'][0]['symbol'])

    # Setup JSON
    result = {
        'rig': {
            'name': rigs['name'],
            'status': rigs['minerStatus'],
            'unpaid': rigs['unpaidAmount']
        },
        'profit': {
            'daily': '{:.10f}'.format(daily),
            'monthly': round(monthly, 10),
            'yearly': round(yearly, 10)
        },
        'balance': my_account['totalBalance']
    }

    return print(result)


def payEstimate():
    # Create private api object
    private_api = nicehash.private_api(host, organisation_id, key, secret, True)

    # Create public api object
    public_api = nicehash.public_api(host, True)

    # Get balance for BTC address
    rigs = private_api.get_rig(rig)

    # Get Today's Date
    today_date = date.today()

    # Format the result to a decimal
    daily = rigs['profitability']
    monthly = daily * 30
    yearly = monthly * 12

    # Estimate the amount of days before we see the next payment
    daysbeforePayment = 0
    total = 0

    # Get balance for BTC address
    currencies = public_api.get_currencies()
    my_account = private_api.get_accounts_for_currency(currencies['currencies'][0]['symbol'])

    # Get the Estimated Pay date and Amount
    while total < float(limit):
        total = total + daily
        daysbeforePayment = daysbeforePayment + 1

    # Set the Pay Date
    payDate = str(today_date + timedelta(daysbeforePayment))

    # Setup JSON
    result = {
        'rig': {
            'name': rigs['name'],
            'status': rigs['minerStatus'],
            'unpaid': rigs['unpaidAmount']
        },
        'profit': {
            'daily': '{:.10f}'.format(daily),
            'monthly': round(monthly, 10),
            'yearly': round(yearly, 10)
        },
        'estimates': {
            'payDate': payDate,
            'daysBeforePayment': daysbeforePayment
        },
        'balance': my_account['totalBalance']
    }

    return print(result)


#setPowerMode('START', 'LOW')
#payEstimate()

