from selenium import webdriver
from time import sleep
import argparse


parser = argparse.ArgumentParser(description="NBGRADER partner script")
parser.add_argument('--item', metavar = 'i', type = str, required = True)
parser.add_argument('--price', metavar = 'p', type = int, required = True)
args = vars(parser.parse_args())




def amazon_scrapper(item,price):
    my_driver = "chromedriver.exe"


    driver = webdriver.Chrome(my_driver)

    driver.get("https://www.amazon.es/")

    sleep(2)
    
    search_bar = driver.find_element_by_xpath('//input[@id="twotabsearchtextbox"]')
    search_bar.send_keys(item)

    sleep(0.5)
    
    search = driver.find_element_by_xpath('/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[4]/div/span/input')
    search.click()

    sleep(2)
    
    
    # Solution one
    ''' 
    products =  driver.find_elements_by_xpath('//div[@class="a-section a-spacing-medium"]')
    
    for p in products:
        
        tittle = p.find_element_by_xpath('.//span[@class="a-size-base-plus a-color-base a-text-normal"]')
    
        print(tittle.text)
    
    '''
    
    titles = driver.find_elements_by_xpath('//span[@class="a-size-base-plus a-color-base a-text-normal"][contains(text(),"3090")]')
    original_xpath = '/html/body/div[1]/div[2]/div[1]/div/div[1]/div/span[3]/div[2]/div[{}]/div/span/div/div/div[2]/div[1]/h2/a/span'
    sleep(0.5)
    
    for i  in range(1,len(titles)):
        
        try:
            #item_price = driver.find_element_by_xpath('//span[@class="a-size-base-plus a-color-base a-text-normal"][contains(text(),"3090")]/following::span[contains(@class,"price-whole")]')
            title = driver.find_element_by_xpath(original_xpath.format(i))
            if "3090" in title.text:
                item_price = driver.find_element_by_xpath(original_xpath.format(i)+'/following::span[contains(@class,"price-whole")]')
                if price > int(item_price.text.replace(".","").split(",")[0]):
                    print(title.text)
                    print("The price",item_price.text)
                    print("------------------------------------------------")
                    
        except:
            break
        
        #product = driver.find_element_by_xpath('//div[@class="a-section a-spacing-medium"][contains(text(),"3090")] ')
        #print(product.text)
        
    driver.close()
        
    
def main():
    while True:
        amazon_scrapper(args['item'],args['price'])
        sleep(2)

if __name__ == '__main__':
    main()
    