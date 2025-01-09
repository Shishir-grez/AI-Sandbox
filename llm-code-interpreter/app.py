import os
import re
import subprocess
import tempfile
from pathlib import Path
import docker
import streamlit as st
import ollama

st.set_page_config(page_title="Code Interpreter")
st.header("Code Interpreter")

system_prompt = ""

help_text = """
⚡️ Environment to execute the generated code.

⚠️ Be careful running arbitrary code on your local machine
- None: Do not run the generated code.
- docker: Run code inside a docker container.
- local: Run code directly on your local machine.
"""

execution_env = st.selectbox(
    "Select environment for Code Execution: ",
    ("None", "docker", "local"),
    help=help_text,
)

user_prompt = st.text_area("**Prompt:**", placeholder="Enter your prompt...")
run = st.button("Run")

local_execution_prompt = """
You are an intelligent AI agent designed to generate accurate python code.
Here are your STRICT instructions:
- If the question does not require writing code, provide a clear and concise answer without generating any code.
- Whatever question is asked to you generate just the python code based on that and it's important that you just generate the code, no explanation of the code before or after.
- Think step by step how to solve the problem before you write the code.
- If the code involves doing system level tasks, it should have the code to identify the platform, the $HOME directory to make sure the code execution is successful.
- Code should be inside of the ```python ``` block.
- Make sure all the imports are always there to perform the task.
- At the end of the generated code, always include a line to run the generated function.
- The code should print output in a human-readable and understandable format.
- If you are generating charts, graphs or anything visual, convert them to image and save it to the /tmp location and return as well as print just the name of the image file path.
"""

docker_execution_prompt = """
You are an intelligent AI agent designed to generate accurate python code.
Here are your STRICT instructions:
- If the question does not require writing code, provide a clear and concise answer without generating any code.
- Whatever question is asked to you generate just the python code based on that and it's important that you just generate the code, no explanation of the code before or after.
- Think step by step how to solve the problem before you write the code.
- If the code involves doing system level tasks, it should have the code to identify the platform, the $HOME directory to make sure the code execution is successful.
- Code should be inside of the ```python ``` block.
- Make sure all the imports are always there to perform the task.
- At the end of the generated code, always include a line to run the generated function.
- The code should print output in a human-readable and understandable format.
- If you are generating charts, graphs or anything visual, convert them to image and save it to the /app location and return as well as print just the name of the image file without path.
"""

if execution_env == "docker":
    system_prompt = (docker_execution_prompt)
else:
    system_prompt = (local_execution_prompt)


def get_code_group(llm_response: str) -> str | bool:
    """Extracts Python code from a markdown-formatted LLM response.

    Args:
        llm_response: A string containing the full response from the LLM, potentially
            containing Python code blocks.

    Returns:
        str: The extracted Python code if found.
        bool: False if no Python code block is found.
    """
    code_match = re.search(r"```python\n(.*?)```", llm_response, re.DOTALL)
    print(">>> Code Match: ", code_match)
    if not code_match:
        print(">>> No Python code found in the response.")
        return False

    return code_match.group(1)


def execute_local(temp_file_path: str) -> str:
    """Executes a Python script locally and returns its output.

    Runs the given Python script file using python3.10 interpreter in a subprocess
    with a x second timeout. Captures and returns stdout/stderr.

    Args:
        temp_file_path: Path to the temporary Python script file to execute.

    Returns:
        str: The stdout output if execution was successful, stderr if there were errors,
            or a timeout message if execution exceeded 10 seconds.

    Raises:
        subprocess.TimeoutExpired: If script execution takes longer than 10 seconds.

    Note:
        The temporary file is deleted after execution regardless of success/failure.
    """
    try:
        result = subprocess.run(
            ["C:\\Users\\narkh\\AppData\\Local\\Programs\\Python\\Python311\\python.exe", temp_file_path], capture_output=True, text=True, timeout=10
        )
        print(">>> Running code completed!")
        return result.stdout if result.returncode == 0 else result.stderr
    except subprocess.TimeoutExpired:
        return ">>> Execution timed out."
    finally:
        os.unlink(temp_file_path)

def execute_docker(temp_file_path: str) -> str:
    """Executes a Python script in an existing Docker container using Docker CLI.

    Args:
        temp_file_path: Path to the temporary Python script file to execute.

    Returns:
        str: The stdout output from the container if execution was successful,
            or an error message if container execution failed.

    Note:
        The temporary file is deleted after execution regardless of success/failure.
    """
    container_name = "exp-container"  # Replace with your container name or ID
    script_name = Path(temp_file_path).name
    destination_path = f"/exp-volume/{script_name}"

    try:
        # Ensure the /exp-volume directory exists in the container
        subprocess.run(
            ["docker", "exec", "exp-container", "mkdir", "-p", "/exp-volume"],
            check=True,
            text=True,
            capture_output=True
        )

        # Copy the script to the container
        subprocess.run(
            ["docker", "cp", temp_file_path, f"{container_name}:{destination_path}"],
            check=True,
            text=True,
            capture_output=True
        )

        # execute the script inside the container
        command = f"python3 {destination_path}"
        
        wrapped_command = (
            f"({command}) 2>&1 | tee -a /var/log/exec_commands.log"
        )
        
        # Run the command inside the container
        result = subprocess.run(
            ["docker", "exec", container_name, "sh", "-c", wrapped_command],
            text=True,
            capture_output=True
        )
        
        if result.returncode == 0:
            # Success: Return stdout
            return f"{result.stdout.strip()}"
        else:
            # Failure: Return stderr with an error message
            return f"{result.stderr.strip()} (Exit code: {result.returncode})"
    except subprocess.CalledProcessError as e:
        # Handle unexpected subprocess errors
        return f"Execution failed with an exception: {str(e)}"

    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)


if run:
   
    response = ollama.chat(
        model="llama3.2:3b",
        stream=False,
        messages=[
            {
                "role": "system",
                "content": system_prompt ,
            },
            {
                "role": "user",
                "content": f"Question: {user_prompt}",
            },
        ],
    )  
    
    # print(response["message"]["content"])
    
    
    
    code = get_code_group(response["message"]["content"])
    if response and code:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name
            print(f">>> Temp file path is : {temp_file_path}")

        executed_result = None
        if execution_env == "local":
            print(">>> Executing in Local Machine!")
            executed_result = execute_local(temp_file_path)
        elif execution_env == "docker":
            print(">>> Executing in Docker!")
            executed_result = execute_docker(temp_file_path)

        if executed_result and any(ext in executed_result for ext in (".png", ".jpg")):
            if execution_env == "local":
                st.image(executed_result.strip())
            else:
                st.image(f"{os.path.dirname(temp_file_path)}/{executed_result.strip()}")
        else:
            st.write(executed_result)
