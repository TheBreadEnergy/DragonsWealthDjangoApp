import os
import tinvest as ti
import datetime


class Tinkoff:

    def __init__(self, tinkoff_token):
        self.tinkoff_token = tinkoff_token
        self.client = ti.SyncClient(os.getenv('TINVEST_TOKEN', tinkoff_token))
        portfolio = self.client
        self.pf = portfolio.get_portfolio().payload.positions


    def operations(self):
        print('OPERATIONS')
        dataStart = '2019-08-01T00:00:00.0+03:00'
        # --Парсинг данного времени
        dataFinish = datetime.datetime.now().isoformat()
        dataFinish = dataFinish[0:-7]
        dataFinish = dataFinish + '.0+03:00'
        # dataStart = '2021-01-01T00:00:00.0+03:00'

        prOperat = self.client.get_operations(dataStart, dataFinish)

        # --Запись в операций в файл
        # my_file = open("operations/test.txt", "w+")
        # my_file.seek(0)
        # my_file.write(str(prOperat))
        # my_file.close()

        commissionUSD = 0
        commissionRUB = 0
        marginCommission = 0
        serviceCommissionUSD = 0
        serviceCommissionRUB = 0
        payOutUSD = 0
        payOutRUB = 0
        dividendUSD = 0
        dividendRUB = 0

        for value in range(0, len(prOperat.payload.operations)):
            # print(prOperat.payload.operations[value].operation_type)
            if prOperat.payload.operations[value].operation_type == 'MarginCommission':
                marginCommission += prOperat.payload.operations[value].payment

            if prOperat.payload.operations[value].operation_type == 'ServiceCommission':
                if prOperat.payload.operations[value].currency == 'USD':
                    serviceCommissionUSD += prOperat.payload.operations[value].payment
                else:
                    serviceCommissionRUB += prOperat.payload.operations[value].payment

            if prOperat.payload.operations[value].operation_type == 'PayOut':
                if prOperat.payload.operations[value].currency == 'USD':
                    payOutUSD += prOperat.payload.operations[value].payment
                else:
                    payOutRUB += prOperat.payload.operations[value].payment

            if prOperat.payload.operations[value].operation_type == 'Dividend':
                if prOperat.payload.operations[value].currency == 'USD':
                    dividendUSD += prOperat.payload.operations[value].payment
                else:
                    dividendRUB += prOperat.payload.operations[value].payment

            if prOperat.payload.operations[value].commission != None:
                if prOperat.payload.operations[value].commission.currency == 'USD':
                    commissionUSD += prOperat.payload.operations[value].commission.value
                else:
                    commissionRUB += prOperat.payload.operations[value].commission.value

        marginCommission = round(marginCommission * (-1), 2)
        commissionUSD = round(commissionUSD * (-1), 2)
        commissionRUB = round(commissionRUB * (-1), 2)
        payOutUSD = round(payOutUSD * (-1), 2)
        payOutRUB = round(payOutRUB * (-1), 2)
        dividendUSD = round(dividendUSD, 2)
        dividendRUB = round(dividendRUB, 2)

        operations = {'marginCommission': marginCommission, 'commissionUSD': commissionUSD,
                      'commissionRUB': commissionRUB, 'payOutUSD': payOutUSD, 'payOutRUB': payOutRUB,
                      'dividendUSD': dividendUSD, 'dividendRUB': dividendRUB,
                      'operationsVal': len(prOperat.payload.operations)
                      }

        print(operations)
        print('--end--')
        return operations

    def portfolio_stock(self):
        pf = self.pf
        print('STOCKS')
        portfolio_Stock = {}
        list = []
        a = 0

        for number in range(0, len(pf)):
            if pf[number].instrument_type == 'Stock':
                price = self.client.get_market_orderbook(pf[number].figi, 1).payload.last_price
                priceAll = price * pf[number].balance
                valChange = (price / pf[number].average_position_price.value - 1) * 100
                price = round(price, 2)
                priceAll = round(priceAll, 2)
                valChange = round(valChange, 2)

                portfolio_Stock[a] = {'ticker': pf[number].ticker, 'name': pf[number].name,
                                      'average_position_price': pf[number].average_position_price.value,
                                      'balance': round(pf[number].balance), 'price': price,
                                      'currency': pf[number].average_position_price.currency.value,
                                      'expected_yield': pf[number].expected_yield.value, 'valChange': valChange,
                                      'priceAll': priceAll, 'isin': pf[number].isin, 'figi': pf[number].figi
                                      }
                a += 1

        for number in portfolio_Stock:
            list.append(portfolio_Stock[number])
            print(list[number])

        print('--end--')
        return list

    def portfolio_etf(self):
        pf = self.pf
        print('ETF')
        portfolio_ETF = {}
        a = 0
        list = []

        for number in range(0, len(pf)):
            if pf[number].instrument_type == 'Etf':
                price = self.client.get_market_orderbook(pf[number].figi, 1).payload.last_price
                priceAll = price * pf[number].balance
                valChange = (price / pf[number].average_position_price.value - 1) * 100
                price = round(price, 2)
                priceAll = round(priceAll, 2)
                valChange = round(valChange, 2)

                portfolio_ETF[a] = {'ticker': pf[number].ticker, 'name': pf[number].name,
                                    'average_position_price': pf[number].average_position_price.value,
                                    'balance': round(pf[number].balance), 'price': price,
                                    'currency': pf[number].average_position_price.currency.value,
                                    'expected_yield': pf[number].expected_yield.value, 'valChange': valChange,
                                    'priceAll': priceAll, 'isin': pf[number].isin, 'figi': pf[number].figi
                                    }
                a += 1
                # expected_yield - разница
                # average_position_price.value - средняя цена покупки одного лота

        for number in portfolio_ETF:
            list.append(portfolio_ETF[number])
            print(list[number])
        print('--end--')
        return list

    def portfolio_bond(self):
        pf = self.pf
        print('Bond')
        portfolio_Bond = {}
        a = 0
        list = []

        for number in range(0, len(pf)):
            if pf[number].instrument_type == 'Bond':
                price = self.client.get_market_orderbook(pf[number].figi, 1).payload.last_price
                priceAll = price * pf[number].balance
                valChange = (price / pf[number].average_position_price.value - 1) * 100
                price = round(price, 2)
                priceAll = round(priceAll, 2)
                valChange = round(valChange, 2)

                portfolio_Bond[a] = {'ticker': pf[number].ticker, 'name': pf[number].name,
                                     'average_position_price': pf[number].average_position_price.value,
                                     'balance': round(pf[number].balance), 'price': price,
                                     'currency': pf[number].average_position_price.currency.value,
                                     'expected_yield': pf[number].expected_yield.value, 'valChange': valChange,
                                     'priceAll': priceAll, 'isin': pf[number].isin, 'figi': pf[number].figi
                                     }
                a += 1
                # expected_yield - разница
                # average_position_price.value - средняя цена покупки одного лота

        for number in portfolio_Bond:
            list.append(portfolio_Bond[number])
            print(list[number])
        print('--end--')
        return list

    def portfolio_сurrency(self):
        pf = self.pf
        print('Currency')
        portfolio_Currency = {}
        a = 0
        list = []

        for number in range(0, len(pf)):
            if pf[number].instrument_type == 'Currency':
                price = self.client.get_market_orderbook(pf[number].figi, 1).payload.last_price
                priceAll = price * pf[number].balance
                valChange = (price / pf[number].average_position_price.value - 1) * 100
                price = round(price, 2)
                priceAll = round(priceAll, 2)
                valChange = round(valChange, 2)

                portfolio_Currency[a] = {'ticker': pf[number].ticker, 'name': pf[number].name,
                                         'average_position_price': pf[number].average_position_price.value,
                                         'balance': pf[number].balance, 'price': price,
                                         'currency': pf[number].average_position_price.currency.value,
                                         'expected_yield': pf[number].expected_yield.value, 'valChange': valChange,
                                         'priceAll': priceAll, 'figi': pf[number].figi
                                         }
                a += 1
                # expected_yield - разница
                # average_position_price.value - средняя цена покупки одного лота

        for number in portfolio_Currency:
            list.append(portfolio_Currency[number])
            print(list[number])

        print('--end--')
        return list

    def portfolio_rub(self):
        print('RUB BALANCE')
        pfb = self.client.get_portfolio_currencies().payload.currencies
        a = 0
        for number in pfb:
            if pfb[a].currency.value == 'RUB':
                rub = pfb[a].balance
            a += 1

        rub = round(rub, 2)
        print(rub)
        print('--end--')
        return rub


    def chart(self):
        pf = self.pf

        chart = []

        for number in range(0, len(pf)):
            val = self.client.get_market_orderbook(pf[number].figi, 1).payload.last_price * \
                  pf[number].balance
            if val > 0:
                chart.append(str(pf[number].name))

        return chart

    def chart_size(self):
        pf = self.pf

        price = []
        chart_size = []
        sum = 0

        for number in range(0, len(pf)):
            if pf[number].average_position_price.currency.value != 'USD':
                val = self.client.get_market_orderbook(pf[number].figi, 1).payload.last_price * \
                      pf[number].balance
                val = round(val, 2)
                if val > 0:
                    price.append(val)


            else:
                val = self.client.get_market_orderbook(pf[number].figi,
                                                              1).payload.last_price * self.client.get_market_orderbook(
                    'BBG0013HGFT4', 1).payload.last_price * pf[number].balance
                val = round(val, 2)
                if val > 0:
                    price.append(val)

        for value in range(0, len(price)):
            sum += price[value]

        # print(sum)

        for value in range(0, len(price)):
            chart_size.append(100 * price[value] / sum)
            chart_size[value] = round(chart_size[value], 2)
            # print(chart_size[value])

        return chart_size
