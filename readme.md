FastAPI Chat Application

This FastAPI application provides endpoints to interact with OpenAI's GPT models, allowing for chat completions and handling image and text inputs for generating responses.

Requirements
- Python 3.9+
- Docker (for Docker deployment)
- OpenAI API key

Installation

Local Setup
git clone https://github.com/mcd0056/FastAPI---Chatgpt

Install dependencies:
- Create a virtual environment and activate it:

python -m venv venv
- source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install the required packages:
- pip install -r requirements.txt

Set up environment variables:
Create a .env file in the root directory of the project and add your OpenAI API key:
- OPENAI_API_KEY=your_openai_api_key_here


Docker Setup
Ensure Docker and Docker Compose are installed on your machine.

Build the Docker image:
docker-compose build

Run the container:
docker-compose up


Usage
Running Locally
To run the application locally:

cd services
cd fastapi 
uvicorn app:app --reload

The API will be available at http://127.0.0.1:8000.

Running with Docker
To start the application using Docker:

docker-compose up -d
The API will be available at http://localhost:8000.

Endpoints

POST /chat: For generating chat completions based on text input.
Request body example:

{
  "user_message": "Hello, assistant!",
  "model": "gpt-3.5-turbo"
}


POST /image_text_chat: For generating responses based on text and an image URL.
Request body example:
{
  "user_text": "What’s in this image?",
  "image_url": "http://example.com/image.jpg",
  "model": "gpt-4-vision-preview"
}

