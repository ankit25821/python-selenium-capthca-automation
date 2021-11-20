from pytesseract import image_to_string 
import pytesseract
from PIL import Image 
from selenium import webdriver
from flask import Flask


app = Flask(__name__)

url = 'https://esearchigr.maharashtra.gov.in/portal/esearchlogin.aspx'

@app.route("/")
def home():
	return '<a href="/start/captcha/">Click here to run automation.</a>'

@app.route("/start/captcha/")
def login_to_website():
	driver = webdriver.Chrome(executable_path="./chromedriver")
	driver.get(url)
	# driver.set_window_size(1120, 550)
	#find part of the page you want image of
	element = driver.find_element_by_xpath('//*[@id="form1"]/div[3]/div[4]/div[2]/div[2]/div/table/tbody/tr[3]/td[1]/img')
	location = element.location
	size = element.size
	driver.save_screenshot('screenshot.png')
	user_id = driver.find_element_by_xpath('//*[@id="txtUserid"]')
	user_id.clear()
	user_id.send_keys('your-username')
	password = driver.find_element_by_xpath('//*[@id="txtPswd"]')
	password.clear()
	password.send_keys('your-password')
	captcha = driver.find_element_by_xpath('//*[@id="txtcaptcha"]')
	captcha.clear()
	captcha_text = get_captcha_text(location, size)
	captcha.send_keys(captcha_text)
	driver.find_element_by_xpath('//*[@id="btnLogin"]').click()

def get_captcha_text(location, size):
	pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
	im = Image.open('screenshot.png')
	left = location['x']
	top = location['y']
	right = location['x'] + size['width']
	bottom = location['y'] + size['height']
	im = im.crop((left, top, right, bottom))
	im.save('screenshot.png')
	captcha_text = image_to_string(Image.open('screenshot.png'))
	return captcha_text

if __name__ == '__main__':
	app.run(5000)
