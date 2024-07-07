import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables from .env file
load_dotenv()

# Retrieve API key and endpoint from environment variables
azure_api_key = os.getenv("AZURE_API_KEY")
azure_endpoint = os.getenv("AZURE_ENDPOINT")

# Initialize the AzureChatOpenAI instance
llm = AzureChatOpenAI(
    openai_api_version="2024-02-01",
    deployment_name="gpt-35-turbo",
    openai_api_key=azure_api_key,
    azure_endpoint=azure_endpoint,
)

# Function to generate prompts based on user input and number of images
def generate_prompts(user_story, num_images):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("ai", f"You are a storybook illustrator. Summarise the story into {num_images} parts by generating short descriptive prompts of maximum 5 words that depict a scene to be used to generate {num_images} number of images on SplashAI based on the story given."),
            ("human", "{input}")
        ]
    )
    chain = prompt | llm
    response = chain.invoke({"input": user_story})

    response_text = response.content.split("\n")
    response_text = [item.split('. ', 1)[1].replace(' ', '+').replace("'", '+').replace(":", "+") if '. ' in item else item for item in response_text]

    return response_text