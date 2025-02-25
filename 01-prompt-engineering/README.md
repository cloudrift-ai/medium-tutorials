# Setup

1. Create virtual environment: `python3 -m venv --prompt prompteng venv`
2. Activate virtual environment: `source venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`

# Usage

1. Run the ollama server.

```bash
docker run -p 11434:11434 -it --name ollama --rm ollama/ollama:latest
```

2. Download LLama3 model.

```bash
docker exec ollama ollama pull llama3
```

3. Start the app.

```bash
python app.py
```
