from datetime import datetime


def datetime_extract_part(origin: str, origin_format: str, extract_format: str) -> str:
    origin_datetime = datetime.strptime(origin, origin_format)
    return origin_datetime.strftime(extract_format)


def datetime_now(what_format) -> str:
    now = datetime.now()
    return now.strftime(what_format)
