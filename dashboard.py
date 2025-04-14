from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sidebar import renderSidebar
from hoverbutton import info_button
from mertics_fetcher import fetch_dashboard_metrics

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
    <h3 style='color: black; font-family: Poppins, sans-serif; font-size: 32px; font-weight: 100;'>
        <b style='font-weight: 700;'>Analytics - </b>  <span style=' font-weight: 100;'>LLMOps Dashboard</span>
    </h3>
""", unsafe_allow_html=True)
    
with col2:
    selected_range= st.selectbox("Select Time Range", ["Last 30 days", "Last 7 days"], index=1)

renderSidebar('dashboard')


today = datetime.today()

if selected_range == "Last 30 days":
    start_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")
elif selected_range == "Last 7 days":
    start_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")


end_date = today.strftime("%Y-%m-%d")

# start_date = "2025-03-03"
# end_date = "2025-03-07"

metrics = fetch_dashboard_metrics(start_date, end_date)
print("metrics :",metrics)

# Unpack metrics
dates = metrics["dates"]
rag_latency = metrics["rag_latency"]
response_time = metrics["response_time"]
overall_error_rate = metrics["overall_error_rate"]
llm_error_rate = metrics["llm_error_rate"]
successful_queries = metrics["successful_queries"]
failed_queries = metrics["failed_queries"]
total_queries = metrics["total_queries"]
unique_users = metrics["unique_users"]
chats_per_user = metrics["chats_per_user"]
queries_per_user = metrics["queries_per_user"]
input_tokens = metrics["input_tokens"]
output_tokens = metrics["output_tokens"]
embedding_tokens = [0 for _ in output_tokens]  # If not available in API
llm_cost = metrics["llm_cost"]
embedding_cost = metrics["embedding_cost"]
total_usage_cost = metrics["total_usage_cost"]
cost_per_user = metrics["cost_per_user"]
cost_per_query = metrics["cost_per_query"]
########

#Level-1
col1, col2 = st.columns(2)
# Latency Graph

with col1:

    with st.container(key="col1"):
         
        info_button("Latency and Response Time","<b>Response Time:</b> Avg. time from UI query to response delivery.<br><b>RAG Latency:</b> Avg. time from RAG start to final token generation.")
        df_latency = pd.DataFrame({"Date": dates, "RAG Latency": rag_latency, "Response Time": response_time})
        fig1 = px.line(df_latency, x="Date", y=["RAG Latency", "Response Time"], markers=True,
                     template="simple_white")
        fig1.update_layout(margin=dict(r=200))
        fig1.update_layout(
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
        )
        st.plotly_chart(fig1)

# Error Rates Graph
with col2:
    with st.container(key="col2"):
        info_button(
            "Error Rates",
            "<b>Overall Error Rate:</b> % of total queries that failed (any reason).<br><b>LLM Error Rate:</b> % of queries failed due to LLM issues (e.g., content violations, malformed output).")
        df_error = pd.DataFrame({"Date": dates, "Overall Error Rate": overall_error_rate, "LLM Error Rate": llm_error_rate})
        fig2 = px.line(df_error, x="Date", y=["Overall Error Rate", "LLM Error Rate"], markers=True,
                     template="simple_white")
        fig2.update_layout(margin=dict(r=200))
        fig2.update_layout(
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
        )
        st.plotly_chart(fig2)
########

#Level-2
col3, col4, col5 = st.columns(3)
# Queries Processed Graph
with col3:
    with st.container(key="col3"):
        info_button(
    "Queries Processed",
    "<b>Total Queries:</b> All queries received.<br><b>Successful Queries:</b> Queries processed without errors.<br><b>Failed Queries:</b> Queries that encountered errors."
)

        df_queries = pd.DataFrame({"Date": dates, "Successful Queries": successful_queries, "Failed Queries": failed_queries, "Total Queries": total_queries})
        fig3 = px.bar(df_queries, x="Date", y=["Successful Queries", "Failed Queries"], barmode='group',  template="simple_white")
        fig3.update_layout(margin=dict(r=200))
        fig3.update_layout(
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
        )
        st.plotly_chart(fig3)

# Unique Users Graph
with col4:
    with st.container(key="col4"):
        info_button("Unique Users","<b>Unique Users :</b> Total number of unique User Ids that requested query responses.")
        df_users = pd.DataFrame({"Date": dates, "Unique Users": unique_users})
        fig4 = px.bar(df_users, x="Date", y="Unique Users", template="simple_white")
        
        fig4.update_traces(width=0.28)
        fig4.update_layout(margin=dict(r=130))
        # Update the trace to include a name for the legend
        fig4.update_traces(name="Unique Users for that Day", showlegend=True)

        # Adjust layout to make the legend clear and visible
        fig4.update_layout(legend_title_text="Variable")
        fig4.update_layout(
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
        )
        st.plotly_chart(fig4)

# Chats & Queries per User Graph
with col5:
    with st.container(key="col5"):
        info_button(
    "Chats & Queries per User",
    "<b>Unique Users:</b> Count of distinct users.<br><b>Chats per User:</b> Avg. number of chat sessions per user.<br><b>Queries per User:</b> Avg. queries submitted per user."
)

        df_chats_queries = pd.DataFrame({"Date": dates, "Chats per User": chats_per_user, "Queries per User": queries_per_user})
        fig5 = px.bar(df_chats_queries, x="Date", y=["Chats per User", "Queries per User"], barmode='group',
                     template="simple_white")
        fig5.update_layout(margin=dict(r=200))
        fig5.update_layout(
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
        )
        st.plotly_chart(fig5)
########
#Level-3
col6, col7 = st.columns(2)
# Tokens Processed Graph
with col6:
    with st.container(key="col6"):
        info_button(
    "Tokens Processed",
    "<b>Input Tokens:</b> Prompt tokens used.<br><b>Output Tokens:</b> Completion tokens generated."
)

        df_tokens = pd.DataFrame({"Date": dates, "Input Tokens": input_tokens, "Output Tokens": output_tokens})
        fig6 = px.bar(df_tokens, x="Date", y=["Input Tokens", "Output Tokens"], barmode='group',
                     template="simple_white")
        fig6.update_traces(width=0.2)
        fig6.update_layout(margin=dict(r=200))
        fig6.update_layout(
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
        )
        st.plotly_chart(fig6)

# Cost Metrics Graph
with col7:
    with st.container(key="col7"):
        info_button(
    "Cost Metrics",
    "<b>LLM Cost:</b> Total spend on LLM usage.<br><b>Embedding Cost:</b> Total spend on embedding models.<br><b>Total Cost:</b> Combined LLM + Embedding cost."
)

        df_cost = pd.DataFrame({"Date": dates, "LLM Cost": llm_cost, "Embedding Cost": embedding_cost, "Total Usage Cost": total_usage_cost})
        fig7 = px.bar(df_cost, x="Date", y=["LLM Cost", "Embedding Cost"], barmode='group',
                     template="simple_white")
        fig7.update_traces(width=0.2)
        fig7.add_scatter(x=dates, y=total_usage_cost, mode='lines+markers', name='Total Usage Cost')
        fig7.update_layout(margin=dict(r=200))
        fig7.update_layout(
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        yaxis_title="DBU"
        )
        st.plotly_chart(fig7)   

col8, col9 = st.columns(2)


# Cost per User Graph
with col8:
    with st.container(key="col8"):
        info_button("Cost per User","<b>Cost per User:</b> Avg. spend per user.<br><b>Cost per User:</b> (Total Usage Cost / Number of Queries)")
        df_cost_user = pd.DataFrame({"Date": dates, "Cost per User": cost_per_user})
        fig8 = px.bar(df_cost_user, x="Date", y="Cost per User",  template="simple_white")
        # Update the trace to include a name for the legend
        fig8.update_traces(name="Cost per User  per Day", showlegend=True)

        # Adjust layout to make the legend clear and visible
        fig8.update_layout(legend_title_text="Variable")
        fig8.update_traces(width=0.2)
        fig8.update_layout(margin=dict(r=200))
        fig8.update_layout(
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        yaxis_title="DBU"
        )
        st.plotly_chart(fig8)

# Cost per Query Graph
with col9:
    with st.container(key="col9"):
        info_button("Cost per Query","<b>Cost per Query:</b> Avg. spend per query.<br><b>Cost per Query:</b> (Total Usage Cost / Number of Queries)")
        df_cost_query = pd.DataFrame({"Date": dates, "Cost per Query": cost_per_query})
        fig9 = px.bar(df_cost_query, x="Date", y="Cost per Query", template="simple_white")
        # Update the trace to include a name for the legend
        fig9.update_traces(name="Cost per Query per Day", showlegend=True)

        # Adjust layout to make the legend clear and visible
        fig9.update_layout(legend_title_text="Variable")
        fig9.update_traces(width=0.2)
        fig9.update_layout(margin=dict(r=200))
        fig9.update_layout(
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        yaxis_title="DBU"
        )
        st.plotly_chart(fig9)
