import streamlit as st
import os 

st.set_page_config(page_title="CV", page_icon="📝", layout="wide")


st.header("Edit your CV")
st.write("")


# Load and display existing CV content
if os.path.exists("cv.txt"):
    with open("cv.txt", "r") as file:
        existing_cv = file.read()
else:
    existing_cv = "Your CV content goes here."

cv_text = st.text_area("Your CV", existing_cv, height=400, label_visibility="hidden")
save_cv_button = st.button("Save CV")

if save_cv_button:
    with open("cv.txt", "w") as file:
        file.write(cv_text)
    st.success("CV updated successfully!")