FROM ollama/ollama
LABEL authors="cloudrift"

RUN apt update && apt upgrade -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install python3.10 python3-pip python3.10-venv -y

RUN nohup bash -c "ollama serve &" && sleep 5 && ollama pull gemma3:27b
RUN nohup bash -c "ollama serve &" && sleep 5 && ollama pull  mxbai-embed-large
RUN mkdir /chatbot
WORKDIR /chatbot
COPY ./run_app.sh .
COPY ./app.py .
COPY ./requirements.txt .
RUN chmod +x run_app.sh
RUN python3.10 --version
RUN python3.10 -m venv /opt/venv/
ENV PATH="/opt/venv/bin:$PATH"
RUN python --version
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["./run_app.sh"]
