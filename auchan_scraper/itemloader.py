import re
from typing import Optional

from itemloaders.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader

DEFAULT_VALUE = "Unknown"


def convert_price(value):
    try:
        return float(value)
    except ValueError:
        return None


# 600g / 600 g / na wagę ok. 600g / sztuka / '1.2 kg', 'na wagę ok. 1.5kg ' / 'na wagę ok. 1.1kg'
VOLUME_REGEX = re.compile(r"[\D]*([\d\.\,]+)\s*(\w+)")

UNIT_REGEX = re.compile(
    r"(sztuka|sztuki|zestaw|pęczek|opakowanie)", flags=re.IGNORECASE
)
VOLUME_REGEX = re.compile(
    r"(?i)[\D]*([\d\.\,]*)\s*(\w+)(?:\s*x\s*(\d+))?", flags=re.IGNORECASE
)


def normalize_amount(amount) -> float:
    if amount:
        return float(amount.replace(",", "."))
    return 1.0


def normalize_unit(unit) -> Optional[str]:
    if unit:
        unit = str(unit).lower()
        if unit in ("sztuka", "sztuki", "zestaw"):
            return "unit"
        return unit
    return DEFAULT_VALUE


def process_volume_info(value) -> tuple[float, Optional[str]]:
    matches = re.search(VOLUME_REGEX, value)
    if matches:
        if matches.group(1):
            if matches.group(3):
                multiplier = int(matches.group(3))
            else:
                multiplier = 1
            return (
                normalize_amount(matches.group(1)) * multiplier,
                normalize_unit(matches.group(2)),
            )
        elif UNIT_REGEX.match(value):
            # sztuka, zestaw, pęczek, opakowanie
            return (1, "unit")

    return (1, DEFAULT_VALUE)


def extract_volume(value):
    return process_volume_info(value)[0]


def extract_unit(value):
    return process_volume_info(value)[1]


class AuchanProductLoader(ItemLoader):
    # might want to use Identity() instead of TakeFirst() for some fields
    default_output_processor = TakeFirst()  # Omits None values

    # convert the price to a float
    price_in = MapCompose(convert_price)
    price_out = TakeFirst()

    # split the volume into a number and a unit
    volume_in = MapCompose(extract_volume)
    unit_in = MapCompose(extract_unit)
    volume_out = TakeFirst()
    unit_out = TakeFirst()

    volume_info_out = TakeFirst()
    package_unit_out = TakeFirst()
    package_size_out = TakeFirst()
