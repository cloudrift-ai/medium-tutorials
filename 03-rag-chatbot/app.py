import streamlit as st
from agno.agent import Agent
from agno.embedder.ollama import OllamaEmbedder
from agno.models.ollama import Ollama
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.vectordb.lancedb import LanceDb, SearchType

# nomic-embed-text
# mxbai-embed-large
# bge-m3
# snowflake-arctic-embed

@st.cache_resource
def get_knowledge_base():
    embedder = OllamaEmbedder(id="mxbai-embed-large", dimensions=1024)
    vector_db = LanceDb(
        table_name="gloomhaven",
        uri="/tmp/lancedb",
        search_type=SearchType.hybrid,
        embedder=embedder
    )
    knowledge_base = PDFUrlKnowledgeBase(
        urls=["https://cdn.1j1ju.com/medias/8d/c5/21-gloomhaven-rulebook.pdf"],
        vector_db=vector_db
    )
    # Load the knowledge base on the first run
    knowledge_base.load(upsert=True)
    return knowledge_base


def stream_response(agent, prompt):
    response = agent.run(prompt, stream=True)
    for chunk in response:
        yield chunk.content

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'agent' not in st.session_state:
    st.session_state.agent = agent = Agent(
    model=Ollama(id="gemma3:27b", options={"num_ctx": 16192}),
    knowledge=get_knowledge_base(),
    add_context=True,
    add_references=True,
    description="You are an expert in the rules of the board game gloomhaven.",
    instructions=[
        "Use additional data provided for the corresponding rules.",
        "Cite the rules book with the corresponding information at the end of the answer to a question"
    ],
    search_knowledge=False,
    add_history_to_messages=True,
    num_history_responses=10,
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
    )

agent = st.session_state.agent

st.title("Chat with expert Agent")

prompt = st.chat_input("Your question")

if prompt:
    st.session_state.messages.append({'role': 'user', 'text': prompt})

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message['text'])

    with st.chat_message('assistant'):
        response = st.write_stream(stream_response(agent, prompt))
        st.session_state.messages.append({'role': 'assistant', 'text': response})
