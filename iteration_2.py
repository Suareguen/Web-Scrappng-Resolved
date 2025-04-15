#### Iteration 2 #############

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from bs4 import BeautifulSoup

# Driver configuration (you can enable headless mode if needed)
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Uncomment this line for headless mode
driver = webdriver.Chrome(options=options)
products_data = []

try:
    # Step 1: Navigate to the main page with the product listings
    main_page_url = "https://guanxe.com/es/3628-portatiles?p=1"
    driver.get(main_page_url)
    
    # Wait until product links are loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.product-name"))
    )
    
    # Step 2: Retrieve the list of product links
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    product_elements = soup.select("a.product-name")
    product_links = [element.get('href') for element in product_elements if element.get('href')]
    
    # (Optional) Remove duplicates if any exist
    product_links = list(dict.fromkeys(product_links))
    
    # Iterate over each product link
    for link in product_links:
        driver.get(link)
        
        # Wait for the main product content to load.
        # Here, we wait for the container that holds the title to be present.
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div#derecha1"))
            )
        except Exception as e:
            print("Could not load the product page:", link)
            continue  # Skip to the next product
        
        # Step 3: Extract product information
        
        # Extract the product name
        try:
            product_name = driver.find_element(By.CSS_SELECTOR, "div#derecha1 h1").text
        except:
            product_name = "No available"
        
        # Extract the product price
        try:
            product_price = driver.find_element(By.CSS_SELECTOR, "span#our_price_display_right").text
        except:
            product_price = "No available"
        
        # Extract the product description
        try:
            product_description = driver.find_element(By.CSS_SELECTOR, "div#short_description_content").text
        except:
            product_description = "No available"
        
        # Print the extracted information
        print("Product Name:", product_name)
        print("Product Price:", product_price)
        print("Product Description:", product_description)
        print("--------------------------------------------------")
        
        # (Optional) Short delay between products to avoid overloading the server
        time.sleep(1)
        
        # Create a dictionary with product information and add it to the list
        product_info = {
            "name": product_name,
            "price": product_price,
            "description": product_description
        }
        products_data.append(product_info)
        
        print("Product added:", product_info)
        # (Optional) Short delay between products to avoid overloading the server
        time.sleep(1)
        
    # Step 4: Save the list of products to a JSON file
    with open("products.json", "w", encoding="utf-8") as file:
        json.dump(products_data, file, ensure_ascii=False, indent=4)
    
    print("File 'products.json' successfully created.")
        
except Exception as e:
    print("An error occurred:", e)
finally:
    driver.quit()
