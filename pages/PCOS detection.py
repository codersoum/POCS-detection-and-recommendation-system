import streamlit as st
import numpy as np
from  reportlab.platypus import SimpleDocTemplate ,Table,TableStyle,Paragraph,Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
import pickle as pk
import datetime as date
import pathlib
import csv
file_path=pathlib.Path(__file__).parent/"user.csv"
element=[["Parameter","Value"]]
true_data=["Normal Range","3-10","3-10","21-35","N(No significant weight gain)","1.0-4.0","N(No excessive hair)","N(Absent)"]
if "predict_report" not in st.session_state:
    st.session_state.predict_report=False
if "prediction_done" not in st.session_state:
    st.session_state.prediction_done=False
def print_report():
        pdf=SimpleDocTemplate("PCOS_Report.pdf",pagesize=letter)
        story=[]
        styles=getSampleStyleSheet()
        story.append(Paragraph("User Information",styles["Heading1"]))
        story.append(Spacer(1,12))
        story .append(Paragraph(f"Date: {date.datetime.now().strftime('%d/%m/%Y')}",styles["Normal"]))
        story.append(Paragraph(f"Name: {st.session_state.name}",styles["Normal"]))
        with open (file_path,'r') as file:
            reader=csv.DictReader(file)
            for row in reader:
                if row['password']==st.session_state.password:
                    st.session_state.email=row['email']
                    break
        story .append(Paragraph(f"Email-id:{st.session_state.email}",styles["Normal"]))
        story.append(Spacer(1,12))
        story.append(Paragraph("PCOS Detection Report",styles["Heading1"]))
        story.append(Spacer(2,12))
        for x in range(len(element)):
            element[x].append(true_data[x])
        table=Table(element,colWidths=[150,100,150],rowHeights=30)
        table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),"lightgrey"),
        ("TEXTCOLOR",(0,0),(-1,0),"black"),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,0),14),
        ("BOTTOMPADDING",(0,0),(-1,0),12),
        ("BACKGROUND",(0,1),(-1,-1),"white"),
        ("GRID",(0,0),(-1,-1),1,"black")
        ]))
        story.append(table)
        story.append(Spacer(2,12))
        if st.session_state.predict_report:
            story.append(Paragraph('<font color="red">Symptoms are  Positive for PCOS</font>',styles["Heading1"]))
        else :
            story.append(Paragraph('<font color="green">Symptoms are  Negative for PCOS</font>',styles["Heading1"]))
        pdf.build(story)
        st.success("Report generated successfully! You can download it from the sidebar.")
        st.sidebar.download_button(label="Download PCOS Report",data=open("PCOS_Report.pdf","rb"),file_name="POCS_Report.pdf",mime="text/pdf")

def main():
    if not st.session_state.get("authenticated") or not st.session_state.get("name"):
         st.warning("Please login back to access the PCOS detection system")
         st.stop()
    else:
        st.title(f"Hi {st.session_state["name"]}!:smiley:")
        st.header("Welcome to the PCOS detection and lifestyle recommendation system.")
        st.header("This application helps you identify potential symptoms of Polycystic Ovary Syndrome (PCOS) and provides personalized lifestyle recommendations to manage the condition effectively.")
        st.subheader("Please fill in the following details to get started:")
        with open('features.pkl','rb') as file:
            features=pk.load(file)
        inputs,categorical_features=[],[]
        for feature in features:
            if feature.endswith('(Y/N)'):
                categorical_features.append(feature)
        for feature in features:
            if feature in categorical_features:
                select=st.selectbox(f"Select {feature}",["Y","N"])
                element.append([feature,select])
                inp=1 if select=="Y" else 0
            else:
                inp=st.number_input(f"Enter {feature}")
                element.append([feature,inp])
            inputs.append(inp)
        if st.button("Predict PCOS"):
            X_input=np.array([inputs])
            with open('model.pkl','rb') as file:
                model=pk.load(file)
            prediction=model.predict(X_input)[0]
            if prediction==1:
                st.error("The model predicts that you may have PCOS. It is advisable to consult a healthcare professional for a comprehensive evaluation and diagnosis.")
                st.session_state.predict_report=True
            else:
                st.success("The model predicts that you are unlikely to have PCOS. However, if you experience any symptoms or have concerns, please consult a healthcare professional for further evaluation.")
                st.session_state.predict_report=False
            st.session_state.prediction_done=True
        if st.session_state.prediction_done:
            if st.button("Generate Report", disabled=not st.session_state.prediction_done):
                print_report()
        if st.session_state.predict_report:
            if st.button("Proceed to PCOS Recommendation System"):
                st.switch_page("pages/Chatbot.py")
if __name__=="__main__":
    main()