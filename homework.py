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
            return ('Денег нет, держись: твой долг -'
                    f' {abs(rounded_balance)} {units}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        remained_calories = self.limit - self.get_today_stats()

        if remained_calories > 0:
            return ('Сегодня можно съесть что-нибудь ещё,\n'
                    'но с общей калорийностью не более'
                    f' {remained_calories} кКал')
        else:
            return 'Хватит есть!'
