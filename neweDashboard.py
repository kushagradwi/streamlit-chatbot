import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fastapi import BackgroundTasks

st.set_page_config(page_title="LLMOPS Dashboard Design", layout="wide")

# # Create a bar chart
# bar_fig = go.Figure(data=[go.Bar(x=categories, y=values)])
# bar_fig.update_layout(title="Sample Bar Chart", xaxis_title="Categories", yaxis_title="Values")


# Performance Charts

# 1. LATENCY (RAG Latency, Response Time)
dates = ['03-Mar', '04-Mar', '05-Mar', '06-Mar', '07-Mar']
avg_rag_latency_ms = [2300,4000,3500,9000,3000]
avg_response_time_sec = [2400,4100,3600,9100,3100]

# 2. Error Rates (LLM Error Rate, Overall Error Rate)
error_rates = [0.9, 1.2, 1.5, 0.6, 1.5]
llm_error_rates = [0.8, 1.2, 1.0, 0.4, 1.4]

# 3. Requests
successful_reqs = [4955, 3359, 4826, 6659, 4186]
failure_reqs = [45, 41, 74, 41, 64]
total_reqs = [5000, 3400, 4900, 6700, 4250]


latency_line_fig = go.Figure()
latency_line_fig.add_trace(go.Scatter(x=dates, y=avg_rag_latency_ms, mode='lines+markers', name="RAG Latency"))
latency_line_fig.add_trace(go.Scatter(x=dates, y=avg_response_time_sec, mode='lines+markers', name="Response Time"))
latency_line_fig.update_layout(title="Latency", xaxis_title="date", yaxis_title="time(ms)")

errors_line_fig = go.Figure()
errors_line_fig.add_trace(go.Scatter(x=dates, y=error_rates, mode='lines+markers', name="Overall Error Rate"))
errors_line_fig.add_trace(go.Scatter(x=dates, y=llm_error_rates, mode='lines+markers', name="LLM Error Rate"))
errors_line_fig.update_layout(title="Error Rates", xaxis_title="date", yaxis_title="Error Percentage")

requests_fig = go.Figure()
requests_fig.add_trace(go.Bar(x=dates, y=successful_reqs, name="Successful Queries", marker_color='green', text=successful_reqs, textposition="inside"))
requests_fig.add_trace(go.Bar(x=dates, y=failure_reqs, name="Failed Queries", marker_color='red', text=failure_reqs, textposition="inside"))
# requests_fig.add_trace(go.Scatter(x=dates, y=total_reqs, name="Total Queries", marker_color='blue'))
requests_fig.add_trace(go.Scatter(
    x=dates,
    y=total_reqs,
    text=total_reqs,
    mode="text",
    textposition="top center",
    showlegend=False  # Hide from legend
))
requests_fig.update_layout(
    title="Queries Processed",
    xaxis_title="Date",
    yaxis_title="# of Queries",
    barmode='stack'  # Change to 'group' for side-by-side bars
)

# Usage Charts

uniques_users = [10, 12, 22, 35, 29]
chats_per_user = [5, 7, 12, 9, 14]
queries_per_user = [50, 70, 120, 90, 140]

# usage_requests_fig = go.Figure()
# usage_requests_fig.add_trace(go.Scatter(x=dates, y=total_reqs, name="Total Requests", marker_color='blue'))
# usage_requests_fig.update_layout(title="Queries Processed", xaxis_title="date", yaxis_title="# of Queries")

usage_requests_fig = go.Figure()
usage_requests_fig.add_trace(go.Bar(x=dates, y=successful_reqs, name="Successful Queries", marker_color='green', text=successful_reqs, textposition="inside"))
usage_requests_fig.add_trace(go.Bar(x=dates, y=failure_reqs, name="Failed Queries", marker_color='red', text=failure_reqs, textposition="inside"))
# requests_fig.add_trace(go.Scatter(x=dates, y=total_reqs, name="Total Queries", marker_color='blue'))
usage_requests_fig.add_trace(go.Scatter(
    x=dates,
    y=total_reqs,
    text=total_reqs,
    mode="text",
    textposition="top center",
    showlegend=False  # Hide from legend
))
usage_requests_fig.update_layout(
    title="Queries Processed",
    xaxis_title="Date",
    yaxis_title="# of Queries",
    barmode='stack'  # Change to 'group' for side-by-side bars
)


uniques_users_fig = go.Figure(data=[go.Bar(x=dates, y=uniques_users)])
uniques_users_fig.update_layout(title="Unique Users", xaxis_title="Date", yaxis_title="# of Uniquw Users")

per_user_fig = go.Figure()
per_user_fig.add_trace(go.Bar(x=dates, y=chats_per_user, name="Chats per user", marker_color='yellow'))
per_user_fig.add_trace(go.Bar(x=dates, y=queries_per_user, name="Queries per user", marker_color='blue'))
per_user_fig.update_layout(
    title="Chats & Queries per user",
    xaxis_title="Date",
    yaxis_title="Number",
    barmode='group'  # Change to 'group' for side-by-side bars
)

# Cost Charts
cost_per_1M_tokens = {"prompt_cost": 7.143, "compln_cost": 21.429, "embedding_cost":1.857}
total_prompt_tokens = [300000, 250000, 290000, 500000, 490000]
total_completion_tokens = [400000, 200000, 290000, 500000, 490000]
total_embedding_tokens = [530000, 870000, 590000, 335000, 990000]

total_input_cost = [tokens * 1e-6 * cost_per_1M_tokens['prompt_cost'] for tokens in total_prompt_tokens]
total_output_cost = [tokens * 1e-6 * cost_per_1M_tokens['compln_cost'] for tokens in total_completion_tokens]
total_llm_cost = [i+j for i,j in zip(total_input_cost, total_output_cost)]
total_embedding_cost = [tokens * 1e-6 * cost_per_1M_tokens['embedding_cost'] for tokens in total_embedding_tokens]
total_llm_embed_cost = [i+j for i,j in zip(total_llm_cost, total_embedding_cost)]

avg_cost_per_user = [cost/user for cost, user in zip(total_llm_embed_cost, uniques_users)]
avg_cost_per_query = [cost/tot_reqs for cost, tot_reqs in zip(total_llm_embed_cost, total_reqs)]
queries_per_dbu = [1/cpq for cpq in avg_cost_per_query]

tokens_fig = go.Figure()
tokens_fig.add_trace(go.Bar(x=dates, y=total_prompt_tokens, name="Input Tokens", marker_color='orange'))
tokens_fig.add_trace(go.Bar(x=dates, y=total_completion_tokens, name="Output Tokens", marker_color='blue'))
tokens_fig.add_trace(go.Bar(x=dates, y=total_embedding_tokens, name="Embedding Tokens", marker_color='purple'))
tokens_fig.update_layout(
    title="Tokens Processed",
    xaxis_title="Date",
    yaxis_title="# of Tokens",
    barmode='group'  # Change to 'group' for side-by-side bars
)


overall_cost_fig = go.Figure()
overall_cost_fig.add_trace(go.Bar(x=dates, y=total_llm_cost, name="LLMs Cost", marker_color='green'))
overall_cost_fig.add_trace(go.Bar(x=dates, y=total_embedding_cost, name="Embeddings Cost", marker_color='yellow'))
overall_cost_fig.add_trace(go.Scatter(x=dates, y=total_llm_embed_cost, name="Total Usage Cost", marker_color='blue'))
overall_cost_fig.update_layout(
    title="Cost",
    xaxis_title="Date",
    yaxis_title="Cost (DBU)",
    barmode='group'  # Change to 'group' for side-by-side bars
)

cost_per_user_fig = go.Figure(data=[go.Bar(x=dates, y=avg_cost_per_user)])
cost_per_user_fig.update_layout(title="Cost per User", xaxis_title="date", yaxis_title="cost (DBU)")

cost_per_query_fig = go.Figure(data=[go.Bar(x=dates, y=avg_cost_per_query)])
cost_per_query_fig.update_layout(title="Cost per Query", xaxis_title="date", yaxis_title="cost (DBU)")

queries_per_dbu_fig = go.Figure(data=[go.Bar(x=dates, y=queries_per_dbu)])
queries_per_dbu_fig.update_layout(title="Possible # of Queries per DBU", xaxis_title="date", yaxis_title="Number")


# # Create a table
# df = pd.DataFrame({
#     "Month": months,
#     "Product 1 Sales": product_1_sales,
#     "Product 2 Sales": product_2_sales,
#     "Product 3 Sales": product_3_sales
# })

# Display elements in Streamlit

st.header("PERFORMANCE METRICS")
# col1, col2, col3 = st.columns(3)
col1, col2 = st.columns(2)

with col1:
    with st.expander("ℹ️ more info"):
        st.write("""
        Response Time = Average time between the UI request with the query, and the time till the passing back of the response\n
        RAG Latency = Average time taken from the start of query input to the RAG pipeline, till the generation of last token of response.
        """)
    st.plotly_chart(latency_line_fig)
with col2:
    with st.expander("ℹ️ more info"):
        st.write("""
        Overall Error Rate = Percentage of total queries from the users that failed. (LLM Errors + API Errors + Network errors + etc.)\n
        LLM Error Rate = Percentage of total queries from the users that failed, due to LLM response issues. (content violation, llm response structure issues, etc.)
        """)
    st.plotly_chart(errors_line_fig)
# with col3:
#     with st.expander("ℹ️ more info"):
#         st.write("""
#         Successful Requests = The total number of requests that were successfully processed.\n
#         Failure Requests = The total number of requests that were failed.\n
#         Total Requests = The total number of requests that were received.\n
#         """)
#     st.plotly_chart(requests_fig)

st.header("USAGE METRICS")
col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("ℹ️ more info"):
        st.write("""
        Total Queries = The total number of queries across users that were received.\n
        Successful Queries = The total number of queries across users that were successfully processed. \n
        Failed Queries = The total number of queries across users that failed.
        """)
    st.plotly_chart(usage_requests_fig)
with col2:
    with st.expander("ℹ️ more info"):
        st.write("""
        Unique Users = Total number of unique User Ids that requested query responses.\n
        """)
    st.plotly_chart(uniques_users_fig)
with col3:
    with st.expander("ℹ️ more info"):
        st.write("""
        Chats per user = The average number of chat sessions that were triggered per user.\n
        Queries per user = The average number of queries requested per user.
        """)
    st.plotly_chart(per_user_fig)

st.header("COST METRICS")
col1, col2 = st.columns(2)

with col1:
    with st.expander("ℹ️ more info"):
        st.write("""
        Total Usage Cost = The total usage cost (LLM Cost + Embedding Cost)\n
        LLM Cost = The total cost incurred for using the LLMs at multiple stages of the RAG pipeline.\n
        Embedding Cost = The total cost incurred for using the Embedding models at multiple stages of the RAG pipeline.
        """)
    st.plotly_chart(overall_cost_fig)
with col2:
    with st.expander("ℹ️ more info"):
        st.write("""
        Input Tokens = The total number of input tokens that were used (prompt tokens)\n
        Output Tokens = The total number of output tokens that were used (completion tokens)\n
        Embedding Tokens = The total number of embedding tokens used for semantic similarity
        """)
    st.plotly_chart(tokens_fig)
    
with st.expander("ℹ️ more info"):
    st.write("""
    Cost per User = The average overall cost incurred per user.\n
    Cost per query = The average overall cost incurred per a user query.\n
    """)
    # Possible # of queries per DBU = The possible number of queries (approx) that can be made per unit DBU.

def wait_for_10s():
    import time
    time.sleep(10)

# col1, col2, col3 = st.columns(3)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(cost_per_user_fig)
with col2:
    BackgroundTasks(wait_for_10s())
    st.plotly_chart(cost_per_query_fig)
    
# with col3:
#     st.plotly_chart(queries_per_dbu_fig)


# st.write("### Sales Data Table")
# st.dataframe(df)
