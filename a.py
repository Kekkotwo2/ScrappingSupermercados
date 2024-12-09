import undetected_chromedriver as uc
import time
driver = uc.Chrome(headless=True)

driver.get("https://www.tottus.cl/tottus-cl/marca/RECETA%20DEL%20ABUELO")
time.sleep(5)
driver.save_screenshot('nowsecure.png')