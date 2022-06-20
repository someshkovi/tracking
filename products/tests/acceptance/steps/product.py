import time

from behave import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

use_step_matcher('re')


@given('I am on the Django Admin')
def step_impl(context):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    context.selenium = webdriver.Chrome(options=chrome_options)

    # Login to the Admin Panel
    context.selenium.get(f'{context.test.live_server_url}/admin/')

    # Fill Login Information
    username = context.selenium.find_element_by_id('id_username')
    username.send_keys('admin')
    password = context.selenium.find_element_by_id('id_password')
    password.send_keys('admin')

    # Locate login button and click on it
    context.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
    context.test.assertEquals(context.selenium.title, "Site administration | Django site admin")


@when('I click on the "(.*)" link')
def step_impl(context, name):
    context.selenium.find_element_by_link_text(f"{name}").click()


@then('I am on the "(.*)" page')
def step_impl(context, name):
    context.test.assertEquals(f"Select {name} to change | Django site admin", context.selenium.title)
    # name = str(name).lower()
    # context.selenium.refresh()
    # context.selenium.find_element_by_xpath(f"//a[@href='/admin/product/{name}/add/']").click()
    # context.test.assertEquals("Add product | Django site admin", context.selenium.title)


@then('I will click on "(.*) add button')
def step_impl(context, name):
    name = str(name).lower()
    context.selenium.refresh()
    context.selenium.find_element_by_xpath(f"//a[@href='/admin/products/product/add/']").click()
    context.test.assertEquals("Add product | Django site admin", context.selenium.title)


@then('I will add new information for Product Section')
def step_impl(context):
    name = context.selenium.find_element_by_xpath(f"//input[@id='id_name']")
    name.send_keys('Test Product')
    price = context.selenium.find_element_by_xpath(f"//input[@id='id_price']")
    price.send_keys(12)
    context.selenium.find_element_by_xpath(f"//select[@name='user']/option[text()='elon']").click()
    context.selenium.find_element_by_name('_save').click()
    context.test.assertEquals("Select product to change | Django site admin", context.selenium.title)
