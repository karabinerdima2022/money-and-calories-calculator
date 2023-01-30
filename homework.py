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
