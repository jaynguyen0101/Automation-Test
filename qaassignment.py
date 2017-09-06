"""
Avenuecode

Jay Nguyen - Automation QA Assignment Part 2
Programing Language: Python2.7 or python 3.x
Testing Platform: Selenium - Latest version 3.5.1
Date: 08/03/2017

Requirements: 
 - Install python2.7 or 3.x
 - Install Selenium by using command in terminal: 
        + "pip install selenium" - python 2.7 
        + or "pip3 install selenium" - python 3.x
 - Download Chrome Driver at http://chromedriver.storage.googleapis.com/index.html?path=2.30/
 - Modify driverPath to correct path of chromedriver. 

Execute the script: 
    python qaassignemtn.py - python2.7
    python3 qaassignemtn.py - python3.x

"""

import time
import re
from selenium import webdriver
from datetime import datetime

url = "http://qa-test.avenuecode.com/"
auth = ('jaynguyen0101@gmail.com', '123456789bB')

driverPath = "/Users/jaynguyen/Documents/chromedriver"

#Login Processclear
def login_mech(driver):
    global auth
    errorOccurred = False
    user = "input[id*='user_email']"
    passw = "input[id*='user_password']"
    submit = "input[class*='btn btn-primary']"
    uname = auth[0]
    pw = auth[1]
    print("START LOGIN PROCESS")
    try:
        username = driver.find_element_by_css_selector(user)
        password = driver.find_element_by_css_selector(passw)
        username.send_keys(uname)
        password.send_keys(pw)
        driver.find_element_by_css_selector(submit).click()
        time.sleep(2)
    except NoSuchElementException:
        errorOccurred = True
        
    return errorOccurred

#Getting all attribute names of a web element
def get_web_element_attribute_names(web_element):
    # get element html
    html = web_element.get_attribute("outerHTML")
    # find all with regex
    pattern = """([a-z]+-?[a-z]+_?)='?"?"""
    return re.findall(pattern, html)

#Checking for min and max length and verify the requirements
def check_for_min_max_length(driver, task_path):
    #Gettign all attribune of task_path
    task_description_element = driver.find_element_by_css_selector(task_path)
    task_description_attributes = get_web_element_attribute_names(task_description_element)
    attribute_min_check = False
    attribute_max_check = False
    min_length = ""
    max_length = ""
    for attribute in task_description_attributes:
        #Check for minlength attribune
        if(attribute == "minlength"):
            attribute_min_check = True
        if(attribute_min_check):
            min_length = task_description_element.get_attribute("minlenght")
            break
        #Check for maxlength attribune    
        if(attribute == "maxlength"):
            attribute_max_check = True
        if(attribute_max_check):
            max_length = task_description_element.get_attribute("maxlength")
            break

    #Creating task with minlength > 3 characters
    if(attribute_min_check):
        if(int(min_length) >= 3):
            print("PASSED: Min Length is greater than 3 charaters")
        elif(int(min_length) < 3):
            print("FAILED: Min Length less than 3 characters")
    else:
        print("FAILED: There are none minlength attribute")

    #Creating task with maxlenght <= 250 characters
    if(attribute_max_check):
        if(int(max_length) > 250):
            print("FAILED: Max Length is greater than 250 charaters")
            print("\tMax Lenght: " + max_length)
        elif(int(max_length) <= 250):
            print("PASSED: Max Length is 250 characters")
    else:
        print("FAILED: There are none maxlength attribute")

def check_exsiting_attribune(driver, path, attribute_name):
    element = driver.find_element_by_css_selector(path)
    attributes = get_web_element_attribute_names(element)
    attribute_check = False
    for attribute in attributes:
        #Checking for readonly.
        if(attribute == attribute_name):
            attribute_check = True
            break
    return attribute_check
#Main test runs with chrome
def chrome_test(url):
    driver = webdriver.Chrome(driverPath)
    driver.set_page_load_timeout(20)
    driver.get(url)
    # time.sleep(5)
    try:
        sign_in_button = "a[href*='sign_in']"
        driver.find_element_by_css_selector(sign_in_button).click()
        time.sleep(1)
        print("Need to log in to qa-test avenuecode page to continue...")
        errorOccurred = login_mech(driver)
        if(not errorOccurred):
            print("LOGIN SUCCESSFUL")
        time.sleep(1)

        #Going to My Task Page.
        my_task_button = "a[class*='btn btn-lg btn-success']"
        driver.find_element_by_css_selector(my_task_button).click()
        
        print("\nUS#1 - Running Test")

        #Getting login username
        welcome_message_element = "a[href='#']"
        welcome_message_element_text = driver.find_element_by_css_selector(welcome_message_element)
        login_user = str(welcome_message_element_text.text).replace("Welcome, ", "")
        login_user = login_user.replace("!", "")

        #US#1 - Greeting message 
        US_1_01_check = False
        greeting_message = "'Hey "+login_user+", this is your todo list for today:'"

        #Getting all text value of h1 tag
        h1_list = driver.find_elements_by_tag_name('h1')
        for h1_item in h1_list:
            if(greeting_message == h1_item.text):
                US_1_01_check = True
                break
        #Getting all text value of p tag
        if(not US_1_01_check):
            p_list = driver.find_elements_by_tag_name('p')
            for p_item in p_list:
                if(greeting_message == p_item.text):
                    US_1_01_check = True
                    break
        if(US_1_01_check == False):
            print("FAILED: Can not locate greeting mesage: " + greeting_message)
        else: 
            print("PASSED: Located greeting message: " + greeting_message)

        

        #Checking for minlength and maxlength    
        task_description_path = "input[name='new_task']"
        check_for_min_max_length(driver, task_description_path)

        
        print("\nUS#2 - Running Test")
        #Checking for task table list
        table_element  = driver.find_elements_by_tag_name('tbody')
        if(len(table_element) > 0): #valid list, has at least 1 element

            #Click on manage subtask button
            manage_subtasks = "button[class='btn btn-xs btn-primary ng-binding']"
            driver.find_element_by_css_selector(manage_subtasks).click()

            #Getting all attribunes of main task description under subtask tab
            main_task_description = "textarea[name='edit_task']"
            attribute_readonly_check = check_exsiting_attribune(driver, main_task_description, "readonly")
            #Printing all alerts
            if(attribute_readonly_check):
                print("PASSED: Main Task Description is read only field")
            else:
                print("FAILED: Main Task Description is editable field")

            #Checking for minlength and maxlength    
            sub_task_description_path = "input[name='new_sub_task']"
            check_for_min_max_length(driver, sub_task_description_path)

            #Getting due date value
            due_date_path = "input[name='due_date']"
            due_date_element = driver.find_element_by_css_selector(due_date_path)
            due_date = due_date_element.get_attribute("value")
            due_date_list = due_date.split('/')
            month = due_date_list[0]
            day = due_date_list[1]
            year = due_date_list[2]
            #Format duedate to MM/dd/yyyy format
            format_due_date = datetime(int(year), int(month), int(day))
            format_due_date_mmddyyyy = format_due_date.strftime('%m/%d/%y')
            if(format_due_date_mmddyyyy == due_date):
                print("PASSED: Due Date has MM/dd/yyyy format")
            else: 
                print("FAILED: Due Date does not have MM/dd/yyyy format")


            #Getting all attribunes of sub task description
            sub_task_description_required_check = check_exsiting_attribune(driver, sub_task_description_path, "required")
            if(sub_task_description_required_check):
                print("PASSED: The SubTask Description is required")
            else: 
                print("FAILED: The SubTask Description does not have required attribune")

            #Getting all attribunes of Due Date
            due_date_required_check = check_exsiting_attribune(driver, due_date_path, "required")
            if(due_date_required_check):
                print("PASSED: The Due Date is required")
            else: 
                print("FAILED: The Due Date does not have required attribune")
            

        else:
            print("FAILED: Empty Task Table")


        driver.quit()
    except Exception as e:
        print(e)
        driver.quit()
     
def run():
    print("AvenueCode - Jay Nguyen - QA Assignemnt\n")
    chrome_test(url)

run()
