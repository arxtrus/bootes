from __future__ import annotations

import datetime as dt
from importlib import metadata
from typing import TYPE_CHECKING, overload

from zoneinfo import ZoneInfo, available_timezones

import tzlocal
from dateutil.relativedelta import relativedelta

if TYPE_CHECKING:
	from zoneinfo import ZoneInfo

utc = ZoneInfo("UTC")

def is_localized(value: dt.datetime) -> bool:
	"""
	Determine if a datetime is timezone-aware.
	"""
	return value.tzinfo is not None

def is_native(value: dt.datetime) -> bool:
	"""
	Determine if a datetime is naive (not timezone-aware).
	"""
	return value.tzinfo is None

def utcnow() -> dt.datetime:
	"""
	Get the current UTC time as a timezone-aware datetime.
	"""
	return dt.datetime.now(tz=utc)

@overload
def convert_to_utc(value: None) -> None: ...

@overload
def convert_to_utc(value: dt.datetime) -> dt.datetime: ...

def convert_to_utc(value: dt.datetime | None) -> dt.datetime | None:
	"""
	Convert a datetime to UTC timezone.

	If the input is None, it returns None.
	If the input is naive, it assumes it's in UTC and makes it timezone-aware.
	If the input is already timezone-aware, it converts it to UTC.
	"""
	if value is None:
		return None

	if not is_localized(value):
		# from orbis.settings import TIMEZONE
		# value = make_aware(value, TIMEZONE)
		value = make_aware(value, "UTC")

	return value.astimezone(utc)

@overload
def make_aware(value: None, tz: dt.tzinfo | str | None = None) -> None: ...

@overload
def make_aware(value: dt.datetime, tz: dt.tzinfo | str | None = None) -> dt.datetime: ...

def make_aware(value: dt.datetime | None, tz: dt.tzinfo | str | None = None) -> dt.datetime | None:
	"""
	Make a naive datetime timezone-aware.

	If the input is None, it returns None.
	If the input is already timezone-aware, it returns it as is.
	If the input is naive, it assigns the specified timezone (or local timezone if none specified).
	"""
	if value is None:
		return None

	if is_localized(value):
		return value

	if tz is None:
		# from orbis.settings import TIMEZONE
		# tz = TIMEZONE
		tz = tzlocal.get_localzone_name()
 
	if isinstance(tz, str):
		tz = ZoneInfo(tz)

	return value.replace(tzinfo=tz)

def make_naive(value: dt.datetime, tz: dt.tzinfo | None = None) -> dt.datetime | None:
	if tz is None:
		# from orbis.settings import TIMEZONE
		# tz = TIMEZONE
		tz = tzlocal.get_localzone()

	if is_native(value):
		raise ValueError("make_naive() expects a timezone-aware datetime")
	
	return value.astimezone(tz).replace(tzinfo=None)


def datetime(*args, **kwargs) -> dt.datetime:
	if "tzinfo" not in kwargs:
		# from orbis.settings import TIMEZONE
		# kwargs["tzinfo"] = TIMEZONE
		kwargs["tzinfo"] = tzlocal.get_localzone_name()

	return dt.datetime(*args, **kwargs)


def parse_timezone(name: str | int) -> ZoneInfo:
    """
    Return a ZoneInfo object from IANA timezone name.
    """
    if isinstance(name, int):
        raise NotImplementedError(
            "Integer offsets not supported with zoneinfo")
    if name in available_timezones():
        return ZoneInfo(name)
    raise ValueError(f"Unknown timezone: {name}")


def local_timezone() -> ZoneInfo:
    """
    Return local timezone.
    """
    return tzlocal.get_localzone()


def from_timestamp(timestamp: int | float, tz: str | ZoneInfo = utc) -> dt.datetime:
    if isinstance(tz, str):
        tz = parse_timezone(tz)
    return dt.datetime.fromtimestamp(timestamp, tz)
