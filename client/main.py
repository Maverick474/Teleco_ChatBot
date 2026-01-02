import streamlit as st
import requests
import json
from datetime import datetime
<<<<<<< HEAD
from dotenv import load_dotenv
import os 

load_dotenv()
=======
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20

# Page configuration
st.set_page_config(
    page_title="Teleco ChatBot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    
    .chat-message {
        display: flex;
        margin-bottom: 1.5rem;
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        justify-content: flex-end;
    }
    
    .assistant-message {
        justify-content: flex-start;
    }
    
    .message-content {
        max-width: 70%;
        padding: 1rem;
        border-radius: 0.75rem;
        line-height: 1.6;
    }
    
    .user-content {
        background-color: #0084ff;
        color: white;
        border-radius: 18px;
    }
    
    .assistant-content {
        background-color: #e5e5e5;
        color: #333;
        border-radius: 18px;
    }
    
    .metadata {
        font-size: 0.85rem;
        color: #666;
        margin-top: 0.5rem;
        padding-top: 0.5rem;
        border-top: 1px solid #ddd;
    }
    
    .upload-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin-bottom: 2rem;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .status-success {
        background-color: #d4edda;
        color: #155724;
    }
    
    .status-error {
        background-color: #f8d7da;
        color: #721c24;
    }
    
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,1));
        padding: 1.5rem 2rem;
        display: flex;
        gap: 0.5rem;
        align-items: center;
    }
    
    .title-section {
        margin-bottom: 1rem;
    }
    
    .welcome-message {
        font-size: 1rem;
        color: #666;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_url" not in st.session_state:
<<<<<<< HEAD
    st.session_state.api_url = os.getenv("API_URL", "http://localhost:8000")
=======
    st.session_state.api_url = "http://localhost:8000"
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20

if "input_key" not in st.session_state:
    st.session_state.input_key = 0

# Sidebar configuration
st.sidebar.title("Configuration & Tools")

# API Configuration
with st.sidebar.expander("API Settings", expanded=True):
    api_url = st.text_input(
        "API Base URL",
        value=st.session_state.api_url,
        help="Enter the FastAPI server URL"
    )
    st.session_state.api_url = api_url

# Document Upload Section
st.sidebar.markdown("---")
st.sidebar.subheader("Document Management")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF Document",
    type="pdf",
    help="Upload a PDF file to add to the knowledge base"
)

if uploaded_file is not None:
    col1, col2 = st.sidebar.columns([1, 1])
    
    with col1:
        if st.button("Upload", use_container_width=True):
            with st.spinner("Processing document..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                    response = requests.post(
                        f"{st.session_state.api_url}/upload_document/",
                        files=files,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        st.sidebar.success("Document uploaded successfully!")
                        st.sidebar.write(response.json()["message"])
                    else:
                        st.sidebar.error(f"Upload failed: {response.json().get('detail', 'Unknown error')}")
                except requests.exceptions.ConnectionError:
                    st.sidebar.error(f"Cannot connect to API at {st.session_state.api_url}")
                except Exception as e:
                    st.sidebar.error(f"Error uploading document: {str(e)}")

# Sidebar utilities
st.sidebar.markdown("---")
if st.sidebar.button("Clear Chat History", use_container_width=True):
    st.session_state.messages = []
    st.session_state.input_key += 1
    st.rerun()

# Main content area
st.markdown('<div class="title-section">', unsafe_allow_html=True)
st.title("Teleco Support ChatBot")
st.markdown('<p class="welcome-message">I am your Teleco virtual assistant. I’m here to help you with your queries. Feel free to reach out to me anytime I’m always happy to assist you.</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Display chat messages
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Add spacing for fixed input
st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)

# Input area
st.markdown("---")

col1, col2 = st.columns([1, 0.1])

with col1:
    user_input = st.chat_input(
        "Your question:",
        key=f"user_input_{st.session_state.input_key}"
    )

# Process user input - either from chat_input (Enter) or send button
if (user_input and user_input.strip()):
    # Get the query text
    query_text = user_input if user_input else ""
    
    if query_text.strip():
        # Add user message to chat
        st.session_state.messages.append({
            "role": "user",
            "content": query_text
        })
        
        # Display user message immediately
        with chat_container:
            with st.chat_message("user"):
                st.write(query_text)
        
        # Get response from API
        with st.spinner("Processing your query..."):
            try:
                response = requests.post(
                    f"{st.session_state.api_url}/query/",
                    data={"query": query_text},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Add assistant response to chat
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result.get("response", "No response received")
                    })
                    
                    # Increment input key to clear the input box
                    st.session_state.input_key += 1
                    
                    # Display assistant message
                    with chat_container:
                        with st.chat_message("assistant"):
                            st.write(result.get("response", "No response received"))
                    
                    st.rerun()
                else:
                    error_detail = response.json().get("detail", "Unknown error")
                    st.error(f"API Error: {error_detail}")
                    
            except requests.exceptions.ConnectionError:
                st.error(f"Cannot connect to API at {st.session_state.api_url}. Make sure the FastAPI server is running.")
            except requests.exceptions.Timeout:
                st.error("Request timeout. The API took too long to respond.")
            except Exception as e:
                st.error(f"Error processing query: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        <p>Teleco ChatBot v1.0 | Powered by Systems Limited</p>
    </div>
    """,
    unsafe_allow_html=True
)