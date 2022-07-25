from flask import Flask, request, jsonify, render_template
import re
import os
from selenium import webdriver
import time
from PIL import Image
import io
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.chrome.service import Service
#Install Driver
def find_price(a_list):
    output = [idx  for idx, element in enumerate(a_list) if re.search('(\d[TL])\w+', element) !=None ]
    # return output
    if output ==[]:
        return len(a_list)

    if output !=[]:
        return output[0]
def scrapper():
	print('driver started')
	driver = webdriver.Chrome(ChromeDriverManager().install())
	print('link ')
	URL = """https://www.amazon.com.tr/s?k=apple&rh=n%3A12466496031%2Cn%3A26232650031&dc&ds=v1%3A24QIKEr1whZX7fY03aG1Rzroi24YQzoigI1WMNytis0&__mk_tr_TR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=9UPC9JZMBEZY&qid=1658327018&rnid=13818411031&sprefix=appl%2Caps%2C122&ref=sr_nr_n_4"""
	print('getting URL')
	driver.get(URL)
	print('URL exracted')
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(10)#sleep_between_interactions
	web_res = driver.find_elements(By.XPATH,"//div[@class='a-section a-spacing-small s-padding-left-small s-padding-right-small']")
	product = []

	for x in web_res:
	    product.append(x.text)

	data = []
	for i in product:

	    TL_flag = False

	    broken_names = i.split("\n")

	    price_end_index = find_price(broken_names)

	    if '+' not in broken_names[0]:

	        p = broken_names[0]
	    if '+' in broken_names[0]:
	        p = broken_names[1]
	    for t in broken_names:

	        if 'TL' in t:
	        	TL_flag = True
	    if TL_flag == True :
	    	price = ','.join(broken_names[price_end_index-1:price_end_index+1])
	    if TL_flag == False:
	    	price = "NA"
	    data.append((p,price))

	print(data)
	#driver.close()	 
	rs = json.dumps(dict(data))
	import pandas as pd

	rs = pd.read_json(rs,orient="index").reset_index()
	rs.columns = ['Product Name', 'Price']
	return rs

print('app started')
app = Flask(__name__)
#webdriver.Chrome(service=Service(ChromeDriverManager().install())) #webdriver.Chrome(ChromeDriverManager().install())





@app.route("/",methods=(["GET"])) #, methods=("POST", "GET"),methods=(["POST"])
def getData():
	rs  = scrapper()

	return render_template('scraper.html',  tables=[rs.to_html(classes='data')], titles=rs.columns.values)


if __name__ == "__main__":
    app.run(port = 5000, debug=True)