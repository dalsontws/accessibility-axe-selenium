from textwrap import wrap
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from axe_selenium_python import Axe
from selenium.common import exceptions
import time
import pymsgbox
import numpy as np
import pytest


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
    count_passes = 0
    count_incomplete = 0

    count_max = 0
    violations_arr = []
    url_arr = []
    for link in full_set:
        print(link)
        driver.get(link)

        axe = Axe(driver)
        # option = {'rules': {'color-contrast': {'enabled': 'false'},
        #                     'valid-lang': {'enabled': 'false'}}}
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

        url = results['url']
        # TODO: Can use dict for violations and url array, using array now for simplicity/pyplot
        violations_arr = np.append(
            violations_arr, len(results['violations']))

        url_arr = np.append(url_arr, url)

        if (len(results['violations']) > count_max):
            count_max = len(results['violations'])
            max_url = url

        count_passes += len(results['passes'])
        count_incomplete += len(results['incomplete'])

        # print(type(results))
        # print(results.get('violations').count("critical"))

        # print('violations: ', count_violations)
        # print('critical violations: ', count_critical)

        full_json[url] = results
        print("done")
    print(sum(violations_arr))
    count_arr = [count_incomplete, sum(violations_arr), count_passes]
    print('Number of violations: ', sum(violations_arr))
    return full_json, violations_arr, url_arr, max_url, count_arr


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

# full_set=remove_invalid(full_set)

full_json, violations_arr, url_arr, max_url, count_arr = save_as_json(
    full_set, full_json)

json_save_path = './data/cpf_test.json'
# json_save_path = './data/a11y_test1.json'
axe.write_results(full_json, json_save_path)

driver.close()
driver.quit()
time_taken = (time.time() - start_time)
# pymsgbox.alert(
#     "Please refer to: " + json_save_path + " for the full violations log.\n " +
#     "Time taken: %s seconds" % time_taken + "\n"
#     "Number of violations:" + str(sum(violations_arr)) + "\n"
#     "Webpage with most violations:" + max_url,
#     'Completion Box')

root = tk.Tk()
root.wm_title("title")

fig = Figure(figsize=(10, 10), dpi=100)
labels = 'Passes', 'Violations', 'Incomplete'
sizes = count_arr
explode = (0, 0.1, 0)

ax1 = fig.add_subplot(223)

ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)


# max_url = 'https://www.cpf.gov.sg/eSvc/Web/Miscellaneous/Cashier/ECashierHomepage'
ax3 = fig.add_subplot(211)
table_vals = []
i = 0

table_vals.append(['No. of Violations', str(int(sum(violations_arr)))])
table_vals.append(['Most Violations', max_url])
table_vals.append(['Time taken:', "%.1f" % time_taken + "s"])
table_vals.append(['Full log:', json_save_path])


# Draw table
the_table = ax3.table(cellText=table_vals,
                      colWidths=[0.07, 0.3],
                      rowLabels=None,
                      colLabels=None,
                      loc='center')
the_table.auto_set_font_size(False)
the_table.set_fontsize(10)
the_table.scale(3, 3)

ax3.tick_params(axis='x', which='both', bottom=False,
                top=False, labelbottom=False)
ax3.tick_params(axis='y', which='both', right=False,
                left=False, labelleft=False)
for pos in ['right', 'top', 'bottom', 'left']:
    ax3.spines[pos].set_visible(False)


j = 1
labels = []
for l in url_arr:
    labels.append(j)
    j = j+1
violations = violations_arr

ax2 = fig.add_subplot(224)

ax2.bar(labels, violations, align='center', alpha=0.5, tick_label=labels)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

tk.mainloop()


print("Test Completed")
