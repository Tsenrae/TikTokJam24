from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv() 
azure_api_key = os.getenv("AZURE_API_KEY") 
azure_endpoint = os.getenv("AZURE_ENDPOINT") 
 
llm = AzureChatOpenAI( 
    openai_api_version="2024-02-01", 
    deployment_name="gpt-35-turbo", 
    openai_api_key=azure_api_key, 
    azure_endpoint=azure_endpoint, 
)

response = llm.invoke("whats up gang")

print(response)
