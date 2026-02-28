import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are a healthcare AI assistant.
You ONLY answer questions related to Polycystic Ovary Syndrome(PCOS),healthcare, medicine, biology, or public health.
If a user asks anything outside healthcare, reply:
"I'm sorry, I can only answer healthcare-related questions."
Never answer non-healthcare topics."""
# -------- System Prompt --------

def main():
    if not st.session_state.get("authenticated") or not st.session_state.get("name"):
         st.warning("Please login back to access the POCS detection system")
         st.stop()
        # -------- Setup --------
    st.title("🤖 PCOS Chatbot")

# -------- Initialize Chat --------
    if "chat" not in st.session_state:
            model = genai.GenerativeModel("gemini-2.5-flash-lite",system_instruction=SYSTEM_PROMPT)
            st.session_state.chat = model.start_chat(history=[])

# -------- Display History --------
    for msg in st.session_state.chat.history:
        with st.chat_message(msg.role):
             st.markdown(msg.parts[0].text)

# -------- User Input --------
    user_input = st.chat_input("Ask a healthcare question...")

    if user_input:
        with st.chat_message("user"):
             st.markdown(user_input)

        response = st.session_state.chat.send_message(user_input)

        with st.chat_message("assistant"):
             st.markdown(response.text)

# -------- Clear Chat --------
    if st.sidebar.button("Clear Chat"):
        st.session_state.chat = genai.GenerativeModel("gemini-2.5-flash-lite",system_instruction=SYSTEM_PROMPT).start_chat(history=[])
        st.rerun()
if __name__ == "__main__":
    main()



