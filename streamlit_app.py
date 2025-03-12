# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title("Customize your smoothie! :cup_with_straw:")
st.write(
    f"""Choose the fruit you want in your custom smoothie!
    """
)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)



name_on_order = st.text_input('', '', 25, placeholder='Name')

ingredients_list = st.multiselect(
    'Choose up to five ingredients:',
    my_dataframe, 
    max_selections=5)



if ingredients_list:
    ingredients_str = ""
    for fruit in ingredients_list:
        st.subheader(fruit + ' Nutrition info')
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')                                                                     
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

        ingredients_str += fruit + ' '
    st.write(ingredients_str)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
            values ('""" + ingredients_str+ """','""" + name_on_order + """')"""

    time_to_insert = st.button('Submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


