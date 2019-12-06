from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from axe_selenium_python import Axe
from selenium.common import exceptions
import time
from pymsgbox import *


def get_all_links(url):
    invalid_links = ['twitter', 'instagram', 'facebook',
                     'youtube']
    fullSet = set()
    fullSet.add(url)
    list = driver.find_elements_by_tag_name("a")
    for link in list:
        fullLink = str(link.get_attribute("href"))
        if any(substring in fullLink for substring in invalid_links):
            break

        fullSet.add(fullLink)

    # fullSet.add('https://www.cpf.gov.sg/Members/Schemes')
    return fullSet


def get_nav_links():
    navSet = set()
    navbar = driver.find_elements_by_css_selector("#mainnav-4 > a")
    for link in navbar:
        fullLink = link.get_attribute("href")
        navSet.add(fullLink)
    return navSet


def remove_invalid(full_set):
    # hard-coded removal of invalid links
    # change/remove if required
    full_set.remove("None")
    full_set.remove("javascript:;")
    return full_set


def save_as_json(full_set, full_json):
    count_violations = 0
    count_critical = 0
    for link in full_set:
        print(link)
        driver.get(link)

        axe = Axe(driver)
        # Inject axe-core javascript into page.
        axe.inject()
        # Run axe accessibility checks.
        try:
            results = axe.run()
        except:
            axe = Axe(driver)
            results = axe.run()

        if (results is None):
            break

        count_violations += len(results['violations'])

        # count_critical += len(results.get(['violations']
        #                                   ['impact']) == 'critical')
        # print(type(results))
        # print(results.get('violations').count("critical"))

        # print('violations: ', count_violations)
        # print('critical violations: ', count_critical)

        url = results['url']
        full_json[url] = results
        print("done")
    print('Number of violations: ', count_violations)
    return full_json


start_time = time.time()
# Initialise driver
driver = webdriver.Chrome()
driver.maximize_window()
url = "https://www.cpf.gov.sg/members"
driver.get(url)
axe = Axe(driver)

full_json = dict()
list = driver.find_elements_by_tag_name("a")

full_set = get_all_links(url)

full_set = remove_invalid(full_set)

full_json = save_as_json(full_set, full_json)

json_save_path = './data/cpf_test.json'
axe.write_results(full_json, json_save_path)

print('Please refer to: "', json_save_path, '" for the full violations log.')
print('Time taken: %s seconds' % (time.time() - start_time))
driver.close()
driver.quit()

print("Test Completed")
