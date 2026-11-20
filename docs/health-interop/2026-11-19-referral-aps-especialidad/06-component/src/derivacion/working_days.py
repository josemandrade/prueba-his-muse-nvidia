"""Días hábiles (lunes a viernes) para los plazos SLA.

La guía define los plazos en días hábiles y no define un calendario
de festivos: el componente no modela festivos (Ruling en `state.md`).
Los plazos vencen a las 17:00 hora local, como el ejemplo compilado
(`2026-11-26T17:00:00-03:00`).
"""

from datetime import date, datetime, time, timedelta, timezone

SANTIAGO = timezone(timedelta(hours=-3))
DEADLINE_HOUR = 17


def is_working_day(day):
    """True si el día es lunes a viernes."""
    return day.weekday() < 5


def add_working_days(start, n):
    """Suma `n` días hábiles a `start` (el día inicial no cuenta)."""
    day = start
    remaining = n
    while remaining > 0:
        day += timedelta(days=1)
        if is_working_day(day):
            remaining -= 1
    return day


def deadline_at(day, hour=DEADLINE_HOUR):
    """El vencimiento de un plazo en ese día, a las 17:00 (-03:00)."""
    return datetime.combine(day, time(hour, 0), tzinfo=SANTIAGO)


def deadline_after(start_dt, n, hour=DEADLINE_HOUR):
    """`n` días hábiles después de `start_dt`, a las `hour` en punto."""
    return deadline_at(add_working_days(start_dt.date(), n), hour)


def working_days_between(start, end):
    """Días hábiles en (start, end] (el inicial no cuenta)."""
    count = 0
    day = start
    while day < end:
        day += timedelta(days=1)
        if is_working_day(day):
            count += 1
    return count


def parse_datetime(value):
    """Parsea un datetime ISO con zona (o naive → America/Santiago)."""
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=SANTIAGO)
    return parsed
