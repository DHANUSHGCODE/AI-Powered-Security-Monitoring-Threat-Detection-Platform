import streamlit as st
import pandas as pd
import joblib

st.title("AI-Powered Security Monitoring")

data = pd.read_csv("data/sample_logs.csv")
model = joblib.load("model/anomaly_model.pkl")

data['anomaly'] = model.predict(data[['bytes']])
anomalies = data[data['anomaly'] == -1]

st.metric("Total Logs", len(data))
st.metric("Anomalies", len(anomalies))

st.subheader("All Logs")
st.dataframe(data)

st.subheader("Detected Anomalies")
st.dataframe(anomalies)

if len(anomalies) > 0:
    st.warning("Suspicious activity detected!")
else:
    st.success("No threats detected")
