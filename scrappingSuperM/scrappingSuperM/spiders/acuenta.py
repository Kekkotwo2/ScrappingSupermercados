import scrapy
from scrappingSuperM.enums import ProductCategory,ProductBrand
from scrappingSuperM.items import Product
from scrapy_playwright.page import PageMethod

class AcuentaSpider(scrapy.Spider):
    
    name = "acuenta"
    brands = [category.value for category in ProductBrand]


    def start_requests(self):
        for busqueda in self.brands:
            #url = f"https://www.santaisabel.cl/busqueda?ft={busqueda}&page=1"
            busqueda = busqueda.replace(' ', '%20') 
            url = f"https://www.acuenta.cl/search?name=san%20jorge"
            yield scrapy.Request(url,meta=dict(
                playwright=True,
                playwright_include_page=True,
                errback=self.errback,
                busqueda = busqueda
                )
            )

    async def parse(self, response):
        self.log("ENTRAMOS AL PARSE")
        page = response.meta["playwright_page"]
        busqueda = response.meta.get("busqueda")
        busqueda = busqueda.replace('%20', ' ')
        await page.screenshot(path=f"acuenta.png")
        
        await page.close()

        #Productos "normales"
        products = response.css("div.card-product-vertical.product-card-default")
        #Productos con descuento
        discountProducts = response.css("div.card-product-vertical.product-card-crossedOut")
        #Productos que estan 2x1 -- este no esta tomando aun
        twoXoneProducts = response.css("div.card-product-vertical.product-card-nx$")
        self.log(f"Listado de productos: {twoXoneProducts}")

        for product in products:
            productName = product.css("p.CardName__CardNameStyles-sc-147zxke-0.bWeSzf.prod__name::text").get()
            price = product.css("p.CardBasePrice__CardBasePriceStyles-sc-1dlx87w-0.bhSKFL.base__price::text").get()
            
            product = Product(
                name = productName,
                actualPrice = price,
                oldPrice = product.css("p.prod-crossed-out__price__old::text").get(),
                brand = busqueda,
                supermarket = "Acuenta",
                tipe = productName.split()[0]
            )
            yield product
        if discountProducts:
            for product in discountProducts:
                productName = product.css("p.CardName__CardNameStyles-sc-147zxke-0.bWeSzf.prod__name::text").get()
                price = product.css("p.base__price::text").get()

                product = Product(
                    name = productName,
                    actualPrice = price,
                    oldPrice = product.css("p.prod-crossed-out__price__old::text").get(),
                    brand = busqueda,
                    supermarket = "Acuenta",
                    tipe = productName.split()[0]
                )
                yield product
                
        if twoXoneProducts:
            for product in twoXoneProducts:
                productName = product.css("p.CardName__CardNameStyles-sc-147zxke-0.bWeSzf.prod__name::text").get()
                price = product.css("p.CardBasePrice__CardBasePriceStyles-sc-1dlx87w-0.bhSKFL.base__price::text").get()

                product = Product(
                    name = productName,
                    actualPrice = price,
                    oldPrice = product.css("p.prod-crossed-out__price__old::text").get(),
                    brand = busqueda,
                    supermarket = "Acuenta",
                    tipe = productName.split()[0]
                )
                yield product
    async def errback(self, failure):
       page = failure.request.meta["playwright_page"]
       await page.close()
       print("Ha ocurrido un error")