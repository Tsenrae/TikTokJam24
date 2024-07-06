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

# User input for number of lines
num = 0
while not (1 <= int(num) <= 10):
    num = input("How many images would you like to generate? Range 1 - 10\n")


# User input to enter the story
user_story = input("Please type in the story you want to create illustrations for.\n")
while len(user_story) <= 100:
    user_story = input("Please enter a longer story.\n")

prompt = ChatPromptTemplate.from_messages(
    [
        ("ai", "You are a storybook illustrator. Summarise the story into " + num + " parts by generating short descriptive prompts of maximum 5 words that depict a scene to be used to generate " + num + " number of images on SplashAI based on the story given."),
        ("human","{input}")
    ]
)

chain = prompt | llm

response = chain.invoke({"input" : user_story})

response_text = response.content
response_text = response_text.split("\n")
response_text = [item.split('. ', 1)[1] if '. ' in item else item for item in response_text]

print(response_text)