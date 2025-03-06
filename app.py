import streamlit as st
import requests
from src.exception import CustomException
import sys

# Configure Streamlit page
# Configure Streamlit page
st.set_page_config(
    page_title="RAG Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .success-message {
            padding: 1rem;
            border-radius: 5px;
            background-color: #D4EDDA;
            color: #155724;
            margin: 1rem 0;
        }
        .error-message {
            padding: 1rem;
            border-radius: 5px;
            background-color: #F8D7DA;
            color: #721C24;
            margin: 1rem 0;
        }
        .info-box {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .centered-header {
            text-align: center;
            padding: 20px;
            background: linear-gradient(90deg, #1E88E5, #1565C0);
            color: white;
            border-radius: 10px;
            margin-bottom: 30px;
        }
    </style>
""", unsafe_allow_html=True)

# Base URL for the FastAPI server
BASE_URL = "https://8001-01jmep9axx72ewy4mdzwddcqsd.cloudspaces.litng.ai"  # Update with your actual server URL

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_pipeline_id' not in st.session_state:
    st.session_state.current_pipeline_id = None
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = {}


def process_document(uploaded_file, pipeline_id, action):
    """Process the uploaded PDF document and perform specified action."""
    try:
        if action == "create":
            # Prepare the file for upload
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}

            # Send request to create pipeline
            response = requests.post(
                f"{BASE_URL}/create_pipeline/{pipeline_id}",
                files=files
            )

            # Check response
            if response.status_code == 200:
                # Store uploaded file info
                st.session_state.uploaded_files[pipeline_id] = uploaded_file.name
                return 1
            elif response.status_code == 400:
                return -1
            else:
                return 0

        elif action == "remove":
            # Send request to delete pipeline
            response = requests.delete(f"{BASE_URL}/delete_pipeline/{pipeline_id}")

            # Check response
            if response.status_code == 200:
                # Remove file info if exists
                if pipeline_id in st.session_state.uploaded_files:
                    del st.session_state.uploaded_files[pipeline_id]
                return 1
            else:
                return 0

    except Exception as e:
        raise CustomException(e, sys)


def main():
    # Header
    st.markdown('<div class="centered-header"><h1>🤖 RAG Assistant</h1></div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("Pipeline Management")

        # Create Pipeline Section
        with st.expander("Create New Pipeline", expanded=True):
            pipeline_id = st.text_input("Pipeline ID:", key="create_pipeline_id", placeholder="Enter numeric ID")
            uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"], key="create_file")

            if st.button("Create Pipeline", key="create_btn"):
                if uploaded_file and pipeline_id:
                    try:
                        with st.spinner("Creating pipeline..."):
                            result = process_document(uploaded_file, pipeline_id, "create")
                            if result == 1:
                                # Enhanced code block with more context
                                st.code(f"""# Example Python Script for Querying RAG Pipeline
    import requests

    # Base URL of your RAG service
    BASE_URL = "{BASE_URL}"

    # Your specific pipeline ID
    PIPELINE_ID = "{pipeline_id}"

    # Function to query the pipeline
    def query_rag_pipeline(query):
        response = requests.post(
            f"{{BASE_URL}}/query_pipeline/{{PIPELINE_ID}}", 
            params={{"query": query}}
        )

        if response.status_code == 200:
            result = response.json()
            print("Answer:", result.get("answer"))
            print("Sources:", result.get("sources"))
        else:
            print("Query failed!")

    # Example usage
    query_rag_pipeline("Your question here")
    """, language="python")

                                st.success("Pipeline created successfully!")
                                st.session_state.current_pipeline_id = pipeline_id

                            elif result == -1:
                                st.error("Pipeline ID already exists.")
                            else:
                                st.error("Failed to create pipeline.")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please provide both Pipeline ID and PDF document.")

        # Delete Pipeline Section
        with st.expander("Delete Pipeline", expanded=False):
            delete_pipeline_id = st.text_input("Pipeline ID to Delete:", key="delete_pipeline_id")
            if st.button("Delete Pipeline", key="delete_btn"):
                if delete_pipeline_id:
                    try:
                        with st.spinner("Deleting pipeline..."):
                            result = process_document(None, delete_pipeline_id, "remove")
                            if result == 1:
                                st.success("Pipeline deleted successfully!")
                                if st.session_state.current_pipeline_id == delete_pipeline_id:
                                    st.session_state.current_pipeline_id = None
                                    st.session_state.messages = []
                            else:
                                st.error("Pipeline not found.")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please provide a Pipeline ID.")

    # Main content area
    col1, col2 = st.columns([2, 1])

    # Right column (System Info)
    with col2:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.subheader("Active Pipeline")

        # Use callback for pipeline ID change
        def on_pipeline_change():
            st.session_state.current_pipeline_id = st.session_state.active_pipeline_id
            st.session_state.messages = []  # Clear chat history when pipeline changes

        active_pipeline_id = st.text_input(
            "Enter Pipeline ID for Chat:",
            key="active_pipeline_id",
            on_change=on_pipeline_change
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # System Information
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.subheader("System Information")
        st.info("Using Llama Model for RAG")
        st.progress(100, "System Ready")

        # Show uploaded file if pipeline is active
        if st.session_state.current_pipeline_id:
            st.success(f"Active Pipeline: {st.session_state.current_pipeline_id}")
            if st.session_state.current_pipeline_id in st.session_state.uploaded_files:
                st.write(f"📄 Uploaded File: {st.session_state.uploaded_files[st.session_state.current_pipeline_id]}")

        st.markdown('</div>', unsafe_allow_html=True)

    # Left column (Chat Interface)
    with col1:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(f'<div class="{message["role"]}-message">{message["content"]}</div>',
                            unsafe_allow_html=True)
                if message.get("sources"):
                    with st.expander("Sources"):
                        for idx, source in enumerate(message["sources"], 1):
                            st.markdown(f"**Source {idx}:**\n{source}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("Ask your question..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get pipeline ID from session state
        if not st.session_state.current_pipeline_id:
            st.session_state.messages.append({"role": "assistant", "content": "Please select a pipeline ID first."})
            st.experimental_rerun()

        # Process query
        with st.spinner("Thinking..."):
            try:
                # Send query to FastAPI endpoint
                response = requests.post(
                    f"{BASE_URL}/query_pipeline/{st.session_state.current_pipeline_id}",
                    params={"query": prompt}
                )

                # Check response
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result.get("answer", "No response"),
                        "sources": result.get("sources", [])
                    })
                else:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "Error processing query."
                    })
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Error: {str(e)}"
                })

        st.experimental_rerun()


if __name__ == "__main__":
    main()