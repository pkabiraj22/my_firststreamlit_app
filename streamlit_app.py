import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header(' Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

# Display the table on the page.
fruits_to_show = my_fruit_list.loc[fruits_selected]


streamlit.dataframe(fruits_to_show)

#new section to get advice from Fruityvice
streamlit.header("Fruityvice Fruit Advice!")

def get_fruityvice_data(fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# write your own comment - Normalize semi-structured JSON data into a flat table 
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - display the data
   streamlit.dataframe(fruityvice_normalized)
   return fruityvice_normalized

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
#streamlit.write('The user entered ', fruit_choice)
  if not fruit_choice:
    streamlit.error('Please select fruit for information')
  else:
      back_from_func = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_func)
except URLerror as e:
   streamlit.error()
#dont run past any thing 



streamlit.header("The fruit load list Contains:")
#Snowflake related functions
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
      return my_cur.fetchall()
      
#add button to load fruit
if streamlit.button('Get Fruit Load List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
   my_data_row = get_fruit_load_list()
#streamlit.header("The fruit load list Contains:")
   streamlit.dataframe(my_data_row)


# Allow end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
   with  with my_cnx.cursor() as my_cur:
      my_cur.execute("Insert into fruit_load_list values ('from streamlit')")
      return "Thanks for Adding" + new_fruit
   
      
      
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function = insert_row_snowflake(add_my_fruit)
   streamlit.text(back_from_function)

