import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from axe_selenium_python import Axe
from selenium.common import exceptions
import time
import pymsgbox
import numpy as np


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
    # count_violations = 0
    count_critical = 0
    count_max = 0
    violations_arr = []
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

        # count_violations += len(results['violations'])

        # TODO: Can use dict for violations and url array, using array now for simplicity/pyplot
        violations_arr = np.append(
            violations_arr, len(results['violations']))

        url_arr = np.append(url_arr, results['url'])

        if (len(results['violations']) > count_max):
            count_max = len(results['violations'])
            max_url = results['url']

        # count_critical += len(results.get(['violations']
        #                                   ['impact']) == 'critical')
        # print(type(results))
        # print(results.get('violations').count("critical"))

        # print('violations: ', count_violations)
        # print('critical violations: ', count_critical)

        url = results['url']
        full_json[url] = results
        print("done")
    print(sum(violations_arr))
    print('Number of violations: ', sum(violations_arr))
    return full_json, count_violations, max_url


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

full_json, count_violations, max_url = save_as_json(full_set, full_json)

json_save_path = './data/cpf_test.json'
axe.write_results(full_json, json_save_path)

# print('Please refer to: "', json_save_path, '" for the full violations log.')
# print('Time taken: %s seconds' % (time.time() - start_time))
driver.close()
driver.quit()

pymsgbox.alert(
    "Please refer to: " + json_save_path + " for the full violations log.\n " +
    "Time taken: %s seconds" % (time.time() - start_time) + "\n"
    "Number of violations:" + str(count_violations) + "\n"
    "Webpage with most violations:" + max_url,
    'Completion Box')


print("Test Completed")
