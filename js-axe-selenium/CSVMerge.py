import pandas as pd
from bokeh.plotting import figure, show
from bokeh.io import show, output_notebook, output_file
from math import pi
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
import panel as pn
pn.extension()


data = pd.read_csv('jug.csv')
score = pd.read_csv('score.csv')


result = pd.merge(data,
                  score[['Volation Type','Govtech Priority','WCAG Mapping']],
                  on='Volation Type',
                  how='left')
df = pd.DataFrame(result)


df.sort_values(by=['URL','Govtech Priority'], inplace=True, ascending=False)
h=df[df.URL!='URL']
devtable = h[h.URL!='Failed to inject axe-core into one of the iframes!']
devtable.to_csv('new.csv')

g=devtable.iloc[:,0]
k=pd.DataFrame(g)
l =k.drop_duplicates()
urllist = l["URL"].tolist()
# print(urllist)


urldict = {}

for i in range(len(urllist)):
    urldict[i] = urllist[i]


# print(urldict)

urlno = list(urldict.keys())


for i in range(len(urlno)):
    urlno[i] = str(urlno[i])

# print(urlno)

criticalno = []
seriousno = []
moderateno = []
minorno = []

impact = ["critical", "serious", "moderate", "minor"]

for i in range(len(urllist)):
    url = df[df.URL == urllist[i]]
    criticalno.append(len(url[url['Impact'] == 'critical']))
    seriousno.append(len(url[url['Impact'] == 'serious']))
    moderateno.append(len(url[url['Impact'] == 'moderate']))
    minorno.append(len(url[url['Impact'] == 'minor']))



output_file("Summary Report.html")


impact = ["critical", "serious", "moderate", "minor"]
colors = ["#3f54b4","#6096fd", "#aab6fb","#787ff6"]

data = {'urlno' : urlno}
data["critical"]=criticalno
data["serious"]=seriousno
data["moderate"]=moderateno
data["minor"]=minorno
# print(data)

p = figure(x_range=urlno, plot_height=350, title="Violation Count by Website",
           toolbar_location="above", tools="hover,pan,wheel_zoom,reset,save", tooltips="@$name $name issue(s) found")

p.vbar_stack(impact, x='urlno', width=0.9, color=colors, source=data,
             legend_label=impact)

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.xaxis.axis_label = 'Page Number'
p.yaxis.axis_label = 'Number of Violations'
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "horizontal"


legendtable = pd.DataFrame.from_dict(urldict,orient='index')
legend = legendtable.rename(columns={0: 'URL'})
# def make_clickable(val):
#     return '<a href="{}">{}</a>'.format(val,val)
#
# p2=legend.style.format(make_clickable)

impact = devtable.groupby('Impact').size()
piechart = impact.to_dict()

data = pd.Series(piechart).reset_index(name='value').rename(columns={'index':'country'})
data['angle'] = data['value']/data['value'].sum() * 2*pi
data['color'] = Category20c[len(piechart)]

p3 = figure(plot_height=350, title="Violation Severity Breakdown", toolbar_location=None,
           tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))

p3.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='country', source=data)


p3.axis.axis_label=None
p3.axis.visible=False
p3.grid.grid_line_color = None

typelist = devtable.groupby('Volation Type').size()
types = typelist.to_dict()
vtypelist = pd.DataFrame.from_dict(types,orient='index')

violationstable = vtypelist.rename(columns={0: 'Most Common Violation Types'})
violationstable.sort_values(by=['Most Common Violation Types'], inplace=True, ascending=False)

combine = pn.Column(p,legend)
combinecolumn = pn.Column(p3,violationstable)
pages = pn.Tabs(('Analysis by Website',combine),('Analysis by Type',combinecolumn))
# combinerow = pn.Row(combine,combinecolumn)
pn.Tabs(('PM/PO',pages),('Developers',devtable)).show()

