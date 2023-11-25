from yargy import Parser, rule, or_, and_
from yargy.predicates import (
    eq,
    type,
    normalized,
    gte,
    lte,
    dictionary,
)
from yargy.interpretation import fact


DOT = eq(".")
INT = type("INT")
SPACE = eq(" ")


Date = fact("Date", ["year", "month", "day"])


MONTHS = {
    "январь": 1,
    "февраль": 2,
    "март": 3,
    "апрель": 4,
    "май": 5,
    "июнь": 6,
    "июль": 7,
    "август": 8,
    "сентябрь": 9,
    "октябрь": 10,
    "ноябрь": 11,
    "декабрь": 12,
}

MONTH_NAME = dictionary(MONTHS).interpretation(
    Date.month.normalized().custom(MONTHS.get)
)

MONTH = and_(INT, gte(1), lte(12)).interpretation(Date.month.custom(int))

YEAR = and_(INT, gte(1000), lte(3000)).interpretation(Date.year.custom(int))

YEAR_SUFFIX = rule(or_(eq("г"), normalized("год")), DOT.optional())

DAY = and_(INT, gte(1), lte(31)).interpretation(Date.day.custom(int))

DATE = or_(
    rule(YEAR, YEAR_SUFFIX),
    rule(MONTH_NAME, YEAR),
    rule(DAY, DOT.optional(), MONTH, DOT.optional(), YEAR),
    rule(YEAR, DOT.optional(), MONTH, DOT.optional(), DAY),
    rule(DAY, MONTH_NAME, YEAR),
)

DATE = rule(
    DATE,
).interpretation(Date)
