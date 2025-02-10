# DocuBot
DocuBot: Your Document Assistant
=================================

Repository:
-----------
https://github.com/MElbahluan23/DocuBot

Overview
--------
DocuBot is an AI-powered chatbot that lets you upload one or multiple PDF documents and ask questions about their content. Using FastAPI, LangChain, and OpenAI’s language models, DocuBot extracts text from your PDFs and provides context-aware answers—all through a modern, responsive web interface.

Features:
- **PDF Upload:** Upload one or several PDF files at once. DocuBot extracts text from your documents and splits it into searchable chunks.
- **Intelligent Chat:** Ask questions about your uploaded documents and receive AI-generated, context-relevant answers.
- **Responsive UI:** A clean, mobile-friendly interface for a seamless user experience.
- **Dockerized Deployment:** Containerized setup using Docker ensures a hassle-free installation and deployment process.

Setup Instructions
------------------
1. **Clone the Repository:**
   Open your terminal and run:
   ```
    git clone https://github.com/MElbahluan23/DocuBot.git
    cd DocuBot
   ```
2. **Configure the Environment:**
Create a file named **.env** in the project root with the following content:
   ```
    OPENAI_API_KEY=your_openai_api_key_here
   ```
Replace `your_openai_api_key_here` with your actual OpenAI API key. This file securely stores your API key so that it isn’t hardcoded into the source code.

3. **Build and Run with Docker:**
DocuBot is designed to run in a Docker container. Follow these steps:

- **Build the Docker Image:**
  Open your terminal in the project directory and run:
  ```
  docker build -t docubot .
  ```

- **Run the Docker Container:**
  Once the image is built, run the container using the following command:
  ```
  docker run -p 8000:8000 –env-file .env docubot
  ```

4. **Access DocuBot:**
Open your web browser and navigate to [http://localhost:8000](http://localhost:8000) to interact with DocuBot.

API Endpoints (for Reference)
------------------------------
- **Upload PDFs:**
- **Single File:** `POST /upload`  
 Form Data: Key `file` (PDF files only)
- **Multiple Files:** `POST /upload-multiple`  
 Form Data: Key `files` (for multiple PDFs)

- **Chat with DocuBot:**
- **Endpoint:** `POST /chat`  
 Form Data: Key `question` (your query)

User Interface
--------------
DocuBot’s homepage includes:
- A PDF Upload section to add your document(s)
- A Chat section to ask questions and get responses based on the uploaded PDFs

Conclusion
----------
DocuBot simplifies document analysis by leveraging Docker for easy deployment. Just clone the repository, set your API key in a **.env** file, and run a couple of Docker commands. You’re ready to chat with your documents!

Enjoy using DocuBot!
