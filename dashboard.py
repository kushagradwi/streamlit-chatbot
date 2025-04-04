import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sidebar import renderSidebar
from hoverbutton import info_button

# Set page config
st.set_page_config(layout="wide", page_title="LLM Ops Dashboard")

with open("static/css/sidebar.css") as css_file:
    st.html(f"<style>{css_file.read()}</style>")

with open("static/css/dashboard.css") as dashboard_css_file:
    st.html(f"<style>{dashboard_css_file.read()}</style>")    

# Header with Timeline Selector
col1, col2 = st.columns([4, 1])
with col1:
    #st.title("LLM Ops Dashboard")
    
    st.markdown("""
    <h3 style='color: black; font-family: Poppins, sans-serif; font-size: 28px; font-weight: 100;'>
        <b style='font-weight: 700;'>Analytics - </b>  <span style=' font-weight: 100;'>LLM Ops Dashboard</span>
    </h3>
""", unsafe_allow_html=True)
    
with col2:
    st.selectbox("Select Time Range", ["Last 30 days", "Last 7 days", "Today"], index=0)

renderSidebar('dashboard')


#########
#Data
dates = ["03-Mar", "04-Mar", "05-Mar", "06-Mar", "07-Mar"]
rag_latency = [2300, 4000, 3500, 9000, 3000]
response_time = [2400, 4100, 3600, 9100, 3100]
overall_error_rate = [0.9, 1.2, 1.5, 0.6, 1.5]
llm_error_rate = [0.8, 1.2, 1.0, 0.4, 1.4]
successful_queries = [4955, 3359, 4826, 6659, 4186]
failed_queries = [45, 41, 74, 41, 64]
total_queries = [5000, 3400, 4900, 6700, 4250]
unique_users = [10, 12, 22, 35, 29]
chats_per_user = [5, 7, 12, 9, 14]
queries_per_user = [50, 70, 120, 90, 140]
input_tokens = [300000, 250000, 290000, 500000, 490000]
output_tokens = [400000, 200000, 290000, 500000, 490000]
embedding_tokens = [530000, 870000, 590000, 335000, 990000]
llm_cost = [x * 0.0001 for x in output_tokens]
embedding_cost = [x * 0.00005 for x in embedding_tokens]
total_usage_cost = [lc + ec for lc, ec in zip(llm_cost, embedding_cost)]
cost_per_user = [tc / u for tc, u in zip(total_usage_cost, unique_users)]
cost_per_query = [tc / tq for tc, tq in zip(total_usage_cost, total_queries)]
########
#Level-1
col1, col2 = st.columns(2)
# Latency Graph

with col1:

    with st.container(key="col1"):
         
        info_button("Latency and Response Time Graph","Response Time = Average time between the UI request with the query, and the time till the passing back of the response.\n RAG Latency = Average time taken from the start of query input to the RAG pipeline, till the generation of last token of response.")
        df_latency = pd.DataFrame({"Date": dates, "RAG Latency": rag_latency, "Response Time": response_time})
        fig1 = px.line(df_latency, x="Date", y=["RAG Latency", "Response Time"], markers=True,
                    title="Latency for RAG and Response Time", template="simple_white")
        st.plotly_chart(fig1)

# Error Rates Graph
with col2:
    with st.container(key="col2"):
        info_button("Error Rates Graph","Overall Error Rate = Percentage of total queries from the users that failed. (LLM Errors + API Errors + Network errors + etc.)\n LLM Error Rate = Percentage of total queries from the users that failed, due to LLM response issues. (content violation, llm response structure issues, etc.")
        df_error = pd.DataFrame({"Date": dates, "Overall Error Rate": overall_error_rate, "LLM Error Rate": llm_error_rate})
        fig2 = px.line(df_error, x="Date", y=["Overall Error Rate", "LLM Error Rate"], markers=True,
                    title="Error Rates for Overall and LLM", template="simple_white")
        st.plotly_chart(fig2)
########
#Level-2
col3, col4, col5 = st.columns(3)
# Queries Processed Graph
with col3:
    with st.container(key="col3"):
        info_button("Queries Processed Graph","Total Queries = The total number of queries across users that were received.\n Successful Queries = The total number of queries across users that were successfully processed. \n Failed Queries = The total number of queries across users that failed.")
        df_queries = pd.DataFrame({"Date": dates, "Successful Queries": successful_queries, "Failed Queries": failed_queries, "Total Queries": total_queries})
        fig3 = px.bar(df_queries, x="Date", y=["Successful Queries", "Failed Queries"], barmode='group',
                    text=df_queries["Total Queries"], title="Queries Processed per Day", template="simple_white")
        fig3.update_traces(texttemplate='%{text}', textposition='outside')
        st.plotly_chart(fig3)

# Unique Users Graph
with col4:
    with st.container(key="col4"):
        info_button("Unique Users Graph","Unique Users = Total number of unique User Ids that requested query responses.")
        df_users = pd.DataFrame({"Date": dates, "Unique Users": unique_users})
        fig4 = px.bar(df_users, x="Date", y="Unique Users", title="Unique Users per Day",template="simple_white")
        
        fig4.update_traces(width=0.28)
        fig4.update_layout(margin=dict(r=130))
        # Update the trace to include a name for the legend
        fig4.update_traces(name="Unique Users for that Day", showlegend=True)

        # Adjust layout to make the legend clear and visible
        fig4.update_layout(legend_title_text="Variable")
        st.plotly_chart(fig4)

# Chats & Queries per User Graph
with col5:
    with st.container(key="col5"):
        info_button("Chats & Queries per User Graph"," Chats per user = The average number of chat sessions that were triggered per user. \n Queries per user = The average number of queries requested per user.")
        df_chats_queries = pd.DataFrame({"Date": dates, "Chats per User": chats_per_user, "Queries per User": queries_per_user})
        fig5 = px.bar(df_chats_queries, x="Date", y=["Chats per User", "Queries per User"], barmode='group',
                    title="Chats and Queries per User", template="simple_white")
        st.plotly_chart(fig5)
########
#Level-3
col6, col7 = st.columns(2)
# Tokens Processed Graph
with col6:
    with st.container(key="col6"):
        info_button("Tokens Processed Graph","Input Tokens = The total number of input tokens that were used (prompt tokens) \n Output Tokens = The total number of output tokens that were used (completion tokens) \n Embedding Tokens = The total number of embedding tokens used for semantic similarity")
        df_tokens = pd.DataFrame({"Date": dates, "Input Tokens": input_tokens, "Output Tokens": output_tokens, "Embedding Tokens": embedding_tokens})
        fig6 = px.bar(df_tokens, x="Date", y=["Input Tokens", "Output Tokens", "Embedding Tokens"], barmode='group',
                    title="Tokens Processed", template="simple_white")
        st.plotly_chart(fig6)

# Cost Metrics Graph
with col7:
    with st.container(key="col7"):
        info_button("Cost Metrics Graph","Total Usage Cost = The total usage cost (LLM Cost + Embedding Cost) \n LLM Cost = The total cost incurred for using the LLMs at multiple stages of the RAG pipeline.\n Embedding Cost = The total cost incurred for using the Embedding models at multiple stages of the RAG pipeline.")
        df_cost = pd.DataFrame({"Date": dates, "LLM Cost": llm_cost, "Embedding Cost": embedding_cost, "Total Usage Cost": total_usage_cost})
        fig7 = px.bar(df_cost, x="Date", y=["LLM Cost", "Embedding Cost"], barmode='group',
                    title="Cost Metrics per Day", template="simple_white")
        fig7.add_scatter(x=dates, y=total_usage_cost, mode='lines+markers', name='Total Usage Cost')
        st.plotly_chart(fig7)
col8, col9 = st.columns(2)
# Cost per User Graph
with col8:
    with st.container(key="col8"):
        info_button("Cost per User Graph","Cost per User = The average overall cost incurred per user")
        df_cost_user = pd.DataFrame({"Date": dates, "Cost per User": cost_per_user})
        fig8 = px.bar(df_cost_user, x="Date", y="Cost per User", title="Cost per User per Day", template="simple_white")
        # Update the trace to include a name for the legend
        fig8.update_traces(name="Cost per USer  per Day", showlegend=True)

        # Adjust layout to make the legend clear and visible
        fig8.update_layout(legend_title_text="Variable")
        fig8.update_traces(width=0.2)
        fig8.update_layout(margin=dict(r=130))
        st.plotly_chart(fig8)

# Cost per Query Graph
with col9:
    with st.container(key="col9"):
        info_button("Cost per Query Graph","Cost per query = The average overall cost incurred per a user query.")
        df_cost_query = pd.DataFrame({"Date": dates, "Cost per Query": cost_per_query})
        fig9 = px.bar(df_cost_query, x="Date", y="Cost per Query", title="Cost per Query per Day", template="simple_white")
        # Update the trace to include a name for the legend
        fig9.update_traces(name="Cost per Query per Day", showlegend=True)

        # Adjust layout to make the legend clear and visible
        fig9.update_layout(legend_title_text="Variable")
        fig9.update_traces(width=0.2)
        fig9.update_layout(margin=dict(r=130))
        st.plotly_chart(fig9)
