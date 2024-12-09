
import scrapy
from scrapy_playwright.page import PageMethod
import time

class LiderSpider(scrapy.Spider):
    name = "lider2"
  
    def start_requests(self):
            url = f"https://www.lider.cl/supermercado"
            yield scrapy.Request(url,meta=dict(
                playwright=True,
                playwright_include_page=True,
                errback=self.errback,
                playwright_page_methods=[  
                    PageMethod("wait_for_selector", "div.banners-home__banner"),
                ],
                )
            )
    async def parse(self, response):
        page = response.meta["playwright_page"]
        self.log("timesleep")
        time.sleep(15)
        await page.screenshot(path=f"lider1.png")
        await page.close()

        self.log("Entro a la pag")


    async def errback(self, failure):
       page = failure.request.meta["playwright_page"]
       await page.close()
       print("Ha ocurrido un error")