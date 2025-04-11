Creating a chatbot helper
=========================

Create and activate a virtualenv:

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
ollama pull gemma3:27b
# or for bigger model
# ollama pull llama3.3
ollama pull  mxbai-embed-large
```

Install requirements:

```shell
pip install -r requirements.txt
```

run script with:

```shell
streamlit run chat_bot.py
```

Then go to the link to see the chatbot interface
http://localhost:8501
