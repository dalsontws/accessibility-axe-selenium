import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

root = tk.Tk()
root.wm_title("title")

fig = Figure(figsize=(10, 10), dpi=100)
labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]
explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

ax1 = fig.add_subplot(223)
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)

ax2 = fig.add_subplot(224)

objects = ['Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp']
objects2 = [['Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp']]
# y_pos = np.arange(len(objects))
performance = [10, 8, 6, 4, 2, 1]

ax3 = fig.add_subplot(221)
columns = ("column")
ax3.table(cellText=objects2,
          colLabels=columns,
          loc='bottom')


ax2.bar(objects, performance, align='center',
        alpha=0.5, tick_label=objects)
ax2.legend(objects)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

tk.mainloop()

# import easygui

# easygui.msgbox(
#     "Please refer to: for the full violations log.\n " +
#     "Time taken: %s seconds\n"
#     "Number of violations:",
#     'Completion Box')


# root = tk.Tk()
# w = tk.Label(root, text='GeeksForGeeks.org!')
# w.pack()
# root.mainloop()
