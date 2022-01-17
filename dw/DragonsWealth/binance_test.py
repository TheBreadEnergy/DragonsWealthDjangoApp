from binance.spot import Spot
import datetime

api_key = 'CtHXx9nBoWxWFmHQGlGIIuZejKgRs0ynCifVOU68aMXR2PodkjsYWsiKpbhU1r7K'
api_secret = 'M3Km39vKvlLMxzLcSEXQr6zrFg4h0U2Zo1BCixma7i5QDosSB8bNtvqH8vQ6QoFC'


def main():
    client = Spot(api_key, api_secret)
    a = client.account_snapshot("SPOT")['snapshotVos'][0]['data']
    timestamp = 1339521878.04
    time_a = client.account_snapshot("SPOT")['snapshotVos'][0]['updateTime']
    # print(time_a)
    # value = datetime.datetime.fromtimestamp(int(time_a))
    # print(value.strftime('%Y-%m-%d %H:%M:%S'))
    totalAssetOfBtc = a['totalAssetOfBtc']
    print('totalAssetOfBtc = ' + totalAssetOfBtc + ' BTC')
    for number in range(0, len(a['balances'])):
        if a['balances'][number]['free'] != '0':
            print(a['balances'][number]['asset'] + ' : ' + a['balances'][number]['free'])


if __name__ == "__main__":
    main()
