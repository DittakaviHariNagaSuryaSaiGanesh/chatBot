# Imports
import os 
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
import streamlit as st
from streamlit_chat import message


# Set API keys and the models to use
API_KEY = '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'
model_id = "gpt-3.5-turbo"

# Add your openai api key for use
os.environ["OPENAI_API_KEY"] = API_KEY

# Load PDF document
# Langchain has many document loaders 
# We will use their PDF load to load the PDF document below
loaders = PyPDFLoader(r"C:\Users\sharb\Downloads\anil kumar_.pdf")

# Create a vector representation of this document loaded
index = VectorstoreIndexCreator().from_loaders([loaders])

# Setup streamlit app

# Display the page title and the text box for the user to ask the question
st.title('🦜 Query your PDF document ')
prompt = st.text_input("Enter your question to query your PDF documents")

# Display the current response. No chat history is maintained

if prompt:
    # Get the resonse from LLM
    # We pass the model name (3.5) and the temperature (Closer to 1 means creative resonse)
    # stuff chain type sends all the relevant text chunks from the document to LLM

    response = index.query(llm=OpenAI(model_name="gpt-3.5-turbo", temperature=0.2), question = prompt, chain_type = 'stuff')

    # Write the results from the LLM to the UI
    st.write("<b>" + prompt + "</b><br><i>" + response + "</i><hr>", unsafe_allow_html=True )

if prompt:
    # Get the resonse from LLM
    # We pass the model name (3.5) and the temperature (Closer to 1 means creative resonse)
    # stuff chain type sends all the relevant text chunks from the document to LLM

    response = index.query(llm=OpenAI(model_name="gpt-3.5-turbo", temperature=0.2), question = prompt, chain_type = 'stuff')

    # Write the results from the LLM to the UI
    # Display the response in a message format
    # User input will appear on the right which is controlled by the property is_user=True
    message(prompt, is_user=True)
    message(response,is_user=False )

#------------------------------------------------------------------
# Save history

# This is used to save chat history and display on the screen
if 'answer' not in st.session_state:
    st.session_state['answer'] = []

if 'question' not in st.session_state:
    st.session_state['question'] = []    

#------------------------------------------------------------------
# Display the current response. Chat history is displayed below

if prompt:
    # Get the resonse from LLM
    # We pass the model name (3.5) and the temperature (Closer to 1 means creative resonse)
    # stuff chain type sends all the relevant text chunks from the document to LLM
    response = index.query(llm=OpenAI(model_name = model_id, temperature=0.2), question = prompt, chain_type = 'stuff')

    # Add the question and the answer to display chat history in a list
    # Latest answer appears at the top
    st.session_state.question.insert(0,prompt  )
    st.session_state.answer.insert(0,response  )
    
    # Display the chat history
    for i in range(len( st.session_state.question)) :
        message(st.session_state['question'][i], is_user=True)
        message(st.session_state['answer'][i], is_user=False)