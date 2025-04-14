
from dotenv import load_dotenv
import os
import requests
from databricks import sdk
 
cfg = sdk.config.Config()

def fetch_dashboard_metrics(start_date: str, end_date: str):
    url = (
        "https://aagchatbot-api-backend-1970155331536418.18.azure.databricksapps.com/"
        f"api/v1/opsdb/fetch_metrics?start_date={start_date}&end_date={end_date}"
    )
    API_KEY = os.getenv("API_KEY")
    headers = {
        "accept": "application/json",
        "api-key": API_KEY,
        "Content-Type": "application/json"
    }
    headers.update(cfg.authenticate())
    response = requests.get(url, headers=headers)
    print ("Response :",response.json())
    if isinstance(response, str):
        raise ValueError(f"API Error: {response}")

    metrics = response.json()

    data = {
        "dates": metrics["dates"],

        # Performance Metrics
        "rag_latency": metrics["performance_metrics"]["avg_rag_latency_ms"],
        "response_time": metrics["performance_metrics"]["avg_response_latency_ms"],
        "overall_error_rate": metrics["performance_metrics"]["error_rates"],
        "llm_error_rate": metrics["performance_metrics"]["llm_error_rates"],

        # Usage Metrics
        "successful_queries": metrics["usage_metrics"]["successful_reqs"],
        "failed_queries": metrics["usage_metrics"]["failure_reqs"],
        "total_queries": metrics["usage_metrics"]["total_reqs"],
        "unique_users": metrics["usage_metrics"]["unique_users"],
        "chats_per_user": metrics["usage_metrics"]["chats_per_user"],
        "queries_per_user": metrics["usage_metrics"]["queries_per_user"],

        # Cost Metrics
        "input_tokens": metrics["cost_metrics"]["tot_prompt_tokens"],
        "output_tokens": metrics["cost_metrics"]["tot_completion_tokens"],
        "llm_cost": metrics["cost_metrics"]["tot_llm_cost"],
        "embedding_cost": metrics["cost_metrics"]["tot_embedding_cost"],
        "total_usage_cost": metrics["cost_metrics"]["tot_llm_embed_cost"],
        "cost_per_user": metrics["cost_metrics"]["avg_cost_per_user"],
        "cost_per_query": metrics["cost_metrics"]["avg_cost_per_query"],
    }

    return data