from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser, StrOutputParser
import openai
import os
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import BingImageCreator

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

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
# Remove headless mode so the user can interact with the browser
chrome_options.add_argument("--start-maximized")

# Initialize the WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Open Bing
driver.get("https://www.bing.com")

# Wait for the user to log in manually
print("Please log in to Bing manually and press Enter here when done...")
input()

# Get the cookie value
cookies = driver.get_cookies()
u_cookie = next((cookie['value'] for cookie in cookies if cookie['name'] == '_U'), None)
SRCHHPGUSR_cookie = next((cookie['value'] for cookie in cookies if cookie['name'] == 'SRCHHPGUSR'), None)

# Print the cookie value
print(f"_U cookie value: {u_cookie}")
print(f"SRCHHPGUSR cookie value: {SRCHHPGUSR_cookie}")

# Close the browser
driver.quit()

image_gen = BingImageCreator.ImageGen(u_cookie, SRCHHPGUSR_cookie)

for prompt in response_text:
    print(image_gen.get_images(prompt))


'''# Function to generate images using the DALL-E-3 model
def generate_images(prompt, api_key):
    api_url = 'https://api.openai.com/v1/images/generations'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        result = response.json()
        return result['data'][0]['url']
    else:
        print("Error:", response.status_code, response.text)
        return None

# Generate and print image URLs for each prompt
for idx, prompt in enumerate(response_text):
    image_url = generate_images(prompt, azure_api_key)
    if image_url:
        print(f"Image {idx + 1} URL:", image_url)'''