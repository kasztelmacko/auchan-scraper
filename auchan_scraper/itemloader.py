from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst


def convert_price(value):
    try:
        return float(value)
    except ValueError:
        return None

class AuchanProductLoader(ItemLoader):

    default_output_processor = TakeFirst()

    # convert the price to a float
    price_in = MapCompose(convert_price)
    price_out = TakeFirst()

    # split the volume into a number and a unit
    volume_in = MapCompose(lambda x: x.rsplit(" ", 1)[0] if x else None)
    unit_in = MapCompose(lambda x: x.rsplit(" ", 1)[1] if x else None)
    volume_out = TakeFirst()
    unit_out = TakeFirst()