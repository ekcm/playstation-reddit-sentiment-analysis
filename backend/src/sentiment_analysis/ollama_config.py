from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

# this is used to test if ollama is correctly configured

local_llm = "llama3.2"
llm = ChatOllama(
    model=local_llm,
    temperature=0,
)

llm_json_mode = ChatOllama(
    model=local_llm,
    temperature=0,
    format="json"
)

# Prompt
instructions = "You are a helpful assistant."

llm_chat = llm.invoke(
    [SystemMessage(content=instructions)]
    + [
        HumanMessage(content="Why is the sky blue?")
    ]
)

print(llm_chat)

llm_json_chat = llm_json_mode.invoke(
    [SystemMessage(content=instructions)]
    + [
        HumanMessage(content="Is the sky blue? Return JSON with a single key, that is 'yes' or 'no'")
    ]
)

print(llm_json_chat)

