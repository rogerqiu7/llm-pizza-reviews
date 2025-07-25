# use an official Python base image
FROM python:3.11-slim

# set environment variables, prevent creation of pyc, print outputs immediately, and set Ollama base URL
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV OLLAMA_BASE_URL=http://localhost:11434
# ollama runs of a server, and listens to port 11434 by default, this tells langchain where to send requests

# set the working directory, this is where all commands will be run
WORKDIR /app

# install system dependencies including curl
RUN apt-get update && \
    apt-get install -y curl procps && \
    rm -rf /var/lib/apt/lists/*

# install Ollama using curl
RUN curl -fsSL https://ollama.com/install.sh | sh

# copy requirements first for better Docker layer caching
COPY requirements.txt .

# install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy project files
COPY . .

# make the entrypoint script executable so it can be run when the container starts
RUN chmod +x entrypoint.sh

# define the default command to run when the container starts; this launches Ollama, waits for readiness, pulls models, and starts the app
CMD ["/app/entrypoint.sh"]