import scrapy
from scrappingSuperM.items import Product
from scrapy_playwright.page import PageMethod

class EltitSpider(scrapy.Spider):
    name = "eltit"
 
    def start_requests(self):
        url = f"https://super.eltit.cl/vendors/san-jorge"
        yield scrapy.Request(url,meta=dict(
            playwright=True,
            playwright_include_page=True,
            )
        )
    async def parse(self, response):
        self.log("Entro a la pagina correctamente")
        page = response.meta["playwright_page"]
        await page.screenshot(path=f"eltit.png")
        
        await page.close()
        
        products = response.css("li.product-item")
        contador = 0

        for product in products:
            # Extraer el nombre del producto
            productName = product.css('span.product-model::text').get()
            price = product.css('span.bootic-price::text').get()

            product = Product(
                name = productName,
                actualPrice = price,
                oldPrice = product.css("span.bootic-price-comparison::text").get(),
                brand = "busqueda",
                supermarket = "Eltit",
                tipe = productName.split()[0],
                promotion = product.css("p.vol-discount-text::text").get()
            )
            yield product