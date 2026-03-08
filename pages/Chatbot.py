import streamlit as st
import google.generativeai as genai
import os
from pages.extraction.report_extraction import parse_interpret
from dotenv import load_dotenv
load_dotenv()
# from import report_extraction
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are a healthcare AI assistant.
You ONLY answer questions related to Polycystic Ovary Syndrome(PCOS),healthcare, medicine, biology, or public health.
If a user asks anything outside healthcare, reply:
"I'm sorry, I can only answer healthcare-related questions."
Never answer non-healthcare topics."""
# -------- System Prompt --------

def main():
    if not st.session_state.get("authenticated") or not st.session_state.get("name"):
         st.warning("Please login back to access the PCOS recommendation system")
         st.stop()
        # -------- Setup --------
    st.title("🤖 PCOS Chatbot")

# -------- Initialize Chat --------
    if "chat" not in st.session_state:
            model = genai.GenerativeModel("gemini-2.5-flash-lite",system_instruction=SYSTEM_PROMPT)
            st.session_state.chat = model.start_chat(history=[])
    if "conversations" not in st.session_state:
         st.session_state.conversations=[]

# -------- Display History --------
    for message in st.session_state.conversations:
         with st.chat_message(message["role"]):
              st.markdown(message["content"])
         
# -------- User Input --------
    filename=st.file_uploader("Upload a file ",type=["pdf","text"],accept_multiple_files=False)
    interpretations=[]

    # parsing file and extract meaningful sentences .Send these sentences as prompts to model and get the response. Display the response in the chat interface.
    if  filename is not None:
        st.session_state.conversations.append({
             "role":"user",
             "content":f'Uploaded file: {filename.name}'
        })
        with st.spinner("Extracting information from the file"):
            interpretations= parse_interpret(filename)
        #with st.chat_message("user"):
        #     for lines in interpretations:
        #           st.markdown(lines)
        prompt=f'''
        You are a healthcare AI assistant specialized in PCOS.Below are the interpretations of patient {st.session_state.name}'s report, 
        '''
        for line in interpretations:
             prompt+=line+"\n"
        prompt+="""Based on the above interpretations,
        
        1.Assess the likelihood of the patient having PCOS.
        2.Describe the symptoms that the patient is facing
        3.Suggest few lifestyle recommendations
        Please provide a short and concise answer and always use 'You' to refer to the patient in your response."
        """
        response = st.session_state.chat.send_message(prompt)
        st.session_state.conversations.append({
             "role": "assistant",
             "content": response.text
        })
        with st.chat_message("assistant"):
              st.markdown(response.text)

#-------- Clear Chat --------
    if st.sidebar.button("Clear Chat"):
        st.session_state.chat = genai.GenerativeModel("gemini-2.5-flash-lite",system_instruction=SYSTEM_PROMPT).start_chat(history=[])
        st.rerun()
if __name__ == "__main__":
    main()



