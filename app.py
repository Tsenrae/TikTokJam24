from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Import custom modules
from BingImageCreator import ImageGen
from llm import generate_prompts

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Global variable to store prompts
prompts = []

webdriver_instance = None

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/runllm', methods=['POST'])
def run_llm():
    global prompts
    num_images = request.form['num_images']
    user_story = request.form['user_story']

    if not (1 <= int(num_images) <= 10):
        return "Please enter a number between 1 and 10."
    
    if len(user_story) <= 100:
        return "Please enter a longer story."

    prompts = generate_prompts(user_story, num_images)

    return redirect(url_for('instructions'))

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/submit', methods=['POST'])
def start_login():
    global webdriver_instance
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://www.bing.com")
    webdriver_instance = driver

    return redirect(url_for('check_login'))

@app.route('/check_login', methods=['GET', 'POST'])
def check_login():
    global webdriver_instance
    driver = webdriver_instance

    cookies = driver.get_cookies()
    u_cookie = next((cookie['value'] for cookie in cookies if cookie['name'] == '_U'), None)
    SRCHHPGUSR_cookie = next((cookie['value'] for cookie in cookies if cookie['name'] == 'SRCHHPGUSR'), None)

    if u_cookie and SRCHHPGUSR_cookie:
        driver.quit()
        return redirect(url_for('generate_images', u_cookie=u_cookie, srchhpgusr_cookie=SRCHHPGUSR_cookie))
    else:
        return "Please log in to Bing."

@app.route('/generate_images')
def generate_images():
    u_cookie = request.args.get('u_cookie')
    srchhpgusr_cookie = request.args.get('srchhpgusr_cookie')

    image_gen = ImageGen(u_cookie, srchhpgusr_cookie)
    image_links = []

    for prompt in prompts:
        normal_image_links = image_gen.get_images(prompt)
        normal_image_links = [i for i in normal_image_links if ".js" not in i and ".svg" not in i]
        if normal_image_links:
            image_links.append(normal_image_links[0])  # Get the first image URL for each prompt

    return render_template('display_images.html', image_links=image_links)

if __name__ == '__main__':
    app.run(debug=True)
