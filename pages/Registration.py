import streamlit as st
import csv
import os
import pathlib
file_path=pathlib.Path(__file__).parent/"user.csv"
def user_exists(email):
    if not os.path.exists(file_path):
        return False
    with open(file_path,'r')as file:
        reader=csv.DictReader(file)
        for row in reader:
            if row['email']==email:
                return True
    return False

def save_user_details(name,email,password):
    with open(file_path,'a')as file:
        fieldnames=['name','email','password'] 
        writer=csv.DictWriter(file,fieldnames=fieldnames)
        if file.tell()==0:
            writer.writeheader()
        writer.writerow({'name':name,'email':email,'password':password})
    st.session_state.file_path=file_path

def main():
    try:
        st.title("Create an Account")
        st.subheader("Register as a new user to the applcation")
        with st.form("registration_form"):
            name=st.text_input("Enter your full name")
            email=st.text_input("Enter your email address")
            password=st.text_input("Create a password",type="password")
            confirm=st.text_input("Confirm your password",type="password")
            submit=st.form_submit_button("Register")
        if submit:
            if not name.strip() or not email.strip() or not password.strip() or not confirm.strip():
                st.error("All fields are required !!")
            elif password!=confirm:
                st.error("Passwords do not match. Please try again.")
            elif len(password)<6:
                st.error("Password must be at least 6 characters long")
            elif "@" not in email or "." not in email:
                st.error("Please enter a valid email address")
            elif user_exists(email):
                  st.error("An account with this email already exists. Please use a different email.")
            else:
                save_user_details(name,email,password)
                st.success("Registration successful! You can now log in to the application.")
    except Exception as e:
         st.write(e)
if __name__=="__main__":
	main()
         
        
