from dotenv import load_dotenv
import streamlit as st

load_dotenv()

from utils.general import initialize_app, show_model_selection, init_model_selection



st.set_page_config(
    page_title="LinkedIn Job Scraper",
    layout="wide",
)

if 'initialized' not in st.session_state:
    initialize_app()


with st.sidebar:
    init_model_selection()
    show_model_selection()

    
st.title("Welcome!")
st.subheader("Manage your applications effortlessly.")
st.write("## ")

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    st.markdown("### 🔍 Search")
    st.markdown("Find your next opportunity.")

with col2: 
    st.markdown("### ✅ Letters")
    st.markdown("View and edit your cover letters.")

with col3:
    st.markdown("### ✍️ Custom")
    st.markdown("Create custom cover letters in seconds.")

with col4:
    st.markdown("#### 📝 CV")
    st.markdown("Keep your CV up-to-date.")

