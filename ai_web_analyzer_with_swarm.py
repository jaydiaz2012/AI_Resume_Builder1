import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import openai
from openai import ChatCompletion
from openai_swarm import SwarmAgent

# Configure API Keys
OPENAI_API_KEY = "" 
openai.api_key = OPENAI_API_KEY

# Load dataset
def load_dataset(file):
    try:
        return pd.read_csv(file)
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None

# Analyze dataset
def analyze_dataset(df):
    summary = {
        "overview": df.describe(include="all").to_dict(),
        "null_values": df.isnull().sum().to_dict(),
        "correlations": df.corr().to_dict(),
    }
    return summary

def generate_web_insights(df):
    web_insights = {
        'source_pageviews': df.groupby('source')['pageviews'].sum(),
        'source_visits': df.groupby('source')['visits'].sum(),
        'source_transactions': df.groupby('source')['transactions'].sum(),
        'source_product_click: df.groupby('source')['productClick'].sum()
    }
    return web_insights

def generate_web_visuals(df):
    visualizations = {}
    
    # Page Views Distribution
    plt.figure(figsize=(10, 6))
    sns.lineplot(df, x="source", y="pageviews")
    plt.title("Page Views Distribution")
    visualizations['page_views_distribution'] = plt.gcf()   
    plt.close()

    # Visits Distribution
    plt.figure(figsize=(10, 6))
    sns.lineplot(df, x="source", y="visits")
    plt.title("Visits Distribution")
    visualizations['visits_distribution'] = plt.gcf()
    plt.close()

    # Transactions Trends
    plt.figure(figsize=(10, 6))
    sns.lineplot(df, x="source", y="transactions")
    plt.title("Transactions Trends")
    visualizations['transactions_trends'] = plt.gcf()
    plt.close()

    # Product Click Trends
    plt.figure(figsize=(10, 6))
    sns.lineplot(df, x="source", y="productClick")
    plt.title("Product Clicks Trends")
    visualizations['product_click_trends'] = plt.gcf()
    plt.close()
    
    return visualizations
    
web_analytics_agent = Agent(
    name="Web Analyst Agent",
    model="gpt-4o-mini",
    instructions="You are a web analyst agent that cleans the dataset and report on the statistical summary of the dataset",
    functions=[analyze_dataset],
)

web_insights_agent = Agent(
    name="Web Insights Agent",
    model="gpt-4o-mini",
    instructions="""You are a Web Insights Agent that provide insights about the data provided and summarize the insights from other agents, including actionable recommendations"
    functions=[generate_web_insights]
)

web_insights_visuals_agent = Agent(
    name="Web_Visuals_Agent",
    model="gpt-4o-mini",
    instructions="""You are a data visualization expert that create visualizations on a given datase and gives summary of the data visuals",
    fuctions=[generate_web_visuals]
)

if __name__ == "__main__":
    client = Swarm()
    
    web_analytics_response = client.run(
        agent=web_analytics_agent,
        messages=[{
            "role": "user", 
            "content": "Please clean and analyze my dataset."
        }]
    )
    
    print("\nWeb Analytics Results:")
    print(web_analytics_response.messages[-1]["content"]) 
  
    web_insights_response = client.run(
        agent=web_insights_agent,
        messages=[{
            "role": "user", 
            "content": "Please provide insights based from my dataset."
        }]
    )
    
    print("\nWeb Insights Results:")
    print(web_insights.messages[-1]["content"])  

    web_insights_visuals_response = client.run(
        agent=web_insights_visuals_agent,
        messages=[{
            "role": "user", 
            "content": "Please provide data visualizations from my dataset."
        }]
    )
    
    print("\nWeb Analytics Results:")
    print(web_insights_visuals_response.messages[-1]["content"])  
  
# Advanced analysis using Swarm
def advanced_analysis(df):
    try:
        prompt = (
            "Perform clustering, detect anomalies, and provide predictive trends "
            f"on this dataset:\n{df.to_csv(index=False)}"
        )
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a data analysis assistant using Swarm."},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message['content']
    except Exception as e:
        st.error(f"Error performing advanced analysis: {e}")
        return None

# Generate business insights
def generate_insights(summary, model):
    prompt = (
        f"Here is the dataset summary:\n{summary}\n"
        "Generate actionable business insights from the above dataset."
    )
    response = model.create(
        engine="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a data analyst AI."},
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message['content']

# Generate a report
def generate_report(insights, advanced_analysis_result, file_path="report.txt"):
    with open(file_path, "w") as file:
        file.write("Automated Business Insights Report\n")
        file.write("=" * 50 + "\n\n")
        file.write("**Insights:**\n")
        file.write(insights + "\n\n")
        file.write("**Advanced Analysis:**\n")
        file.write(advanced_analysis_result + "\n")
    return file_path
