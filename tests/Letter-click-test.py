from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from string import ascii_uppercase
import time
import os 
import thread

def fire_web_engine():
    os.system('python ../web_engine.py -d > /dev/null 2>&1')

thread.start_new_thread(fire_web_engine, ())

passed= True
browser = webdriver.Firefox() # Get local session of firefox
browser.implicitly_wait(10)
browser.get("http://localhost:8080/gameplay/3/1") # Load page

for c in ascii_uppercase:
	browser.get("http://localhost:8080/gameplay/3/1")
	actionChain = ActionChains(browser)
	elem = browser.find_element_by_name("guess") # Find the query box
	elem.send_keys("Testing " + c)
	try:
		letter = browser.find_element_by_class_name(c)
		letter.text #Gets the text in the element
		actionChain.double_click(letter).perform()
	except:
		print "Could not find the element with the letter " + c

	newletter = browser.execute_script("return getLG()")
	#assert newletter == c, "%r is not the letter we wanted %r" % (newletter,c)
	if newletter != c:
		print  "Testing letter " + c +" [Failed]"
		passed = False
	else:
		print  "Testing letter " + c + " [Success]"
	elem.clear();
		
if passed:
	print "All letters worked"
	print "Test[Passed]"
else:
	print "Some letters had problems"
	print "Test[Failed]"
#ActionChains(browser).double_click(letter).perform()

browser.close()
