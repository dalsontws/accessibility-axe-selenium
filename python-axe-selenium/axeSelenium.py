# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# import tkinter as tk
from selenium import webdriver
from axe_selenium_python import Axe

from scipy import stats
import time
import numpy as np
# from Naked.toolshed.shell import execute_js


def get_user_input():
    input_list = []
    print()
    print("# -------------------- Start URL Input -------------------- #")
    print('Enter a blank character if there are no more links')
    while True:
        input_url = input('Enter URL: ')
        if (input_url == ''):
            break
        if ('http' not in input_url):
            print('Please enter a valid URL')
            continue
        input_list.append(input_url)
    # print(input_list)
    print("# --------------------- End URL Input --------------------- #")
    print()
    return(input_list)


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        if pct > 7:
            return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)
        else:
            return ''
    return my_autopct


def get_all_links(list_of_urls):
    fullSet = set()
    invalid_links = ['twitter', 'instagram', 'facebook',
                     'youtube', 'areyouready', 'void(0)']
    for url in list_of_urls:
        fullSet.add(url)
        driver.get(url)
        url_list = driver.find_elements_by_tag_name("a")
        for link in url_list:
            fullLink = str(link.get_attribute("href"))
            # print(fullLink)
            if any(substring in fullLink for substring in invalid_links):
                break

            fullSet.add(fullLink)

    # fullSet.add('https://www.cpf.gov.sg/Members/Schemes')

    # ------- LocalHost Testing ------- #
    # fullSet.add('http://127.0.0.1:8000/about/')
    # fullSet.add('http://127.0.0.1:8000/contact/')
    # ------- LocalHost Testing ------- #

    return fullSet


def remove_invalid(whole_set):
    # Removing possible special cases
    # fix later
    if ("" in whole_set):
        whole_set.remove("")
    if ("None" in whole_set):
        whole_set.remove("None")
    if ("javascript:;" in whole_set):
        whole_set.remove("javascript:;")
    if ("https://www.gov.sg/" in whole_set):
        whole_set.remove("https://www.gov.sg/")
    if ("https://null/common/Lists/CPFPages/DispForm.aspx?ID=239" in whole_set):
        whole_set.remove(
            "https://null/common/Lists/CPFPages/DispForm.aspx?ID=239")
    if ("https://www.cpf.gov.sg/members" in whole_set):
        whole_set.remove("https://www.cpf.gov.sg/members")
    if ("https://www.cpf.gov.sg/members#" in whole_set):
        whole_set.remove("https://www.cpf.gov.sg/members#")
    if ("https://www.cpf.gov.sg/Members/Schemes#" in whole_set):
        whole_set.remove("https://www.cpf.gov.sg/Members/Schemes#")
    if ("https://icaeservices.ica.gov.sg/ipevp/web/evp/enquire-status-make-payment/status-enquiry" in whole_set):
        whole_set.remove(
            "https://icaeservices.ica.gov.sg/ipevp/web/evp/enquire-status-make-payment/status-enquirygit")
    if ("https://www.onemotoring.com.sg/content/onemotoring/home/digitalservices/buy-e-day-licence.html" in whole_set):
        whole_set.remove(
            "https://www.onemotoring.com.sg/content/onemotoring/home/digitalservices/buy-e-day-licence.html")
    if ("https://www.cpf.gov.sg/eSvc/Web/Miscellaneous/ContributionCalculator/Index?isFirstAndSecondYear=0&isMember=1" in whole_set):
        whole_set.remove(
            "https://www.cpf.gov.sg/eSvc/Web/Miscellaneous/ContributionCalculator/Index?isFirstAndSecondYear=0&isMember=1")
    return whole_set


def save_as_json(final_set, final_json):
    count_passes = 0
    count_incomplete = 0
    count_max = 0
    violations_array = []
    url_array = []

    # -------- Python Selenium -------- #
    for link in final_set:
        print(link)
        driver.get(link)

        axe = Axe(driver)

        # try options
        # full_options = { 'xpath : True }

        # Inject axe-core javascript into page.
        axe.inject()
        # Run axe accessibility checks.
        try:
            results = axe.run()
        except:
            break
            # driver.get(link)
            # axe=Axe(driver)
            # results=axe.run()

        if (results is None):
            break

        url = results['url']
    # -------- Python Selenium -------- #

     # TODO: Can use dict for violations and url array, using array now for simplicity/pyplot
        violations_array = np.append(
            violations_array, len(results['violations']))

        url_array = np.append(url_array, url)

        if (len(results['violations']) > count_max):
            count_max = len(results['violations'])
            max_url_name = url

        count_passes += len(results['passes'])
        count_incomplete += len(results['incomplete'])
        # print(len(results['incomplete']))

        # print(type(results))
        # print(results.get('violations').count("critical"))

        # print('violations: ', count_violations)
        # print('critical violations: ', count_critical)

        final_json[url] = results
        print("done")

        count_array = [count_incomplete, sum(violations_array), count_passes]

    print('Number of violations: ', sum(violations_array))
    return final_json, violations_array, url_array, max_url_name, count_array


def print_stats(count_array, violations_array, url_array, des_array, max_url_name, save_path):
    print(['No. of Web Pages', len(url_array)])
    print(['No. of Violations', str(int(sum(violations_array)))])
    print(['Most Common Violation', str(stats.mode(des_array)[0])])
    print(['No. of Passes', str(count_array[0])])
    print(['Most Violations', max_url_name])
    print(['Time taken:', "%.1f" % time_taken + "s"])
    print(['Full log:', save_path])

# def plot_visualisations(count_array, violations_array, url_array, des_array, max_url_name, save_path):
#     root = tk.Tk()
#     root.wm_title("title")

#     fig = Figure(figsize = (10, 10), dpi = 100)
#     labels = 'Passes', 'Violations', 'Incomplete'
#     sizes = count_array
#     explode = (0, 0.2, 0)

#     ax1=fig.add_subplot(223)

#     ax1.pie(sizes, explode = explode, labels = labels, autopct = make_autopct(sizes),
#             textprops = {'fontsize': 10}, shadow = True, startangle = 90, radius = 1.5)

#     ax3 = fig.add_subplot(211)
#     table_vals = []

#     table_vals.append(['No. of Web Pages', len(url_array)])
#     table_vals.append(['No. of Violations', str(int(sum(violations_array)))])
#     table_vals.append(['Most Common Violation', str(stats.mode(des_array)[0])])
#     table_vals.append(['No. of Passes', str(count_array[0])])
#     table_vals.append(['Most Violations', max_url_name])
#     table_vals.append(['Time taken:', "%.1f" % time_taken + "s"])
#     table_vals.append(['Full log:', save_path])


#     print(['No. of Web Pages', len(url_array)])
#     print(['No. of Violations', str(int(sum(violations_array)))])
#     print(['Most Common Violation', str(stats.mode(des_array)[0])])
#     print(['No. of Passes', str(count_array[0])])
#     print(['Most Violations', max_url_name])
#     print(['Time taken:', "%.1f" % time_taken + "s"])
#     print(['Full log:', save_path])

#     # Draw table
#     the_table = ax3.table(cellText=table_vals,
#                           colWidths=[0.09, 0.3],
#                           rowLabels=None,
#                           colLabels=None,
#                           loc='center')
#     the_table.auto_set_font_size(False)
#     the_table.set_fontsize(10)
#     the_table.scale(3, 3)

#     ax3.tick_params(axis = 'x', which = 'both', bottom = False,
#                     top=False, labelbottom=False)
#     ax3.tick_params(axis='y', which='both', right=False,
#                     left=False, labelleft=False)
#     for pos in ['right', 'top', 'bottom', 'left']:
#         ax3.spines[pos].set_visible(False)

#     j = 1
#     labels = []
#     for l in url_arr:
#         labels.append(j)
#         j = j+1
#     violations = violations_array

#     ax2 = fig.add_subplot(224)

#     ax2.bar(labels, violations, align='center', alpha=0.5, tick_label=labels)

#     canvas = FigureCanvasTkAgg(fig, master=root)
#     canvas.draw()
#     canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#     toolbar = NavigationToolbar2Tk(canvas, root)
#     toolbar.update()
#     canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#     tk.mainloop()


start_time = time.time()
# Initialise driver

input_url_list = get_user_input()

# -------- For Chrome -------- #
driver = webdriver.Chrome()
driver.maximize_window()
# -------- For Chrome -------- #

# -------- Internet Explorer -------- #
# cap = DesiredCapabilities().INTERNETEXPLORER
# cap['ignoreZoomSetting'] = True
# driver = webdriver.Ie(capabilities=cap)
# -------- Internet Explorer -------- #


# main_url = "https://www.healthhub.sg/a-z"

# --------- SP Log In -------- #
main_url = "https://www.google.com"
# main_url = "https://saml.singpass.gov.sg/"
driver.get(main_url)
# --------- SP Log In -------- #

# -------- Add base URLs -------- #
# urls = {"https://www.cpf.gov.sg/members"}
# "https://www.mycareersfuture.sg/search/"}

axe = Axe(driver)

# Thread sleep
# time.sleep(50)

full_json = dict()

full_set = get_all_links(input_url_list)
# full_set = get_all_links(urls)

full_set = remove_invalid(full_set)

full_json, violations_arr, url_arr, max_url, count_arr = save_as_json(
    full_set, full_json)


json_save_path = './data/demo_test.json'
axe.write_results(full_json, json_save_path)

des_arr = []
for items in full_json.values():
    # print(items['violations'])
    for item in items['violations']:
        des_arr.append(item['description'])


driver.close()
driver.quit()
time_taken = (time.time() - start_time)

# plot_visualisations(count_arr, violations_arr, url_arr, des_arr,
#                     max_url, json_save_path)

print_stats(count_arr, violations_arr, url_arr, des_arr,
            max_url, json_save_path)

print("Test Completed")
