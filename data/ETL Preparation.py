ETL Pipeline Preparation
Follow the instructions below to help you create your ETL pipeline.

1. Import libraries and load datasets.
Import Python libraries
Load messages.csv into a dataframe and inspect the first few lines.
Load categories.csv into a dataframe and inspect the first few lines.
# import libraries
import pandas as pd
from sqlalchemy import create_engine
# load messages dataset
messages = pd.read_csv('disaster_messages.csv')
messages.head(5)
id	message	original	genre
0	2	Weather update - a cold front from Cuba that c...	Un front froid se retrouve sur Cuba ce matin. ...	direct
1	7	Is the Hurricane over or is it not over	Cyclone nan fini osinon li pa fini	direct
2	8	Looking for someone but no name	Patnm, di Maryani relem pou li banm nouvel li ...	direct
3	9	UN reports Leogane 80-90 destroyed. Only Hospi...	UN reports Leogane 80-90 destroyed. Only Hospi...	direct
4	12	says: west side of Haiti, rest of the country ...	facade ouest d Haiti et le reste du pays aujou...	direct
# load categories dataset
categories = pd.read_csv('disaster_categories.csv')
categories.head(5)
id	categories
0	2	related-1;request-0;offer-0;aid_related-0;medi...
1	7	related-1;request-0;offer-0;aid_related-1;medi...
2	8	related-1;request-0;offer-0;aid_related-0;medi...
3	9	related-1;request-1;offer-0;aid_related-1;medi...
4	12	related-1;request-0;offer-0;aid_related-0;medi...
print('Number of rows and columns in the messages file are: {} and {}'.format(messages.shape[0],messages.shape[1]))
print('Number of rows and columns in the categories file are: {} and {}'.format(categories.shape[0],categories.shape[1]))
Number of rows and columns in the messages file are: 26248 and 4
Number of rows and columns in the categories file are: 26248 and 2
2. Merge datasets.
Merge the messages and categories datasets using the common id
Assign this combined dataset to df, which will be cleaned in the following steps
# merge datasets
df = messages.merge(categories, on='id')
df.head(5)
id	message	original	genre	categories
0	2	Weather update - a cold front from Cuba that c...	Un front froid se retrouve sur Cuba ce matin. ...	direct	related-1;request-0;offer-0;aid_related-0;medi...
1	7	Is the Hurricane over or is it not over	Cyclone nan fini osinon li pa fini	direct	related-1;request-0;offer-0;aid_related-1;medi...
2	8	Looking for someone but no name	Patnm, di Maryani relem pou li banm nouvel li ...	direct	related-1;request-0;offer-0;aid_related-0;medi...
3	9	UN reports Leogane 80-90 destroyed. Only Hospi...	UN reports Leogane 80-90 destroyed. Only Hospi...	direct	related-1;request-1;offer-0;aid_related-1;medi...
4	12	says: west side of Haiti, rest of the country ...	facade ouest d Haiti et le reste du pays aujou...	direct	related-1;request-0;offer-0;aid_related-0;medi...
print('Number of rows and columns in the merged file are: {} and {}'.format(df.shape[0],df.shape[1]))
Number of rows and columns in the merged file are: 26386 and 5
3. Split categories into separate category columns.
Split the values in the categories column on the ; character so that each value becomes a separate column. You'll find this method very helpful! Make sure to set expand=True.
Use the first row of categories dataframe to create column names for the categories data.
Rename columns of categories with new column names.
# create a dataframe of the 36 individual category columns
categories = df['categories'].str.split(pat=';', expand=True)
categories.head(5)
0	1	2	3	4	5	6	7	8	9	...	26	27	28	29	30	31	32	33	34	35
0	related-1	request-0	offer-0	aid_related-0	medical_help-0	medical_products-0	search_and_rescue-0	security-0	military-0	child_alone-0	...	aid_centers-0	other_infrastructure-0	weather_related-0	floods-0	storm-0	fire-0	earthquake-0	cold-0	other_weather-0	direct_report-0
1	related-1	request-0	offer-0	aid_related-1	medical_help-0	medical_products-0	search_and_rescue-0	security-0	military-0	child_alone-0	...	aid_centers-0	other_infrastructure-0	weather_related-1	floods-0	storm-1	fire-0	earthquake-0	cold-0	other_weather-0	direct_report-0
2	related-1	request-0	offer-0	aid_related-0	medical_help-0	medical_products-0	search_and_rescue-0	security-0	military-0	child_alone-0	...	aid_centers-0	other_infrastructure-0	weather_related-0	floods-0	storm-0	fire-0	earthquake-0	cold-0	other_weather-0	direct_report-0
3 rows × 36 columns

# select the first row of the categories dataframe
row = categories.iloc[[1]]

# use this row to extract a list of new column names for categories.
# one way is to apply a lambda function that takes everything 
# up to the second to last character of each string with slicing
category_colnames = [category_name.split('-')[0] for category_name in row.values[0]]
print(category_colnames)
['related', 'request', 'offer', 'aid_related', 'medical_help', 'medical_products', 'search_and_rescue', 'security', 'military', 'child_alone', 'water', 'food', 'shelter', 'clothing', 'money', 'missing_people', 'refugees', 'death', 'other_aid', 'infrastructure_related', 'transport', 'buildings', 'electricity', 'tools', 'hospitals', 'shops', 'aid_centers', 'other_infrastructure', 'weather_related', 'floods', 'storm', 'fire', 'earthquake', 'cold', 'other_weather', 'direct_report']
# rename the columns of `categories`
categories.columns = category_colnames
categories.head()
related	request	offer	aid_related	medical_help	medical_products	search_and_rescue	security	military	child_alone	...	aid_centers	other_infrastructure	weather_related	floods	storm	fire	earthquake	cold	other_weather	direct_report
0	related-1	request-0	offer-0	aid_related-0	medical_help-0	medical_products-0	search_and_rescue-0	security-0	military-0	child_alone-0	...	aid_centers-0	other_infrastructure-0	weather_related-0	floods-0	storm-0	fire-0	earthquake-0	cold-0	other_weather-0	direct_report-0
1	related-1	request-0	offer-0	aid_related-1	medical_help-0	medical_products-0	search_and_rescue-0	security-0	military-0	child_alone-0	...	aid_centers-0	other_infrastructure-0	weather_related-1	floods-0	storm-1	fire-0	earthquake-0	cold-0	other_weather-0	direct_report-0
2	related-1	request-0	offer-0	aid_related-0	medical_help-0	medical_products-0	search_and_rescue-0	security-0	military-0	child_alone-0	...	aid_centers-0	other_infrastructure-0	weather_related-0	floods-0	storm-0	fire-0	earthquake-0	cold-0	other_weather-0	direct_report-0
3	related-1	request-1	offer-0	aid_related-1	medical_help-0	medical_products-1	search_and_rescue-0	security-0	military-0	child_alone-0	...	aid_centers-0	other_infrastructure-0	weather_related-0	floods-0	storm-0	fire-0	earthquake-0	cold-0	other_weather-0	direct_report-0
4	related-1	request-0	offer-0	aid_related-0	medical_help-0	medical_products-0	search_and_rescue-0	security-0	military-0	child_alone-0	...	aid_centers-0	other_infrastructure-0	weather_related-0	floods-0	storm-0	fire-0	earthquake-0	cold-0	other_weather-0	direct_report-0
5 rows × 36 columns

4. Convert category values to just numbers 0 or 1.
Iterate through the category columns in df to keep only the last character of each string (the 1 or 0). For example, related-0 becomes 0, related-1 becomes 1. Convert the string to a numeric value.
You can perform normal string actions on Pandas Series, like indexing, by including .str after the Series. You may need to first convert the Series to be of type string, which you can do with astype(str).
for column in categories:
    # set each value to be the last character of the string
    categories[column] = categories[column].astype(str).str[-1:]
    
    # convert column from string to numeric
    categories[column] = categories[column].astype(int)

categories.head(5)
related	request	offer	aid_related	medical_help	medical_products	search_and_rescue	security	military	child_alone	...	aid_centers	other_infrastructure	weather_related	floods	storm	fire	earthquake	cold	other_weather	direct_report
0	1	0	0	0	0	0	0	0	0	0	...	0	0	0	0	0	0	0	0	0	0
1	1	0	0	1	0	0	0	0	0	0	...	0	0	1	0	1	0	0	0	0	0
2	1	0	0	0	0	0	0	0	0	0	...	0	0	0	0	0	0	0	0	0	0
3	1	1	0	1	0	1	0	0	0	0	...	0	0	0	0	0	0	0	0	0	0
4	1	0	0	0	0	0	0	0	0	0	...	0	0	0	0	0	0	0	0	0	0
5 rows × 36 columns

5. Replace categories column in df with new category columns.
Drop the categories column from the df dataframe since it is no longer needed.
Concatenate df and categories data frames.
# drop the original categories column from `df`
df.drop(['categories'], axis=1, inplace=True)
df.head(5)
id	message	original	genre
0	2	Weather update - a cold front from Cuba that c...	Un front froid se retrouve sur Cuba ce matin. ...	direct
1	7	Is the Hurricane over or is it not over	Cyclone nan fini osinon li pa fini	direct
2	8	Looking for someone but no name	Patnm, di Maryani relem pou li banm nouvel li ...	direct
3	9	UN reports Leogane 80-90 destroyed. Only Hospi...	UN reports Leogane 80-90 destroyed. Only Hospi...	direct
4	12	says: west side of Haiti, rest of the country ...	facade ouest d Haiti et le reste du pays aujou...	direct
# concatenate the original dataframe with the new `categories` dataframe
df = pd.concat([df,categories], join='inner', axis=1)
df.head(5)
id	message	original	genre	related	request	offer	aid_related	medical_help	medical_products	...	aid_centers	other_infrastructure	weather_related	floods	storm	fire	earthquake	cold	other_weather	direct_report
0	2	Weather update - a cold front from Cuba that c...	Un front froid se retrouve sur Cuba ce matin. ...	direct	1	0	0	0	0	0	...	0	0	0	0	0	0	0	0	0	0
1	7	Is the Hurricane over or is it not over	Cyclone nan fini osinon li pa fini	direct	1	0	0	1	0	0	...	0	0	1	0	1	0	0	0	0	0
2	8	Looking for someone but no name	Patnm, di Maryani relem pou li banm nouvel li ...	direct	1	0	0	0	0	0	...	0	0	0	0	0	0	0	0	0	0
3	9	UN reports Leogane 80-90 destroyed. Only Hospi...	UN reports Leogane 80-90 destroyed. Only Hospi...	direct	1	1	0	1	0	1	...	0	0	0	0	0	0	0	0	0	0
4	12	says: west side of Haiti, rest of the country ...	facade ouest d Haiti et le reste du pays aujou...	direct	1	0	0	0	0	0	...	0	0	0	0	0	0	0	0	0	0
5 rows × 40 columns

6. Remove duplicates.
Check how many duplicates are in this dataset.
Drop the duplicates.
Confirm duplicates were removed.
# Check number of duplicates before removal of duplicates
print('Number of duplicates before removal are: {}'.format(sum(df.duplicated())))
Number of duplicates before removal are: 170
# Drop duplicates
df.drop_duplicates(inplace=True)
# Check number of duplicates after removal of duplicates
print('Number of duplicates after removal are: {}'.format(sum(df.duplicated())))
Number of duplicates after removal are: 0
7. Save the clean dataset into an sqlite database.
You can do this with pandas to_sql method combined with the SQLAlchemy library. Remember to import SQLAlchemy's create_engine in the first cell of this notebook to use it below.

database_filepath = "disaster_response_db.db"
engine = create_engine('sqlite:///' + database_filepath)
table_name = os.path.basename(database_filepath).replace(".db","") + "_table"
df.to_sql(table_name, engine, index=False, if_exists='replace')
8. Use this notebook to complete etl_pipeline.py
Use the template file attached in the Resources folder to write a script that runs the steps above to create a database based on new datasets specified by the user. Alternatively, you can complete etl_pipeline.py in the classroom on the Project Workspace IDE coming later.
