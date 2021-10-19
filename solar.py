import time
import re
import math
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

print("Turning on and getting everything ready")

options = Options()
options.add_argument('--disable-infobars')
options.set_preference("permissions.default.geo", 1)
driver = webdriver.Firefox(options=options, executable_path=r'geckodriver.exe')
driver.set_page_load_timeout(30)
driver.implicitly_wait(30)

endpt = "https://globalsolaratlas.info/map?c={},11&s={}&m=site"

def travel(dest):
	driver.get(dest)

def find_solar():
	time.sleep(2)
	a = driver.find_element_by_css_selector('mat-list-item.mat-list-item:nth-child(2) > div:nth-child(1) > gsa-site-data-item:nth-child(3) > div:nth-child(1) > div:nth-child(4) > sg-unit-value:nth-child(1) > sg-unit-value-inner:nth-child(1)')
	tempele = driver.find_element_by_css_selector('mat-list-item.mat-list-item:nth-child(7) > div:nth-child(1) > gsa-site-data-item:nth-child(3) > div:nth-child(1) > div:nth-child(4) > sg-unit-value:nth-child(1) > sg-unit-value-inner:nth-child(1)')
	tempinner = tempele.get_attribute("innerHTML")
	temparr = re.findall('\d*\.?\d+',tempinner)
	tempa = math.ceil(float(temparr[0]))
	temp = int(tempa)
	b = a.get_attribute("innerHTML")
	c = re.findall('\d*\.?\d+',b)
	return int(math.ceil(float(c[0]))), temp

def savefl(flname, content):
	f = open(flname, "w")
	f.write(content)
	f.close()

def getLocation():
	url = "https://www.onlinegdb.com/RPj204xdq"
	driver.get(url)
	xpthselector = '#demo'
	runslector = '#control-btn-run'
	runbtn = driver.find_element_by_css_selector(runslector)
	runbtn.click()
	time.sleep(10)
	driver.switch_to.frame(1)
	latlon = driver.find_element_by_css_selector(xpthselector)
	latlong = latlon.get_attribute("innerHTML")
	driver.switch_to.default_content()
	return latlong


print("Getting Current Location. This takes around 15 seconds.")
latilong = getLocation()
print("Location Found: ",latilong,sep="")
print("Finding DNI and Air Temp at current location")
print("Accessing website")
travel(endpt.format(latilong,latilong))
print("Now looking for Direct Normal Irradiation (DNI) and Air Temperature.")
dni, airtemperature = find_solar()
print("Data Found!", end="\n\n")
print("DNI: ", end="")
print(dni)
print("Air Temperature: ", end="")
print(airtemperature,end="\n\n")
print("Saving DNI and Air Temperature to file")
savefl("dni.txt", str(dni))
savefl("airt.txt", str(airtemperature))
print("The data has been saved. Press any key to exit...")
driver.quit()
input()