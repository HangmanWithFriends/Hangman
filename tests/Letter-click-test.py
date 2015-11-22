from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from string import ascii_uppercase
import time

passed= True
browser = webdriver.Firefox() # Get local session of firefox
browser.implicitly_wait(10)
browser.get("http://localhost:8080/gameplay/1/1") # Load page

for c in ascii_uppercase:
	
	actionChain = ActionChains(browser)
	elem = browser.find_element_by_name("guess") # Find the query box
	elem.send_keys("Testing " + c)
	try:
		letter = browser.find_element_by_class_name(c)
		letter.text #Gets the text in the element
		actionChain.double_click(letter).perform()
	except:
		print "Could not find teh element with the letter " + c

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