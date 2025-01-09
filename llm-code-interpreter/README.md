## Description

This module enables LLMs to generate and execute Python code in isolated environments, including:

* Local execution.
* Dockerized execution.

## Usage
Provide a prompt in the UI to generate Python code.
Choose an execution environment:
* **Local** : Runs directly on the host system.
* **Docker** : Executes within an isolated Docker container.

## Setup

1. Install Ollama and prefered LLM using this [guide](https://github.com/Shishir-grez/AI-Sandbox/tree/main/ollama.md).

2. Run DockerFile 
   ```bash
   docker build -t ubuntu-python-app .
   ```
3. Create a volume to store logs, name the container "*exp-container*" and volume "*exp-volume*" :
    ```bash
    docker run -d --name exp-container -v exp-volume:/exp-volume ubuntu-python-app
    ```
4. Create python virtual enviornment :
   ```bash
    python -m venv env_name
   ```
5. Activate virtual enviornment :
   ```bash
   env_name\Scripts\activate
   ```
6. Install Dependencies : 
   ```bash
    pip install -r requirements.txt
   ```
7. Start Ollama : 
   ```bash
   ollama run llama3.2:3b
   ```
8. Run the Application :
   ```bash
    streamlit run app.py
   ```

>[!Tip]
> 
> if have any errors once check : 
>
> 1. If Docker Desktop is running 
> 2. If Docker container is running
> 3. If Ollama is running
> 4. If you have any issue regarding firewall for that code