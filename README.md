# BookBot 📚🤖
BookBot is an innovative AI-driven application that enhances user interaction with books by providing detailed insights, summaries, and responses based on text analysis. It leverages advanced AI models from OpenAI, including GPT-3.5 Turbo for conversational responses and Pinecone for retrieving book information and recommendations.

## How It Works

- **Book Metadata Retrieval**: BookBot retrieves detailed information about books, including titles, authors, publication years, and summaries, using a custom book metadata API based on Pinecone vector database.
- **AI-Driven Interaction**: Users can interact with the bot by asking questions about specific books. BookBot uses GPT-3.5-turbo to understand the context of the questions and generate accurate and relevant answers.

## Built With

- **Streamlit** - For creating and sharing beautiful data apps quickly.
- **OpenAI GPT-3.5 Turbo** - For generating responses to user queries.
- **Pinecone** - Used to store books data in vector form and retrieve book information and recommendations based on vector score.

## Getting Started

### Prerequisites

- Python 3.8 or newer.
- An OpenAI API key.
- A Pinecone API key.
- Streamlit installed.

### Installation

Clone the repository:

```bash
git clone https://github.com/jeelkan/BookBot.git
```

Install required packages:

```bash
pip install -r requirements.txt
```

### Setting Up Environment Variables

Before running the application, you need to set up necessary environment variables. Specifically, you need to set your OpenAI API key to enable AI functionalities. Here’s how you can set it up based on your operating system:

For Windows
```bash
set OPENAI_API_KEY=your_openai_api_key_here
set PINECONE_API_KEY=your_pinecone_api_key_here
```

For macOS and Linux
```bash
export OPENAI_API_KEY=your_openai_api_key_here
export PINECONE_API_KEY=your_pinecone_api_key_here
```

Make sure to replace your_openai_api_key_here with your actual OpenAI API key.


### Run the Streamlit application:

```bash
streamlit run app.py
```

## Usage
Interact through the UI: Use the sidebar to search for books and view detailed metadata. Navigate to the interaction section to chat with BookBot about the book details.
Ask Questions or Get Summaries: You can ask specific questions about any book's content or get a summary of other books or authors.


## Author
[Jeel Kanzaria] - Initial work - jeelkan

## Acknowledgments
Thanks to OpenAI for providing the GPT and Pinecone for providing the vector database which power the core functionalities of this application.
Thanks to the Python and Streamlit communities for support and tools that make this app possible.

