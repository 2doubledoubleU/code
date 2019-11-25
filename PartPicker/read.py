import pandas as pd
import ast

data = pd.read_csv("test.csv") 

#example dirty code for searching for manufacturer part number Ford New Holland 336728 which in this case is https://www.malpasonline.co.uk/itemdetails/itemdetails.aspx?ItemNumber=102655

for row in data.itertuples():
	colValue = ast.literal_eval(row[5])
	if (colValue) and ('Ford New Holland' in colValue) and ('336728' in colValue['Ford New Holland']):
		print(row[1])