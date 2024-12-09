import scrapy
from scrappingSuperM.enums import ProductCategory,ProductBrand
from scrappingSuperM.items import Product
from scrapy_playwright.page import PageMethod

class SupertrebolSpider(scrapy.Spider):
    name = "superTrebol"
 
    def start_requests(self):
        url = f"https://www.supertrebol.cl/vendors/san-jorge"
        yield scrapy.Request(url,meta=dict(
            playwright=True,
            playwright_include_page=True,
            )
        )
    async def parse(self, response):
        self.log("Entro a la pagina correctamente")
        page = response.meta["playwright_page"]
        await page.screenshot(path=f"supertrebol.png")
        
        await page.close()
        
        products = response.css("li.product-item")

        for product in products:
            # Extraer el nombre del producto
            productName = product.css('h3.product-model::text').get()
            self.log(f"{productName}")