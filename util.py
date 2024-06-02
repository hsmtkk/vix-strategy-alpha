import datetime


def split_first_second(
    first_expiration: datetime.datetime, total: int
) -> tuple[int, int]:
    days_till_first_expiration = (first_expiration - datetime.datetime.now()).days
    first_quantity = days_till_first_expiration // 7
    second_quantity = total - first_quantity
    return (first_quantity, second_quantity)
