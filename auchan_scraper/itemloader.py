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