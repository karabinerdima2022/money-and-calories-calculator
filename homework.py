import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment

        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_stats(self, days):
        today = dt.date.today()
        first_day = today - dt.timedelta(days=days)

        total_amount = sum(record.amount for record in self.records
                           if first_day <= record.date <= today)

        return total_amount

    def get_today_stats(self):
        return self.get_stats(days=0)

    def get_week_stats(self):
        return self.get_stats(days=7)


class CashCalculator(Calculator):
    RUB_RATE = 1.0
    USD_RATE = 69.75
    EURO_RATE = 75.81

    def get_today_cash_remained(self, currency='rub'):
        currencies = {
            'rub': ('руб', self.RUB_RATE),
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE)
        }

        if currency not in currencies:
            return 'Данная валюта не поддерживается'

        units, rate = currencies.get(currency)
        balance = self.limit - self.get_today_stats()
        converted_balance = balance / rate
        rounded_balance = round(converted_balance, 2)

        if balance > 0:
            return f'На сегодня осталось {rounded_balance} {units}'
        elif balance == 0:
            return 'Денег нет, держись'
        else:
            return ('Денег нет, держись: твой долг - '
                    f'{abs(rounded_balance)} {units}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        remained_calories = self.limit - self.get_today_stats()

        if remained_calories > 0:
            return ('Сегодня можно съесть что-нибудь ещё,\n'
                    'но с общей калорийностью не более '
                    f'{remained_calories} кКал')

        return 'Хватит есть!'


def main():
    dates = [
        dt.date.today() - dt.timedelta(days=1),
        dt.date.today() - dt.timedelta(days=2),
        dt.date.today() - dt.timedelta(days=3),
        dt.date.today() - dt.timedelta(days=4),
        dt.date.today() - dt.timedelta(days=5),
        dt.date.today() - dt.timedelta(days=6),
        dt.date.today() - dt.timedelta(days=7),
    ]

    cash_comments = {
        'Заказ еды на дом': (580, dates[4].strftime('%d.%m.%Y')),
        'Оплата Интернета': (1200, dates[3].strftime('%d.%m.%Y')),
        'Оплата ЖКХ': (5800, '20.01.2023'),
        'Билеты в театр': (650, dates[1].strftime('%d.%m.%Y')),
        'Оплата проезда': (30, None),
        'Ресторан': (1440, dates[6].strftime('%d.%m.%Y')),
        'Донат любимому блогеру': (555, None),
        'Продукты на неделю': (4855, dates[6].strftime('%d.%m.%Y')),
        'Благотворительность': (1500, dates[3].strftime('%d.%m.%Y')),
        'Вкусняшки для кота': (495, None)
    }

    calories_comments = {
        'Овсяная каша': (312, dates[3].strftime('%d.%m.%Y')),
        'Творог со сметаной': (440, None),
        'Два кусочка торта Прага': (755, '22.01.2023'),
        'Борщ со сметаной': (820, None),
        'Цезарь с курицей': (535, dates[1].strftime('%d.%m.%Y')),
        'Гречневая каша с мясом': (634, '20.01.2023'),
        'Пицца': (798, dates[4].strftime('%d.%m.%Y')),
        'Молочный шоколад': (258, None),
        'Сэндвич с арахисовой пастой': (187, '19.01.2023'),
        'Пирог с картофелем': (272, dates[2].strftime('%d.%m.%Y'))
    }

    cash_calculator = CashCalculator(21000)
    calories_calculator = CaloriesCalculator(14000)

    for cash_comment in cash_comments:
        cash, date = cash_comments.get(cash_comment)
        cash_calculator.add_record(Record(amount=cash,
                                          comment=cash_comment,
                                          date=date))

    for calories_comment in calories_comments:
        calories, date = calories_comments.get(calories_comment)
        calories_calculator.add_record(Record(amount=calories,
                                              comment=calories_comment,
                                              date=date))

    print('\n---------------------------------------------')
    print('Деньги')
    print('---------------------------------------------')
    print(cash_calculator.get_today_cash_remained())
    print(cash_calculator.get_today_cash_remained('usd'))
    print(cash_calculator.get_today_cash_remained('eur'))
    print(cash_calculator.get_today_cash_remained('jpy'))
    print('\nЗа сегодняшний день потрачено'
          f' {cash_calculator.get_today_stats()} руб')
    print('За последние 7 дней потрачено'
          f' {cash_calculator.get_week_stats()} руб\n')

    print('---------------------------------------------')
    print('Калории')
    print('---------------------------------------------')
    print(calories_calculator.get_calories_remained())
    print('\nЗа сегодняшний день набрано'
          f' {calories_calculator.get_today_stats()} кКал')
    print('За последние 7 дней набрано'
          f' {calories_calculator.get_week_stats()} кКал\n')


if __name__ == '__main__':
    main()
