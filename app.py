import pandas as pd
import streamlit as st
import plotly.express as px

from PIL import Image


st.set_page_config(page_title='Survery Results')
st.header('Survery Results 2021')
st.subheader('Was the tutorial helpful?')


### Load the dataframe
excel_file = 'Survey_Results.xlsx'
sheet_name = 'DATA'

df = pd.read_excel(excel_file, sheet_name=sheet_name, usecols='B:D',header=3)

df_participants = pd.read_excel(excel_file, sheet_name=sheet_name, usecols='F:G',header=3)


## st.dataframe(df) ## display the list 
## st.dataframe(df_participants) ## display the list based on departments 

## st.dataframe(df) (all the data in a excel format way)

## drop the value as null
df_participants.dropna(inplace=True)

## 1 insert slider and multiselect option
#  storage the unique value of the department and age column in a list
department = df['Department'].unique().tolist()
ages = df['Age'].unique().tolist()


## age selectiong slider
age_selection = st.slider('Age:', min_value=min(ages), max_value=max(ages), value=(min(ages),max(ages)))

## multi-selection box
department_selection = st.multiselect('Department:', department, default=department) 

# --- FILTER DATAFRAME BASED ON SELECTION
# first create a mask that will combine the data 'age' between the age selection & combine with the department selected with 'isin

mask = (df['Age'].between(*age_selection)) & (df['Department'].isin(department_selection))
# store the number of available rows result
number_of_results = df[mask].shape[0]
st.markdown(f'*Available results: {number_of_results}')

# --- GROUP the DATAFRAME ----
# group by rating and countiong the values and returing only the age column
df_grouped = df[mask].groupby(by=['Rating']).count()[['Age']]
# rename the group to display on the screen
df_grouped = df_grouped.rename(columns={'Age':'Votes'})
# reset group 
df_grouped = df_grouped.reset_index()

df_grouped

# --- PLOT the result in a bar chart

bar_chart = px.bar(df_grouped, x='Rating', y='Votes', text='Votes', color_discrete_sequence = ['#F63366']*len(df_grouped), template='plotly_white' )



st.plotly_chart(bar_chart)






st.dataframe(df)

#pie_chart = px.pie(df_participants,title='Total No. of Participants',values='Participants',names='Departments')
#st.plotly_chart(pie_chart)



## inserting images 
image = Image.open('images/survey.jpg')

st.image(image,
    caption='Keep the data',
    ## for regular size ... width=200
    use_column_width=True)


info = 'Now displaying image and dataframa in 2 columns'
st.markdown(info)

# --- Displaying image and dataframe in two columns
col1, col2 = st.beta_columns(2)
col1.image(image,
    caption='Keep the data',
    ## for regular size ... width=200
    use_column_width=True)

col2.dataframe(df[mask])  # the filtered data with the mask

pie_chart = px.pie(df_participants,title='Total No. of Participants',values='Participants',names='Departments')
st.plotly_chart(pie_chart)