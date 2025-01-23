import streamlit as st
import langchain_helper

st.title("Restuarnt Name Generator")

cuisine = st.sidebar.selectbox("Pick a Cuisine", ("Indian", "Italian", "Mexican", "Arabic", "American"))

if cuisine:

    # get restaurant name, food items and clean
    response = langchain_helper.generate_restaurant_name_and_items(cuisine)

    dirty_string = response['restaurant_name']
    response['restaurant_name'] = dirty_string.strip().strip('"').replace("\\'", "'")
    st.header(response['restaurant_name'].strip())

    # cleaning food items
    menu_items = [line.split('. ', 1)[1].strip() for line in response['menu_items'].strip().split('\n')]
    st.write("**Menu Items**")

    for item in menu_items:
        st.write("-", item)

# streamlit run main.py (to run this application)