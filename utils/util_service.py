"""
Utils for service layer
"""


def get_ru_month_name(month_int: int) -> str:
    """
    Get month name in russian

    :param month_int: int

    :return: str
    """
    MONTH: list = [
        "Января",
        "Февраля",
        "Марта",
        "Апреля",
        "Мая",
        "Июня",
        "Июля",
        "Августа",
        "Сентября",
        "Октября",
        "Ноября",
        "Декабря",
    ]
    return MONTH[month_int - 1]
