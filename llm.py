from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser, StrOutputParser
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

num = input("How many images would you like to generate?")


prompt = ChatPromptTemplate.from_messages(
    [
        ("ai", "You are a storybook illustrator. Summarise the story into " + num + " parts by generating short descriptive prompts of maximum 5 words that depict a scene to be used to generate " + num + " number of images on SplashAI based on the story given."),
        ("human","{input}")
    ]
)

chain = prompt | llm

response = chain.invoke({"input" : "On a stormy night, Lily found an old, dusty key hidden in her grandmother's attic. Curiosity piqued, she unlocked a forgotten trunk, revealing a map to buried treasure. With a determined heart and a flashlight, she embarked on an adventure, discovering not gold, but her family's lost legacy."})

response_text = response.content
response_text = response_text.split("\n")
response_text = [item.split('. ', 1)[1] if '. ' in item else item for item in response_text]

print(response_text)