import streamlit as st
import requests
import time

BACKEND_URL = "http://localhost:8000"

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Chatbot", layout="wide")

# Sidebar Navigation
with st.sidebar:
    selected = st.selectbox("Navigation", ["Chat", "Upload Documents"])

# Chat Section
if selected == "Chat":
    st.title("🤖 Document Chatbot")
    
    # Display chat history
    for chat in st.session_state.chat_history:
        st.markdown(f"**You:** {chat['question']}")
        if 'answer' in chat:
            st.markdown(f"**Bot:** {chat['answer']}")
            with st.expander("Citations"):
                for citation in chat.get("citations", []):
                    st.markdown(f"- `{citation['id']}` | Page: `{citation.get('page', '?')}` | Score: `{round(citation['score'], 2)}`")
        else:
            st.markdown(f"**Bot:** 🤖 Thinking...")
        st.markdown("---")

    # Input box for new question
    user_input = st.chat_input("Ask something about your documents...")

    if user_input:
        # Add user input to chat history
        st.session_state.chat_history.append({"question": user_input})

        # Show thinking message
        st.markdown(f"**You:** {user_input}")
        thinking_msg = st.markdown("**Bot:** 🤖 Thinking...")

        # Send request to backend
        try:
            payload = {"question": user_input}
            response = requests.post(f"{BACKEND_URL}/query/", json=payload)
            result = response.json()

            # Update thinking message with actual answer
            thinking_msg.empty()
            st.session_state.chat_history[-1]["answer"] = result.get("answer", "Not found")
            st.session_state.chat_history[-1]["citations"] = result.get("citations", [])

            # Rerun to show updated chat
            st.rerun()
        except Exception as e:
            thinking_msg.empty()
            st.error(f"Query failed: {e}")

# Upload Section
elif selected == "Upload Documents":
    st.title("📄 Upload Documents")
    uploaded_files = st.file_uploader(
        "Select one or more files (PDF, DOCX, Image)", 
        type=["pdf", "docx", "png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )
    if uploaded_files:
        for file in uploaded_files:
            files = {"file": (file.name, file.getvalue(), file.type)}
            response = requests.post(f"{BACKEND_URL}/upload/", files=files)
        st.success(f"{len(uploaded_files)} files uploaded successfully!")