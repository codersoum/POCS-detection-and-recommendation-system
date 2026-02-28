import streamlit as st
st.title("Welcome to the PCOS Detection and Lifestyle Recommendation System")
st.write("This application helps in detecting Polycystic Ovary Syndrome (PCOS) and provides lifestyle recommendations based on the detection results.")
col1,col2=st.columns(2,border=True)
with col1 :
    if st.button("Go to Authentication Page"):
        st.switch_page("pages/Authentication.py")
    st.write("Please log in to access the PCOS detection and lifestyle recommendation features.")
with col2:
    if st.button("Go to Registration Page"):
        st.switch_page("pages/Registration.py")
    st.write("If you don't have an account, please create an account .")
st.write("Once logged in, you will be able to use the PCOS detection system and receive personalized lifestyle recommendations.")

