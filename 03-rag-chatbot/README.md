Creating a chatbot helper

In this tutorial I will show how to create a simple chatbot with RAG running on your local machine or on dedicated cloud server using free llm models.

First install requirements:
create a virtualenv:

```shell
python3 -m venv venv
source venv/bin/activate
```

Install ollama
```shell
curl -fsSL https://ollama.com/install.sh | sh
```
Download ollama model that we want to use
Add short description of available ollama models and which of them would be the best for this application and your computational resources

```shell
ollam pull qwen2.5:32b
```
Describe how simple RAG is implemented
Create a python file chat_bot.py

Start a vector database locally:
Install docker
```shell
docker run -d   -e POSTGRES_DB=ai   -e POSTGRES_USER=ai   -e POSTGRES_PASSWORD=ai   -e PGDATA=/var/lib/postgresql/data/pgdata   -v pgvolume:/var/lib/postgresql/data   -p 5532:5432   --name pgvector   phidata/pgvector:16
```

```python
import streamlit as st
from agno.agent import Agent
from agno.models.openai import OpenAIChat

from agno.models.ollama import Ollama
from agno.embedder.ollama import OllamaEmbedder
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.vectordb.pgvector import PgVector, SearchType


@st.cache_resource
def get_knowledge_base():
    db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
    embedder = OllamaEmbedder(id="mxbai-embed-large", dimensions=1024)
    knowledge_base = PDFUrlKnowledgeBase(
        urls=["https://cdn.1j1ju.com/medias/8d/c5/21-gloomhaven-rulebook.pdf"],
        vector_db=PgVector(table_name="gloomhaven", db_url=db_url, search_type=SearchType.hybrid, embedder=embedder),
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
    #model=OpenAIChat(id="gpt-4o"),
    #model=Ollama(id="qwen2.5:32b"),
    #model=Ollama(id="deepseek-r1:14b", options={"num_ctx": 131072}),
    model=Ollama(id="qwen2.5:32b", options={"num_ctx": 18192}),
    knowledge=get_knowledge_base(),
    add_context=True,
    add_references=True,
    description="You are an expert in the rules of the board game gloomhaven.",
    instructions=[
        "Use additional data provided for the corresponding rules.",
        #"If the question is better suited for the web, search the web to fill in gaps.",
        #"Prefer the information in your knowledge base over the web results."
        "Cite the rules book with the corresponding information at the end of the answer to a question"
    ],
    # Add a tool to search the knowledge base which enables agentic RAG.
    search_knowledge=False,
    # Add a tool to read chat history.
    #read_chat_history=True,
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

```


run script with:

```shell
streamlit run chat_bot.py
```

screenshot of the app running

add flag to agent to enable debug mode

debug_mode=True

When running ollama models with RAG it is important to specify a context size which we are doing by adding options={"num_ctx": 18192} to the model.
The default size 2048 is most often not enough for RAG applications.

Running chatbot on a remote server
If we want to use a bigger model our local machine might be not enough. The way to go would be to rent a machine to run this model.
There are two options of renting GPU enabled machines - virtual machine or docker container.
Virtual machine will allow you better flexibility for your experiments since you have a full access to the os and ports of the machine.
Running a docker container will allow you to deploy your application after the development stage was finished.

You can easily rent a GPU enabled virtual machine on neuralrack here:

Screenshots

After running machine and clicking connect you will see an ip address of the machine.
Connect to the machine using these instructions.
You may need to install virtual env package since it might not be installed by default on the VM.
```shell
sudo apt install python3.12-venv
```
Install all the necessary libraries listed in install section.

After connecting to the machine you may want to install and start jupyter lab to have an easy way to access the machine.
You can do it this way:
```shell
pip install jupyterlab
jupyter notebook --no-browser --port=8080 --ip=0.0.0.0
```
You need to add '--ip=0.0.0.0' flag to be able to access notebook on a remote server externally since by default all access outside if disabled.

Deploying chatbot into production

I am going to show how a simple way to deploy this chatbot in a single docker container.
If you want to create a docker container, you have to first install docker. To allow for gpu support in the container
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
Install the NVIDIA Container Toolkit⁠.


```dockerfile
FROM ollama/ollama
LABEL authors="cloudrift"
RUN nohup bash -c "ollama serve &" && sleep 5 && ollama pull llama3.1:8b
RUN mkdir chatbot
COPY ./run-app.sh /chatbot/run-app.sh
COPY ./app.py /chatbot/app.py
COPY ./requirements.txt /chatbot/requirements.txt
WORKDIR /chatbot
RUN chmod +x run-app.sh
RUN pip install -r requirements.txt
ENTRYPOINT ["./run-app.sh"]
```


```shell
streamlit run app.py
```
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
    | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
    | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
    | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

http://localhost:8501
