try:
    import unzip_requirements
except ImportError:
    pass

import nicehash
import requests
import json
import os

from datetime import date, timedelta

# Withdraw Settings
address = ''
limit = '0.0005'


def withdraw(event, context):
    # Production - https://www.nicehash.com
    host = 'https://api2.nicehash.com'
    organisation_id = ''
    key = ''
    secret = ''
    rig = ''

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


def getAccount(event, context):
    # Production - https://www.nicehash.com
    host = 'https://api2.nicehash.com'
    organisation_id = ''
    key = ''
    secret = ''
    rig = ''

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
            'daysBeforePayment': daysbeforePayment,
            'total': total
        },
        'balance': my_account['totalBalance']
    }

    return {
        'statusCode': 200,
        'body': json.dumps(result, indent=4)
    }


def getGecko(event, context):
    symbols = ['shiba-inu', 'bitcoin', 'bitcoin-cash']

    market_data = []

    for data in symbols:
        api_result = requests.get(f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={data}")
        api_response = api_result.json()

        market_data.append(api_response[0])

    return {
        'statusCode': 200,
        'body': json.dumps(market_data, indent=4)
    }


def setPowerMode(action, op):
    # Production - https://www.nicehash.com
    host = 'https://api2.nicehash.com'
    organisation_id = ''
    key = ''
    secret = ''
    rig = ''

    # Create private api object
    private_api = nicehash.private_api(host, organisation_id, key, secret, True)

    current_mode = private_api.get_rig(rig)

    request = private_api.miner_request(rigId=rig, action=action, op_mode=op)
    return request

    # If the PowerMode is not set to Low, change it.
    # if current_mode != 'LOW':
    #    request = private_api.miner_request(rigId=rig, action=action, op_mode=op)
    #    return request
    # else:
    #    return current_mode['rigPowerMode']


def startMiner_week(event, context):
    return setPowerMode('START', 'LOW')


def startMiner_weekend(event, context):
    return setPowerMode('START', 'LOW')


def stopMiner(event, context):
    return setPowerMode('STOP', '')
