# Story Image Generator

This application generates images based on a user-provided story using OpenAI's GPT model and Bing Image Creator. 

## Setup

### Prerequisites

- Python 3.6 or higher
- Google Chrome browser
- Git
- Azure API Key from OpenAI

### Installation

1. **Clone the repository:**

    Clone the repo and follow the instructions below to set up.

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file in the root directory of the project and add your API keys and other necessary environment variables. You can use the `.env.example` file as a reference:**

    ```bash
    cp .env.example .env
    ```

5. **Open the `.env` file and add your API keys and other environment variables:**

    ```bash
    AZURE_API_KEY='replace_with_your_azure_api_key'
    AZURE_ENDPOINT='replace_with_your_azure_endpoint'
    ```

### Running the Application

1. **Run the Flask application:**

    ```bash
    python app.py
    ```

2. **Open your browser (Google Chrome recommended) and navigate to `http://localhost:5000`.**

3. **Follow the instructions on the webpage to generate images based on your story.**

### Project Structure

- `app.py`: The main Flask application file.
- `authcheck.py`: Handles Bing login and cookie extraction.
- `BingImageCreator.py`: Contains the Bing Image Creator integration.
- `llm.py`: Handles prompt generation using OpenAI's GPT model.
- `templates/`: Contains the HTML templates.
  - `home.html`: The homepage where users input the number of images and their story.
  - `instructions.html`: Instructions for logging into Bing.
  - `display_images.html`: Displays the generated images.
- `.env.example`: Example environment file to help users set up their own `.env`.

### Acknowledgements
This project makes use of the following third-party library:
- [Bing Image Creator](https://github.com/acheong08/BingImageCreator) - The use of their API to access Bing's AI image generator.
- [OpenAI](https://www.openai.com) - The use in code for generating text prompts based on the story input.