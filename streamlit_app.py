# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    "Choose the fruits you want in your custom Smoothie"
)
st.write(
    f"""Replace the code in this example app with your own code! And if you're new to Streamlit, here are some helpful links:

    • :page_with_curl: [Streamlit open source documentation]({helpful_links[0]})
    • :snow: [Streamlit in Snowflake documentation]({helpful_links[1]}) 
    • :books: [Demo repo with templates]({helpful_links[2]})
    • :memo: [Streamlit in Snowflake release notes]({helpful_links[3]})
    """
)

name_on_order = st.text_input("Name on Smoothie :")
st.write("The name on your Smoothie will be:", name_on_order)


# import streamlit as st (Duplicate)
option = st.selectbox(
    "What is your favorite fruits",
    ("Banana", "Strawberries", "Peaches"),
)

st.write("Your favorite fruit is:", option)


# from database table

cnx = st.connection("snowflake")
session = cnx.session()
# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# my_dataframe = session.table("smoothies.public.fruit_options")

import streamlit as st

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients"
    , my_dataframe
    , max_selections=5
)

# List Type
# st.write(ingredients_list)
# st.text(ingredients_list)
# st.dataframe(data=my_dataframe, use_container_width=True)

#
# move the line
import requests

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)
    
    # convert the list to a string
    ingredients_string = ''

    # FOR LOOP
    for fruit_chosen in ingredients_list:
        # ingredients_string += fruit_chosen
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Inoformation')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        # The += operator means "add this to what is already in the variable" so each time the FOR Loop is repeated
    st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+ """')"""
    st.write(my_insert_stmt)
    # st.stop()

    # Inserted Repeat data
    #if ingredients_string:
    #    session.sql(my_insert_stmt).collect()
    #    st.success('Your Smoothie is ordered!', icon="✅")
    
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

# New Section to display smoothiefroot nutrition information
# import requests
# smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response)
# st.text(smoothiefroot_response.json())
# sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)



