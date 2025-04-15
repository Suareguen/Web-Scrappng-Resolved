from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

# Set up the Chrome driver
options = webdriver.ChromeOptions()
# Uncomment the following line to run Chrome in headless mode if desired:
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

try:
    # Step 1: Navigate to the main page with the product listings
    main_page_url = "https://guanxe.com/es/3628-portatiles?p=1"
    driver.get(main_page_url)

    # Wait until at least one product link is present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.product-name"))
    )

    # Step 2: Find the first product link and click on it
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    product_links = soup.select("a.product-name")

    if product_links:
        first_product_link = product_links[0].get('href')
        driver.get(first_product_link)
    else:
        raise Exception("No product links found")

    # Step 3: Wait for the product detail page to load
    # We wait until the price element is present on the detail page
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span#our_price_display_right"))
    )

    # Step 4: Extract the product information

    # Extract the product name (found within the <h1> tag in the section with id "derecha1")
    product_name = driver.find_element(By.CSS_SELECTOR, "div#derecha1 h1").text

    # Extract the product price (from the span with id "our_price_display_right")
    product_price = driver.find_element(By.CSS_SELECTOR, "span#our_price_display_right").text

    # Extract the product description (from the div with id "short_description_content")
    try:
        product_description = driver.find_element(By.CSS_SELECTOR, "div#short_description_content").text
    except:
        product_description = "No description available"

    # Print the extracted information
    print("Product Name:", product_name)
    print("Product Price:", product_price)
    print("Product Description:", product_description)

except Exception as e:
    print("An error occurred:", e)
finally:
    driver.quit()
