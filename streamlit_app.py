 # Import Python packages
import streamlit as st
from snowflake.snowpark.functions import col,when_matched

# Write directly to the app
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("""
Choose the fruits you want in your custom Smoothie!
""")

# Input for smoothie name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Get the active Snowflake session
cnx = st.connection("snowflake")
session = cnx.session

# Load fruit options from Snowflake table
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Multi-select ingredients (up to 5)
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
    
)

if ingredients_list:
    # Create ingredient string from selections
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # Prepare SQL insert statement
    my_insert_stmt = """
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('""" + ingredients_string + """','""" + name_on_order + """')
    """

    # Submit button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        # Execute insert statement in Snowflake
        session.sql(my_insert_stmt).collect()
        st.success(f"✅ Your Smoothie is ordered, {name_on_order}!")
    
   
