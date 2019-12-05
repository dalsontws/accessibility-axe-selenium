from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from axe_selenium_python import Axe
from selenium.common import exceptions


def get_all_links():
    invalid_links = ['twitter', 'instagram', 'facebook',
                     'youtube']
    fullSet = set()

    list = driver.find_elements_by_tag_name("a")
    for link in list:
        fullLink = str(link.get_attribute("href"))
        if any(substring in fullLink for substring in invalid_links):
            break

        fullSet.add(fullLink)
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
    full_set.remove("None")
    full_set.remove("javascript:;")
    return full_set


def save_as_json(full_set, full_json):

    for link in full_set:
        driver = webdriver.Chrome()
        driver.get(link)
        axe = Axe(driver)
        # Inject axe-core javascript into page.
        axe.inject()
        # Run axe accessibility checks.
        print(link)
        results = axe.run()
        if (results is None):
            break

        url = results['url']
        full_json[url] = results
        print("done")
    return full_json


# Initialise driver
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.cpf.gov.sg/members")
axe = Axe(driver)

full_json = dict()
list = driver.find_elements_by_tag_name("a")

full_set = get_all_links()
full_set = remove_invalid(full_set)

full_json = save_as_json(full_set, full_json)

axe.write_results(full_json, 'a11y_full3.json')
driver.close()
driver.quit()

print("Test Completed")
