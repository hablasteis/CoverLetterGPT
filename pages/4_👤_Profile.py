import streamlit as st
import os 
import json

st.set_page_config(page_title="Profile", page_icon="👤", layout="wide")

st.header("Update your CV")

st.write("")
st.info("**Disclaimer**: All your personal data is hosted locally on your computer and used **only** for the generation of the **cover letter**.")

st.write("")
st.write("")
c1, _, c2 = st.columns([4, 1, 12])

with c1:

    st.subheader("Personal info")

    if os.path.exists("cv.txt"):
        with open("cv.txt", "r") as file:
            existing_cv = file.read()


    if os.path.exists("info.json"):
        with open("info.json", 'r') as file:
            info = json.load(file)
    else:
        info = {
            "name": "",
            "address": "",
            "email": "",
            "phone": "",
            }
    

    st.write("")    
    info["name"] = st.text_input("**Name** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; e.g. \"John Doe\"", info["name"])

    st.write("")    
    info["address"] = st.text_input("**Address** ", info["address"])

    st.write("")    
    info["email"] = st.text_input("**Email** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; e.g. \"john.doe@mail.com\"", info["email"])

    st.write("")    
    info["phone"] = st.text_input("**Phone** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; e.g. \"+12 123 123 1231\"", info["phone"])

    save_info_button = st.button("Save informations")

    if save_info_button:
        with open("info.json", 'w') as file:
            json.dump(info, file)  # Save object as a JSON
        st.success("Info updated successfully!")

with c2:
    st.subheader("CV")
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