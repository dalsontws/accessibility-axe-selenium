import pandas as pd

data = pd.read_csv('jug.csv')
score = pd.read_csv('score.csv')


result = pd.merge(data,
                  score[['Volation Type','Govtech Priority','WCAG Mapping']],
                  on='Volation Type',
                  how='left')

result.to_csv('new.csv')
