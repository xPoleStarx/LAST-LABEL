import pandas as pd

df = pd.read_csv('ml_fruit.csv')

df['fruit'] = 'cherry'

df.to_csv('ml_fruit_updated.csv', index=False)