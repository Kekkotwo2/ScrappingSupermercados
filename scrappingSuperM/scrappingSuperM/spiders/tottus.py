import scrapy
from scrappingSuperM.enums import ProductCategory,ProductBrand
from scrappingSuperM.items import Product
from scrapy_playwright.page import PageMethod


class TottusSpider(scrapy.Spider):
    name = "tottus"

    def start_requests(self):
            url = f"https://www.tottus.cl/tottus-cl/marca/RECETA%20DEL%20ABUELO"
            yield scrapy.Request(url,meta=dict(
                playwright=True,
                playwright_include_page=True,
                errback=self.errback
                
                )
            )
    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.screenshot(path=f"totus.png")
        await page.close()

        products = response.css("div.jsx-1068418086.search-results-4-grid.grid-pod")
        self.log("Produtos")
        self.log(products)
        for product in products:
            productName = product.css("b.jsx-184544934.copy2.primary.jsx-3451706699.normal.line-clamp.line-clamp-3.pod-subTitle.subTitle-rebrand::text").get()
            product = Product(
                name = productName,
                actualPrice = product.css("span.copy10.primary.medium.jsx-3451706699.normal.line-height-22::text").get(),
                oldPrice = product.css("span.copy3.primary.medium.jsx-3451706699.normal.crossed.line-height-17::text").get(),
                brand = product.css("b.jsx-184544934.title1.secondary.jsx-3451706699.bold.pod-title.title-rebrand::text").get(),
                supermarket = "Tottus",
                tipe = productName.split()[0]
            )
            yield product
        
        
    async def errback(self, failure):
       page = failure.request.meta["playwright_page"]
       await page.close()
       print("Ha ocurrido un error")
