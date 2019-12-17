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


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        if pct > 7:
            return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)
        else:
            return ''
    return my_autopct


def get_all_links(urls):
    fullSet = set()
    invalid_links = ['twitter', 'instagram', 'facebook',
                     'youtube', 'areyouready']
    for url in urls:
        fullSet.add(url)
        driver.get(url)
        url_list = driver.find_elements_by_tag_name("a")
        for link in url_list:
            fullLink = str(link.get_attribute("href"))
            print(fullLink)
            if any(substring in fullLink for substring in invalid_links):
                break

            fullSet.add(fullLink)

    # fullSet.add('https://www.cpf.gov.sg/Members/Schemes')

    # ------- LocalHost Testing ------- #
    # fullSet.add('http://127.0.0.1:8000/about/')
    # fullSet.add('http://127.0.0.1:8000/contact/')
    # ------- LocalHost Testing ------- #

    return fullSet


def remove_invalid(full_set):
    # Removing possible special cases
    # fix later
    if ("None" in full_set):
        full_set.remove("None")
    if ("javascript:;" in full_set):
        full_set.remove("javascript:;")
    if ("https://www.gov.sg/" in full_set):
        full_set.remove("https://www.gov.sg/")
    if ("https://null/common/Lists/CPFPages/DispForm.aspx?ID=239" in full_set):
        full_set.remove(
            "https://null/common/Lists/CPFPages/DispForm.aspx?ID=239")
    if ("https://www.cpf.gov.sg/members" in full_set):
        full_set.remove("https://www.cpf.gov.sg/members")
    if ("https://www.cpf.gov.sg/members#" in full_set):
        full_set.remove("https://www.cpf.gov.sg/members#")
    if ("https://www.cpf.gov.sg/Members/Schemes#" in full_set):
        full_set.remove("https://www.cpf.gov.sg/Members/Schemes#")

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

        # try options
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


def plot_visualisations(count_arr, violations_arr, url_arr, max_url, json_save_path):
    root = tk.Tk()
    root.wm_title("title")

    fig = Figure(figsize=(10, 10), dpi=100)
    labels = 'Passes', 'Violations', 'Incomplete'
    sizes = count_arr
    explode = (0, 0.2, 0)

    ax1 = fig.add_subplot(223)

    ax1.pie(sizes, explode=explode, labels=labels, autopct=make_autopct(sizes),
            textprops={'fontsize': 10}, shadow=True, startangle=90, radius=1.5)

    # max_url = 'https://www.cpf.gov.sg/eSvc/Web/Miscellaneous/Cashier/ECashierHomepage'
    ax3 = fig.add_subplot(211)
    table_vals = []

    table_vals.append(['No. of Web Pages', len(url_arr)])
    table_vals.append(['No. of Violations', str(int(sum(violations_arr)))])
    table_vals.append(['No. of Passes', str(count_arr[0])])
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


start_time = time.time()
# Initialise driver


# -------- For Chrome -------- #
driver = webdriver.Chrome()
driver.maximize_window()
# -------- For Chrome -------- #

# -------- Internet Explorer -------- #
# cap = DesiredCapabilities().INTERNETEXPLORER
# cap['ignoreZoomSetting'] = True
# driver = webdriver.Ie(capabilities=cap)
# -------- Internet Explorer -------- #

# main_url = "https://www.cpf.gov.sg/members"
main_url = "https://eservices.healthhub.sg/PersonalHealth"

# -------- Add base URLs -------- #
urls = {"https://eservices.healthhub.sg/PersonalHealth"}
# "https://www.cpf.gov.sg/Members/Schemes"}
# -------- Add base URLs -------- #

driver.get(main_url)

# Thread sleep
time.sleep(60)

axe = Axe(driver)

full_json = dict()

full_set = get_all_links(urls)

full_set = remove_invalid(full_set)

full_json, violations_arr, url_arr, max_url, count_arr = save_as_json(
    full_set, full_json)

json_save_path = './data/healthhub_test.json'
axe.write_results(full_json, json_save_path)

driver.close()
driver.quit()
time_taken = (time.time() - start_time)

plot_visualisations(count_arr, violations_arr, url_arr,
                    max_url, json_save_path)


print("Test Completed")
