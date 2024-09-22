import os
import getpass
import subprocess
import streamlit as st
from sqlalchemy import create_engine
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv, set_key
from pathlib import Path

def load_env():
    env_path = Path(".env")
    load_dotenv(dotenv_path=env_path)

    if "GROQ_API_KEY" not in os.environ:
        groq_api_key = getpass.getpass("Enter your Groq API key: ")
        os.environ["GROQ_API_KEY"] = groq_api_key
        
        if not env_path.exists():
            env_path.touch()
        set_key(env_path, "GROQ_API_KEY", groq_api_key)
    else:
        groq_api_key = os.environ["GROQ_API_KEY"]
    
    return groq_api_key

groq_api_key = load_env()
engine = create_engine("sqlite:///sqlite.db")
history = SQLChatMessageHistory(session_id="history", connection=engine)

llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0.5,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=groq_api_key,
)

template_onion = """You're ONION, ONION Is An LNP (Language Natural Programmation) That Can 
Transform Simple Human Language Into Complex And Advanced C Code, You're The C Compiler, You Don't Have To Say Something, Go Ahead And Just Make The C Code Like An Compiler, Remember, Use Format Block C Code, Don't Talk In C Code Too, Just Follow The Rule: Don't Talk Something, Just Make The C Code For Client, ONION Is An LNP (Language Natural Programmation) That Can Transform Simple Human Language Into Complex And Advanced C Code, Remember, Don't Make Simple Or Basic C Code, You Can Make 100% Functional C Code, Don't use [```c and ``] and Don't Use C++/CPP'.

Task: {task}

{agent_scratchpad}

Answer: I will think step by step..."""

prompt_onion = ChatPromptTemplate.from_template(template_onion)
search = DuckDuckGoSearchRun()

onion_agent = create_tool_calling_agent(llm=llm, tools=[search], prompt=prompt_onion)

def process_input(task):
    onion_messages = [
        ("system", template_onion),
        ("human", task),
    ]

    ai_msg_onion = llm.invoke(onion_messages)
    debug_messages = [
        ("system", "You're a code reviewer and optimizer. Your task is to review and optimize the code provided without adding any comments. Focus on fixing errors and making the code efficient, Don't use [```c and ```] and Don't Use C++/CPP and Don't Say What You Changed Or Fixed.'"),
        ("human", ai_msg_onion.content),
    ]

    ai_msg_debug = llm.invoke(debug_messages)

    cleaned_code = ai_msg_debug.content.replace('```c', '').replace('```', '').strip()

    output_filename = "main.c"
    with open(output_filename, 'w') as file:
        file.write(cleaned_code)
    
    return cleaned_code, output_filename 

def compile_and_run_agent(code):
    compile_cmd = f"gcc main.c -o main"
    compile_result = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)

    if compile_result.returncode != 0:
        return None, compile_result.stderr  

    exec_result = subprocess.run("./main", capture_output=True, text=True)
    return exec_result.stdout if exec_result.returncode == 0 else exec_result.stderr, None

compiler_agent_template = """You are a compiler agent. Your job is to compile and run C code. 
The provided code is: {code}. 
Generate only the shell command to compile this code using gcc. Do not provide any explanations or additional text, Don't Use C++/CPP, Remember, the name of *.c file is main.c"""

def compile_agent(code):
    cleaned_code = code  
    compiler_prompt = compiler_agent_template.format(code=cleaned_code)
    compile_message = llm.invoke([("system", compiler_prompt)])

    compile_cmd = compile_message.content.strip()
    compile_result = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)

    if compile_result.returncode != 0:
        return compile_result.stderr, compile_message.content  

    exec_result = subprocess.run("./main", capture_output=True, text=True)
    return exec_result.stdout if exec_result.returncode == 0 else exec_result.stderr, compile_message.content

st.title("🖥️ ONION[X]")
st.write("Transform natural language into advanced C code!")

user_input = st.text_area("Type your request here", placeholder="Enter your task...")
submit_btn = st.button("Submit")

if submit_btn and user_input:
    with st.spinner("Processing..."):
        code, filename = process_input(user_input)
        exec_output, compile_message = compile_agent(code)

    st.subheader("Generated Code:")
    st.code(code, language='c')

    if compile_message:
        st.subheader("Compilation Message:")
        st.text(compile_message)

    if exec_output is not None:
        st.subheader("Execution Output:")
        st.text(exec_output)

    with open(filename, 'w') as f:
        f.write(code)
    
    st.download_button("Download Code File", data=open(filename, 'rb').read(), file_name=filename)

st.markdown("""
    ### About
    This application uses the ONION compiler to transform human language into complex C code.
    Feel free to input your tasks and see the magic happen!
""")

