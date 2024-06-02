import datetime


def parse_date(date: str) -> datetime.datetime:
    parsed = datetime.datetime.strptime(date, "%Y%m%d")
    return parsed


def format_date(date: datetime.datetime) -> str:
    return date.strftime("%Y/%m/%d")
