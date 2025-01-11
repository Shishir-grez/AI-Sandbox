## Description

This module integrates ***LLMs*** with a ***Retrieval-Augmented Generation (RAG)*** pipeline, enabling responses grounded in user-provided documents. Features include :

* Context-based Q&A.
* Document vectorization with ChromaDB.
* Cross-encoder re-ranking for enhanced relevance.
## Usage
* Upload documents (PDF format) via the interface.
* Questions are answered by querying the vectorized context and utilizing LLMs for precise responses.

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