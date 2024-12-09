# import asyncio
# import time
# # undetected-playwright here!
# from undetected_playwright.async_api import async_playwright, Playwright


# async def run(playwright: Playwright):
#     args = []
    
#     # disable navigator.webdriver:true flag
#     args.append("--disable-blink-features=AutomationControlled")
#     browser = await playwright.chromium.launch(headless=True,
#                                                args=args)
#     page = await browser.new_page()
#     await page.goto("https://www.jumbo.cl/receta-del-abuelo?page=1")
#     time.sleep(10)
   
#     time.sleep(2)
#     await page.screenshot(path=f"totus.png")
#     await browser.close()




# async def main():
#     async with async_playwright() as playwright:
#         await run(playwright)


# if __name__ == "__main__":
#     loop = asyncio.ProactorEventLoop()
#     loop.run_until_complete(main())
#     # asyncio.run(main) # should work for non-Windows as well