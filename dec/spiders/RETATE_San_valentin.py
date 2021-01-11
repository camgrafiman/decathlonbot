from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.exporters import XmlItemExporter
from scrapy.loader.processors import TakeFirst
import random

# construir los campos del archivo:


class Producto(Item):
    imagen = Field(output_processor=TakeFirst())
    id = Field(output_processor=TakeFirst())
    titulo = Field(output_processor=TakeFirst())
    precio = Field(output_processor=TakeFirst())
    precio_a = Field(output_processor=TakeFirst())
    precio_b = Field(output_processor=TakeFirst())
    precio_previo = Field(output_processor=TakeFirst())
    reduccion = Field(output_processor=TakeFirst())
    marca = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    rating = Field(output_processor=TakeFirst())
    review = Field(output_processor=TakeFirst())
    modelId = Field(output_processor=TakeFirst())
    control_type = Field(output_processor=TakeFirst())


class decSpider(Spider):
    name = "RETATE_San_valentin"
    start_urls = [
        # Regalos san valentin:
        'https://www.decathlon.es/es/browse/c0-shops/c1-regalos-san-valentin/_/N-1vd55rq', 'https://www.decathlon.es/es/browse/c0-mujer/c1-calzado-deportivo/c3-zapatillas-skechers/_/N-1r2fue1'
    ]

    def parse(self, response):

        sel = Selector(response)
        productos = sel.xpath('//div[@id="js-product-wrapper"]/article')

        # sel.css también puede ser usado.
        # iterar sobre todos los productos:
        for i, elem in enumerate(productos):
            item = ItemLoader(Producto(), elem)
            item.add_xpath(
                # 'imagen', './div[@class="dkt-product__gallery"]/div/div/div/div/picture/source[5]/@srcset')
                # 'imagen', './div/div/div/div/div/picture/source[position()=4]/@srcset')
                'imagen', './div[@class="dkt-product__gallery"]/div/div/div[position()=1]/div/picture/source/source/source/source/source/@srcset')
            item.add_xpath(
                'titulo', 'normalize-space(div[@class="dkt-product__infos-wrapper"]/div[@class="dkt-product__infos__link"]/div/div/a/h2/text())')
            item.add_xpath(
                # 'precio', './div[@class="dkt-product__infos-wrapper"]/div/div/div[@class="dkt-product__price"]/div/div/@data-price')
                'precio', './div[@class="dkt-product__infos-wrapper"]/div/div/div[@class="dkt-product__price"]/div/div[@class="dkt-price__cartridge"]/@data-price' or './div[@class="dkt-product__infos-wrapper"]/div/div/div[@class="dkt-product__price"]/div/div/@data-price')
            item.add_xpath(
                'precio_a', 'normalize-space(.//div[@class="dkt-price__cartridge"]/text())')
            item.add_xpath(
                'precio_b', 'normalize-space(.//div[@class="dkt-price__cartridge"]/sup/text())')
            item.add_xpath(
                'precio_previo', './div[@class="dkt-product__infos-wrapper"]/div/div/div[@class="dkt-product__price"]/div/span/span[position()=1]/text()')
            item.add_xpath(
                'reduccion', './div[@class="dkt-product__infos-wrapper"]/div/div/div[@class="dkt-product__price"]/div/span/span[position()=2]/text()')
            item.add_xpath(
                'marca', './div[@class="dkt-product__infos-wrapper"]/div/div/div/span/span/text()')
            item.add_xpath(
                'url', './div[@class="dkt-product__infos-wrapper"]/div[@class="dkt-product__infos__link"]/div/div/a/@href')
            item.add_xpath(
                'rating', './div[@class="dkt-product__infos-wrapper"]/div/div/span[@itemprop="ratingValue"]/text()')
            item.add_xpath(
                'review', './div[@class="dkt-product__infos-wrapper"]/div/div/span[@itemprop="reviewCount"]/text()')
            item.add_xpath(
                'modelId', './div[@class="dkt-product__gallery"]/div/div[position()=1]/div[position()=1]/@data-modelid')
            item.add_value('id', i + random.randrange(10, 4000000))
            item.add_value('control_type', 'A')

            yield item.load_item()
        # Paginacion con el botón más productos:
        # boton_next = response.css('button #more_product_a').extract_first()
        # if boton_next:
        #     boton_next = response.urljoin(boton_next)
        #     # ahora repetir el proceso en la nueva url con la funcion parse
        #     yield scrapy.Request(url=boton_next, callback=self.parse)


# correr el programa en consola:
# scrapy runspider spider.py -o datos.csv -t csv
