import pandas as pd
import json

openfile = open('python-axe-selenium/data/demo_test.json')
jsondata = json.load(openfile)
print(type(jsondata))
df = pd.DataFrame.from_dict(jsondata)

openfile.close()
print(df)

df.to_csv('test_to_csv.csv')
