from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst

class AuchanProductLoader(ItemLoader):

    default_output_processor = TakeFirst()