import scrapy
from scrappingSuperM.enums import ProductCategory,ProductBrand
from scrappingSuperM.items import Product
from scrapy_playwright.page import PageMethod

class SantaisabelSpider(scrapy.Spider):
    
    name = "santaIsabel"
    brands = [category.value for category in ProductBrand]


    def start_requests(self):
        for busqueda in self.brands:
            #url = f"https://www.santaisabel.cl/busqueda?ft={busqueda}&page=1"
            busqueda = busqueda.replace(' ', '-') 
            url = f"https://www.santaisabel.cl/{busqueda}?page=1"
            yield scrapy.Request(url,meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[  
                    PageMethod("wait_for_selector", "div.shelf-content"),
                ],
                busqueda = busqueda,
                errback=self.errback,
                )
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        busqueda = response.meta.get("busqueda")
        await page.screenshot(path=f"{busqueda}.png")
        await page.wait_for_selector("div.product-card")
        
        await page.close()

        products = response.css("div.product-card")

        for product in products:
            productName = product.css("a.product-card-name::text").get()
            product = Product(
                name = productName,
                actualPrice = product.css("span.prices-main-price::text").get(),
                oldPrice = product.css("span.prices-old-price::text").get(),
                brand = product.css("a.product-card-brand::text").get(),
                supermarket = "SantaIsabel",
                tipe = productName.split()[0]
            )
            yield product
        
        
        actual_page = response.css('div.slides button.page-number.active::text').get()
        pages = response.css('div.slides button.page-number:not(.active)::text').getall()
        list_pages_true = []
        if pages:
            for i in pages:
                if actual_page < i:
                    list_pages_true.append(i)

        self.log(f"LABUSQUEDA: {busqueda}")
        self.log(f"PaginasActuales{list_pages_true}")
        if list_pages_true:
            for i in list_pages_true:
                self.log(f"PAGINACTUAL{i}")

                url_page = f"https://www.santaisabel.cl/{busqueda}?page={i}"
                
                next_page_url = response.urljoin(url_page)
                yield scrapy.Request(
                    next_page_url,
                    meta=dict(
                        playwright=True,
                        playwright_include_page=True,
                        playwright_page_methods=[  
                        PageMethod("wait_for_selector", "div.shelf-content"),
                        ],
                        errback=self.errback,
                        busqueda = busqueda,
                    ),
                )

    async def errback(self, failure):
       page = failure.request.meta["playwright_page"]
       await page.close()
       print("Ha ocurrido un error")