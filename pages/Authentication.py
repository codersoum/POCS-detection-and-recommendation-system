import streamlit as st
import csv
import pathlib
file_path=pathlib.Path(__file__).parent/"user.csv"
def main():
    st.title("Authentication Page")
    st.header("Please log in to access the PCOS detection and lifestyle recommendation system")
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if not st.session_state.authenticated:
        name = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Log In"):
            file_=""
            with open(file_path, 'r') as file:  
                reader=csv.DictReader(file)
                for row in reader:
                    if row['name']==name:
                        file_=row['password']
                        break
            if password == file_:
                st.session_state.authenticated = True
                st.success("Logged in successfully!")
                st.session_state.name = name
                st.session_state.password = password
            else:
                st.error("Invalid username or password.")
    if st.session_state.authenticated:
        if st.button("Proceed to PCOS Detection System"):
            st.switch_page("pages/PCOS detection.py")
        if st.button("Log Out"):
            st.session_state.authenticated = False
            st.session_state.name=""
            st.session_state.password=""
            st.success("Logged out successfully.")
            st.stop()
if __name__=="__main__":
    main()
    


    


