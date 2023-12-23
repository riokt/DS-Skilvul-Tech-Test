import streamlit as st
import pandas as pd
from recommender import get_recommendation

# Set the page configuration
st.set_page_config(page_title="Terra Store Recommendation System", page_icon="✅")

# Set the title and font size
st.image("header.png", use_column_width=True,)
st.markdown("<span style='font-size: 8px;'> Image source: https://depositphotos.com/editorial/interior-of-the-electronics-shop-m-video-in-samara-russia-63829565.html </span>")
st.subheader("Please put the customer ID and number of recommendation")
customer_id = st.number_input("Customer ID", value=0, step=1)
n = st.number_input("Number of Recommendation", value=10, step=1)

# Button to process the video
if st.button("Get Recommendation"):    
    df_recoms = get_recommendation(cust_id=customer_id, n=n)
    if isinstance(df_recoms, str):
        st.error(df_recoms)
    else:
        for idx, recom in df_recoms.iterrows():
            st.markdown(
                f"<span style='font-size: 16px;'>#{idx} {recom.recommend_product_id}. </span>"
                f"<span style='font-size: 10px;'>*Based on buying history of product id {recom.history_product_id}, </span>"
                f"<span style='font-size: 10px;'>{recom.recency.years} years {recom.recency.months} months {recom.recency.days} days ago</span>",
                unsafe_allow_html=True
            )



