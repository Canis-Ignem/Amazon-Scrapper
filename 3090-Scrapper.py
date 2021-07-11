from selenium import webdriver
from time import sleep
import argparse
import smtplib


parser = argparse.ArgumentParser(description="Amazon scrapper")
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
    original_xpath = '/html/body/div[1]/div[2]/div[1]/div/div[1]/div/span[3]/div[2]/div[{}]/div/span/div/div/div[2]/div[1]/h2/a'
                      
    sleep(0.5)
    
    body = ""
    
    for i  in range(1,len(titles)):
        
        try:
            #item_price = driver.find_element_by_xpath('//span[@class="a-size-base-plus a-color-base a-text-normal"][contains(text(),"3090")]/following::span[contains(@class,"price-whole")]')
            #title = driver.find_element_by_xpath(original_xpath.format(i))
            product = driver.find_element_by_xpath(original_xpath.format(i))
            if item in product.text:
                item_price = driver.find_element_by_xpath(original_xpath.format(i)+'/following::span[contains(@class,"price-whole")]')
                print(item_price.text)
                if price > int(item_price.text.replace(".","").split(",")[0]):
                    body += "Product name: {} \n Price: {} \n Link: {} \n ------------------------------------------------\n".format(str(product.text.encode())[2:-1], item_price.text.replace(".","").split(",")[0], product.get_attribute("href") ) 
                    print(body)
        except:
            break
    
    if body != "":
        print()
        send_email(item,body)
        
        #product = driver.find_element_by_xpath('//div[@class="a-section a-spacing-medium"][contains(text(),"3090")] ')
        #print(product.text)
        
    driver.close()
    
def send_email(item, body):
    subject = item
    
    email = "jonperezetxebarria@gmail.com"
    sender_email = "jonperezetxebarria@gmail.com"
    pas= "mpmppwoxfvwnzbyg"
    message = "Subject: {}\n\n{}".format(subject,body)
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.login(sender_email, pas)
        s.sendmail(sender_email, email, message)         
        print( "Successfully sent email to: ", email)
        s.quit()
    except Exception as vx:      
        print(vx)        
    
def main():
    while True:
        amazon_scrapper(args['item'],args['price'])
        sleep(2)

if __name__ == '__main__':
    main()
    