import streamlit as st
from openai import OpenAI
import os
from utils import text_to_embedding
from pinecone_config import init_pinecone

# Initialize OpenAI and Pinecone
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
index = init_pinecone()

language_dict = {
    'ar': 'Arabic', 'ca': 'Catalan', 'cy': 'Welsh', 'da': 'Danish', 'de': 'German',
    'el': 'Greek', 'en': 'English', 'eo': 'Esperanto', 'es': 'Spanish', 'fa': 'Persian (Farsi)',
    'fr': 'French', 'ga': 'Irish', 'gd': 'Scottish Gaelic', 'gl': 'Galician', 'hi': 'Hindi',
    'it': 'Italian', 'ja': 'Japanese', 'ko': 'Korean', 'la': 'Latin', 'ms': 'Malay',
    'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian',
    'ru': 'Russian', 'th': 'Thai', 'tl': 'Tagalog (Filipino)', 'vi': 'Vietnamese',
    'zh-CN': 'Chinese (Simplified)', 'zh-TW': 'Chinese (Traditional)'
}

def query_model(messages):
    if messages:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return completion.choices[0].message.content.strip()
    else:
        return "No message to process."

def get_book_metadata(user_query):
    query_vector = text_to_embedding(user_query)
    response = index.query(vector=query_vector, top_k=1, include_metadata=True)
    matches = response.get('matches', [])
    return matches[0]['metadata'] if matches else None

def get_similar_books(query_text, exclude_title):
    query_embedding = text_to_embedding(query_text)
    results = index.query(vector=query_embedding, top_k=10, include_metadata=True)
    filtered_results = [book for book in results['matches'] if book['metadata']['book_title'] != exclude_title]
    return filtered_results[:10]

def expand_summary(summary):
    # Instructional prompt to generate text in English
    prompt = f"Translate and expand the following summary into a detailed English summary of about 150-300 words:\n\n{summary}"

    expanded = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return expanded.choices[0].message.content.strip()

def cache_recommended_book_summaries(books):
    if "cached_recommended_books" not in st.session_state or st.session_state.cached_recommended_books != books:
        st.session_state.cached_recommended_books = books
        st.session_state.cached_summaries = [expand_summary(book['metadata']['Summary']) for book in books]

def send_message():
    if st.session_state.chat_input.strip():  # Ensure input is not just whitespace
        user_message = {"role": "user", "content": st.session_state.chat_input.strip()}
        st.session_state.messages.append(user_message)

        response = query_model(st.session_state.messages)
        assistant_message = {"role": "assistant", "content": response}
        st.session_state.messages.append(assistant_message)

        # Clear the input box after sending the message
        st.session_state.chat_input = ""

def main():
    st.sidebar.title("Current Book Details")
    user_query = st.sidebar.text_input("Search for a book:", "")

    if user_query and (user_query != st.session_state.get('last_query', '')):
        st.session_state.last_query = user_query
        st.session_state.book_metadata = get_book_metadata(user_query)
        recommended_books = get_similar_books(user_query, st.session_state.book_metadata['book_title'] if st.session_state.book_metadata else "")
        st.session_state.recommended_books = recommended_books
        cache_recommended_book_summaries(recommended_books)
        # Expand summary only when a new book is queried
        st.session_state.expanded_summary = expand_summary(st.session_state.book_metadata['Summary'])
        # Clear previous chat messages for the new book query
        st.session_state.messages = [{"role": "assistant", "content": "Hello, I'm BookBot! You can ask me anything about books and more!"}]

    st.title("BookBot: Book Information and Recommendation Chatbot")
    tabs = st.tabs(["Recommended Books", "Chat"])

    if st.session_state.get('book_metadata'):
        book_metadata = st.session_state.book_metadata
        st.sidebar.image(book_metadata['img_l'] if book_metadata['img_l'] else "default_image.jpg", caption=book_metadata['book_title'], use_column_width=True)
        st.sidebar.write("Title: " + book_metadata['book_title'])
        st.sidebar.write("Author: " + book_metadata['book_author'])
        if book_metadata['year_of_publication']:
             year_of_publication = int(float(book_metadata['year_of_publication']))
             st.sidebar.write(f"Year of Publication: {year_of_publication}")
        else:
             st.sidebar.write("Year of Publication: Unknown")
        st.sidebar.write("Publisher: " + book_metadata['publisher'])
        language = language_dict.get(book_metadata['Language'], 'Unknown Language')
        st.sidebar.write(f"Language: {language}")
        category = book_metadata.get('Category', 'Unknown Category')
        if category.startswith('[') and category.endswith(']'):
            category = category[1:-1]
        st.sidebar.write(f"Category: {category}")
        # Use cached expanded summary
        st.sidebar.write("Summary: " + st.session_state.expanded_summary)

    with tabs[0]:
        if st.session_state.get('recommended_books'):
            for index, book in enumerate(st.session_state.recommended_books):
                st.image(book['metadata']['img_l'] if book['metadata']['img_l'] else "default_image.jpg", caption=book['metadata']['book_title'])
                st.write("Title: " + book['metadata']['book_title'])
                st.write("Author: " + book['metadata']['book_author'])
                language_name = language_dict.get(book['metadata']['Language'], "Unknown Language")
                st.write(f"Language: {language_name}")
                st.write("Summary: " + st.session_state.cached_summaries[index])
                st.markdown("---")

    with tabs[1]:
        if "messages" not in st.session_state:
            if "messages" not in st.session_state:
                st.session_state.messages = [{"role": "assistant", "content": "Hello, I'm BookBot! You can ask me anything about books and more!"}]

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        st.text_input("Ask about books here:", value="", key="chat_input", on_change=send_message, args=())

if __name__ == "__main__":
    main()
