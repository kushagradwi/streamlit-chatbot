import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sidebar import renderSidebar

# Set page config
st.set_page_config(layout="wide", page_title="LLM Ops Dashboard")

with open("static/css/sidebar.css") as css_file:
    st.html(f"<style>{css_file.read()}</style>")

with open("static/css/dashboard.css") as dashboard_css_file:
    st.html(f"<style>{dashboard_css_file.read()}</style>")    

# Header with Timeline Selector
col1, col2 = st.columns([4, 1])
with col1:
    st.title("LLM Ops Dashboard")
with col2:
    st.selectbox("Select Time Range", ["Last 30 days", "Last 7 days", "Today"], index=0)

# Sample Data
dates = pd.date_range(start="2024-08-01", periods=10)
data = pd.DataFrame({
    "Date": dates,
    "Success Requests": np.random.randint(200, 800, size=10),
    "Failure Requests": np.random.randint(50, 300, size=10),
    "Chat Model Latency": np.random.randint(100, 400, size=10),
    "Lookup Latency": np.random.randint(100, 400, size=10),
    "Prompt Latency": np.random.randint(100, 400, size=10),
})

# Main Layout
col1, col2 = st.columns(2)

renderSidebar('dashboard')

# Request Handling Status
with col1:
    with st.container(key="col1"):
        st.subheader("Request Handling Status")
        fig = px.bar(data, x="Date", y=["Success Requests", "Failure Requests"],
                    labels={"value": "Number of Requests", "variable": "Status"},
                    title="Day Level Requests - Status Counts Across Time",
                    barmode="group",
                    color_discrete_map={"Success Requests": "green", "Failure Requests": "red"})
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', 
                        margin=dict(l=10, r=10, t=30, b=10),
                        xaxis=dict(showgrid=False), yaxis=dict(showgrid=False),
                        font=dict(color='rgba(157, 157, 157, 1)'))
        st.plotly_chart(fig, use_container_width=True)

# System Metric Overview
with col2:
    with st.container(key="col2"):
        st.subheader("System Metric Overview")
        metric1, metric2, metric3 = st.columns(3)
        metric1.metric(label="Avg Flow Latency", value=f"{np.mean(data['Chat Model Latency']):.2f} ms")
        metric2.metric(label="Avg Token Consumption", value="N/A")
        metric3.metric(label="Error Rate", value="N/A")

# Row 2: LLM Latency & Daily Avg Node Latency
col3, col4 = st.columns(2)

with col3:
    with st.container(key="col3"):
        st.subheader("LLM Latency")  
        fig = px.line(data, x="Date", y="Chat Model Latency", title="Remote Procedure Call Latency")
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', 
                        margin=dict(l=10, r=10, t=30, b=10),
                        xaxis=dict(showgrid=False), yaxis=dict(showgrid=False),
                        font=dict(color='rgba(157, 157, 157, 1)'))
        st.plotly_chart(fig, use_container_width=True)

with col4:
    with st.container(key="col4"):
        st.subheader("Daily Average Node Latency")
        fig = px.bar(data, x="Date", y=["Chat Model Latency", "Lookup Latency", "Prompt Latency"],
                    labels={"value": "Latency (ms)", "variable": "Type"},
                    title="Comparison of Chat Model, Prompt, and Lookup Latency",
                    barmode="group",
                    color_discrete_map={"Chat Model Latency": "blue", "Lookup Latency": "red", "Prompt Latency": "green"})
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', 
                        margin=dict(l=10, r=10, t=30, b=10),
                        xaxis=dict(showgrid=False), yaxis=dict(showgrid=False),
                        font=dict(color='rgba(157, 157, 157, 1)'))
        st.plotly_chart(fig, use_container_width=True)

# Row 3: Request Frequency & Node Latency Trend
col5, col6 = st.columns(2)

with col5:
    with st.container(key="col5"):
        st.subheader("Request Frequency")    
        fig = px.line(data, x="Date", y=["Success Requests", "Failure Requests"],
                    labels={"value": "Number of Requests", "variable": "Type"},
                    title="Number of Requests Across Time")
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', 
                        margin=dict(l=10, r=10, t=30, b=10),
                        xaxis=dict(showgrid=False), yaxis=dict(showgrid=False),
                        font=dict(color='rgba(157, 157, 157, 1)'))
        st.plotly_chart(fig, use_container_width=True)

with col6:
    with st.container(key="col6"):
        st.subheader("Node Latency Trend")
        fig = px.line(data, x="Date", y="Chat Model Latency", title="Trend of Chat Model, Prompt, and Lookup Latency")
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', 
                        margin=dict(l=10, r=10, t=30, b=10),
                        xaxis=dict(showgrid=False), yaxis=dict(showgrid=False),
                        font=dict(color='rgba(157, 157, 157, 1)'))
        st.plotly_chart(fig, use_container_width=True)

