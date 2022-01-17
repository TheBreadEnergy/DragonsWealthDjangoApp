import os
import tinvest as ti
import datetime


class Tinkoff_test:

    def __init__(self, tinkoff_token):
        self.tinkoff_token = tinkoff_token
        self.client = ti.SyncClient(os.getenv('TINVEST_TOKEN', tinkoff_token))
        portfolio = self.client
        self.pf = portfolio.get_portfolio().payload.positions
        Tinkoff_test.main(self)

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

        operations = {'marginCommission': marginCommission, 'commissionUSD': commissionUSD, 'commissionRUB': commissionRUB, 'payOutUSD': payOutUSD, 'payOutRUB': payOutRUB,
                      'dividendUSD': dividendUSD, 'dividendRUB': dividendRUB, 'operationsVal': len(prOperat.payload.operations)
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

    def main(self):

        pf = self.client.get_portfolio().payload.positions  # Получение портфеля(Акции/Облигации/ETF)

        # print(pf)

        portfolio_Stock = Tinkoff_test.portfolio_stock(self)  # Получение Акций
        portfolio_ETF = Tinkoff_test.portfolio_etf(self)  # Получение ETF
        portfolio_Bond = Tinkoff_test.portfolio_bond(self) # Получение Облигаций
        portfolio_Currency = Tinkoff_test.portfolio_сurrency(self) # Получение баланса портфеля
        portfolio_RUB = Tinkoff_test.portfolio_rub(self)
        operations = Tinkoff_test.operations(self)
        # Tinkoff_test.old(self)

    def old(self):

        client = self.client

        pf = client.portfolio.portfolio_get()
        pfb = client.portfolio.portfolio_currencies_get()

        # Получение списка облигаций
        # bonds = client.market.market_bonds_get()

        # Получение списка ETF
        # etfs = client.market.market_etfs_get()

        # Получение списка акций
        # stocks = client.market.market_stocks_get()

        portfolio_sum = 0
        portfolio_usd = 0
        portfolio_rub = 0
        portfolio_change = 0

        average_position_price_All_USD = 0
        average_position_price_All_RUB = 0
        average_position_price_All = 0

        # --Вывод портфеля и стоимости
        for number in range(0, len(pf.payload.positions)):
            print('Тикер:', pf.payload.positions[number].ticker)
            print('Название', pf.payload.positions[number].name)
            val = client.market.market_orderbook_get(pf.payload.positions[number].figi, 1).payload.last_price
            valAll = val * pf.payload.positions[number].balance
            valChange = (val / pf.payload.positions[number].average_position_price.value - 1) * 100
            if pf.payload.positions[number].balance < 0:
                valChange *= -1
                pass
            print('Стоимость одного лота:', val, pf.payload.positions[number].average_position_price.currency)
            print('Средняя цена покупки:', pf.payload.positions[number].average_position_price.value,
                  pf.payload.positions[number].average_position_price.currency)
            if pf.payload.positions[number].figi != 'BBG0013HGFT4':
                print('Количество в портфеле:', round(pf.payload.positions[number].balance))
            else:
                print('Количество в портфеле:', round(pf.payload.positions[number].balance, 2))
                pass
            valAll = round(valAll, 2)
            valChange = round(valChange, 2)
            print('Общая стоимость в портфеле:', valAll, pf.payload.positions[number].average_position_price.currency,
                  ' (',
                  valChange, '% )')
            # print('figi:', pf.payload.positions[number].figi)
            print()

            if str(pf.payload.positions[number].average_position_price.currency) == 'USD':
                portfolio_usd += valAll
            else:
                portfolio_rub += valAll
            pass

            if str(pf.payload.positions[number].average_position_price.currency) == 'USD':
                average_position_price_All_USD += pf.payload.positions[number].average_position_price.value * \
                                                  pf.payload.positions[number].balance
            else:
                average_position_price_All_RUB += pf.payload.positions[number].average_position_price.value * \
                                                  pf.payload.positions[number].balance
            pass

            pass

        # --Баланс рублей
        print('RUB:', pfb.payload.currencies[1].balance, '\n')

        # TODO: проверить корректность работы с положительным балансом руб
        portfolio_sum = portfolio_usd * client.market.market_orderbook_get('BBG0013HGFT4',
                                                                           1).payload.last_price + portfolio_rub + \
                        pfb.payload.currencies[1].balance

        if pfb.payload.currencies[1].balance >= 0:
            average_position_price_All = average_position_price_All_USD * client.market.market_orderbook_get(
                'BBG0013HGFT4',
                1).payload.last_price + average_position_price_All_RUB + \
                                         pfb.payload.currencies[1].balance
            portfolio_change = portfolio_sum - average_position_price_All
        else:
            average_position_price_All = average_position_price_All_USD * client.market.market_orderbook_get(
                'BBG0013HGFT4',
                1).payload.last_price + average_position_price_All_RUB
            portfolio_change = portfolio_sum - average_position_price_All + (-1 * pfb.payload.currencies[1].balance)
            pass

        valChangeAll = ((portfolio_sum - pfb.payload.currencies[1].balance) / average_position_price_All - 1) * 100
        portfolio_change = round(portfolio_change, 2)
        portfolio_sum = round(portfolio_sum, 2)
        valChangeAll = round(valChangeAll, 2)

        # print(str(portfolio_sum)+' рублей ('+str(valChangeAll)+'%)')
        # print()

        dataStart = '2019-08-01T00:00:00.0+03:00'
        # --Парсинг данного времени
        dataFinish = datetime.datetime.now().isoformat()
        dataFinish = dataFinish[0:-7]
        dataFinish = dataFinish + '.0+03:00'

        prOperat = client.operations.operations_get(dataStart, dataFinish)

        # --Запись в операций в файл
        my_file = open("../operations/" + 'test' + ".txt", "w+")
        my_file.seek(0)
        my_file.write(str(prOperat))
        my_file.close()

        print('Кол-во операций:', len(prOperat.payload.operations))
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
                pass
            if prOperat.payload.operations[value].operation_type == 'ServiceCommission':
                if prOperat.payload.operations[value].currency == 'USD':
                    serviceCommissionUSD += prOperat.payload.operations[value].payment
                else:
                    serviceCommissionRUB += prOperat.payload.operations[value].payment
                    pass
                pass

            if prOperat.payload.operations[value].operation_type == 'PayOut':
                if prOperat.payload.operations[value].currency == 'USD':
                    payOutUSD += prOperat.payload.operations[value].payment
                else:
                    payOutRUB += prOperat.payload.operations[value].payment
                    pass
                pass

            if prOperat.payload.operations[value].operation_type == 'Dividend':
                if prOperat.payload.operations[value].currency == 'USD':
                    dividendUSD += prOperat.payload.operations[value].payment
                else:
                    dividendRUB += prOperat.payload.operations[value].payment
                    pass
                pass

            if prOperat.payload.operations[value].commission != None:
                if prOperat.payload.operations[value].commission.currency == 'USD':
                    commissionUSD += prOperat.payload.operations[value].commission.value
                else:
                    commissionRUB += prOperat.payload.operations[value].commission.value
                    pass
            pass
        pass

        marginCommission = round(marginCommission)
        commissionUSD = round(commissionUSD, 2)
        commissionRUB = round(commissionRUB, 2)
        payOutUSD = round(payOutUSD, 2)
        payOutRUB = round(payOutRUB, 2)
        dividendUSD = round(dividendUSD, 2)
        dividendRUB = round(dividendRUB, 2)

        print('Комиссия в долларах:', commissionUSD * -1, '$ по курсу на сейчас:',
              round(commissionUSD * -1 * client.market.market_orderbook_get('BBG0013HGFT4', 1).payload.last_price, 2),
              'руб')
        print('Комиссия в рублях:', commissionRUB * -1, 'руб\n')
        print('Маржинальная комиссия в рублях:', marginCommission * -1, 'руб\n')
        print('Сервисная комиссия в долларах:', serviceCommissionUSD * -1, '$ по курсу на сейчас:',
              round(
                  serviceCommissionUSD * -1 * client.market.market_orderbook_get('BBG0013HGFT4', 1).payload.last_price,
                  2), 'руб')
        print('Сервисная комиссия в рублях:', serviceCommissionRUB * -1, 'руб\n')
        print('Вывод в долларах:', payOutUSD * -1, '$')
        print('Вывод в рублях:', payOutRUB * -1, 'руб\n')
        print('Все дивиденды в доларах:', dividendUSD, '$ по курсу на сейчас:',
              round(dividendUSD * client.market.market_orderbook_get('BBG0013HGFT4', 1).payload.last_price, 2), 'руб')
        print('Все дивиденды в рублях:', dividendRUB, 'руб\n')

        # --Вывод портфеля и стоимости на сайт

        portfolio = []
        portfolio.append('Стоимость портфеля: ' + str(portfolio_sum) + ' рублей')
        portfolio.append('Изменения за всё время: ' + str(portfolio_change) + ' рублей (' + str(valChangeAll) + '%)')
        portfolio.append('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        for number in range(0, len(pf.payload.positions)):
            portfolio.append('Тикер: ' + str(pf.payload.positions[number].ticker))
            portfolio.append('Название: ' + str(pf.payload.positions[number].name))
            val = client.market.market_orderbook_get(pf.payload.positions[number].figi, 1).payload.last_price
            valChange = (val / pf.payload.positions[number].average_position_price.value - 1) * 100
            if pf.payload.positions[number].balance < 0:
                valChange *= -1
                pass
            valChange = round(valChange, 2)
            portfolio.append(
                'Стоимость одного лота: ' + str(val) + ' ' + str(
                    pf.payload.positions[number].average_position_price.currency))
            portfolio.append(
                'Средняя цена покупки: ' + str(pf.payload.positions[number].average_position_price.value) + ' ' + str(
                    pf.payload.positions[number].average_position_price.currency))
            if pf.payload.positions[number].figi != 'BBG0013HGFT4':
                portfolio.append('Количество в портфеле: ' + str(round(pf.payload.positions[number].balance)))
            else:
                portfolio.append('Количество в портфеле: ' + str(round(pf.payload.positions[number].balance, 2)))
                pass

            portfolio.append(
                'Общая стоимость в портфеле: ' + str(round(val * pf.payload.positions[number].balance, 2)) + ' ' + str(
                    pf.payload.positions[number].average_position_price.currency) + ' (' + str(valChange) + '%)')
            portfolio.append('_____________________________________________________')
            pass
        portfolio.append('RUB: ' + str(pfb.payload.currencies[1].balance))

        portfolio.append(
            '""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""')

        portfolio.append('Комиссия в долларах: ' + str(commissionUSD * -1) + ' $ по курсу на сейчас: ' +
                         str(round(commissionUSD * -1 * client.market.market_orderbook_get('BBG0013HGFT4',
                                                                                           1).payload.last_price,
                                   2)) + ' руб')
        portfolio.append('Комиссия в рублях: ' + str(commissionRUB * -1) + ' руб')
        portfolio.append('Маржинальная комиссия в рублях: ' + str(marginCommission * -1) + ' руб')
        portfolio.append(
            'Сервисная комиссия в долларах: ' + str(serviceCommissionUSD * -1) + ' $ по курсу на сейчас: ' +
            str(round(
                serviceCommissionUSD * -1 * client.market.market_orderbook_get('BBG0013HGFT4', 1).payload.last_price,
                2)) + ' руб')
        portfolio.append('Сервисная комиссия в рублях: ' + str(serviceCommissionRUB * -1) + ' руб')
        portfolio.append('Вывод в долларах: ' + str(payOutUSD * -1) + ' $')
        portfolio.append('Вывод в рублях: ' + str(payOutRUB * -1) + ' руб')
        portfolio.append('Все дивиденды в долларах: ' + str(dividendUSD) + ' $ по курсу на сейчас: ' +
                         str(round(
                             dividendUSD * client.market.market_orderbook_get('BBG0013HGFT4', 1).payload.last_price,
                             2)) + ' руб')
        portfolio.append('Все дивиденды в рублях: ' + str(dividendRUB) + ' руб')


token = ''
Hleb = Tinkoff_test(token)
