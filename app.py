
import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from db import insert_data, get_all_data

#  Load trained model
model = joblib.load("model.pkl")

st.set_page_config(page_title="Learning Path Generator", layout="centered")

st.title(" Personalized Learning Path Generator")

# USER INPUT SECTION
st.subheader(" Enter Student Details")

hours = st.slider("Hours Studied", 0, 12, 5)
previous = st.slider("Previous Scores", 0, 100, 50)
extra = st.selectbox("Extracurricular Activities", ["Yes", "No"])
sleep = st.slider("Sleep Hours", 0, 10, 6)
papers = st.slider("Sample Papers Practiced", 0, 20, 5)

# Convert categorical
extra_val = 1 if extra.lower() == "yes" else 0

#  PREDICTION BUTTON
if st.button(" Predict Performance"):

    input_data = pd.DataFrame([{
        "Hours Studied": hours,
        "Previous Scores": previous,
        "Extracurricular Activities": extra_val,
        "Sleep Hours": sleep,
        "Sample Question Papers Practiced": papers
    }])

    #  Predict
    score = model.predict(input_data)[0]

    st.subheader(f"Predicted Score: {score:.2f}")

    #  Recommendation
    if score < 40:
        rec = "Basic Learning Path"
    elif score < 70:
        rec = "Intermediate Learning Path"
    else:
        rec = "Advanced Learning Path"

    st.success(rec)

    #  Save to MongoDB
    insert_data(input_data.iloc[0], score)

    st.info(" Data saved to cloud database!")


# SHOW GRAPH
if st.button("Show Performance Graph"):

    data = get_all_data()

    if data and len(data) > 1:
        df = pd.DataFrame(data)

        st.subheader(" Stored Data")
        st.dataframe(df)

        #  Line Graph
        plt.figure()
        plt.plot(range(len(df)), df["performance"], marker='o')
        plt.xlabel("Students")
        plt.ylabel("Performance Score")
        plt.title("Student Performance Trend")

        st.pyplot(plt)

    elif data and len(data) == 1:
        st.warning("Only 1 record found. Showing bar chart instead.")

        df = pd.DataFrame(data)

        plt.figure()
        plt.bar(["Student 1"], df["performance"])
        plt.ylabel("Performance Score")
        plt.title("Single Student Performance")

        st.pyplot(plt)

    else:
        st.error(" No data found in database!")