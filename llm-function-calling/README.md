## Description
This module uses LLMs with function-calling capabilities to perform specific operations based on user prompts. Key tools include : 

* Disk usage retrieval.
* Time zone-based time reporting.
  
## Usage

Enter a prompt in the UI. If a function is required (e.g., "What is the disk usage?"), the tool will execute and display the result.

Extend functionality by defining new tools in the code.

## Setup

1. Setup a python virtual enviornment :
   ```bash
   python -m venv env_name
   ```

2. Activate virtual enviornment :
    ```bash
    env_name\Scripts\activate
    ```
3. Install Dependencies :
    ```bash
    pip install -r requirements/requirements.txt
    ```
4. Start Ollama and run llama3.2:3b :
   ```bash
   ollama run llama3.2:3b
   ```
5. Start streamlit app :
    ```bash
    streamlit run app.py
    ```