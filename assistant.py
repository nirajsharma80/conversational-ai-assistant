from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

def get_reply(history, instructions: str, model: str) -> str:
    messages=[SystemMessage(content=instructions)]
    for item in history[-12:]:
        if item["role"]=="user": messages.append(HumanMessage(content=item["content"]))
        elif item["role"]=="assistant": messages.append(AIMessage(content=item["content"]))
    response=ChatGoogleGenerativeAI(model=model,temperature=0.25).invoke(messages)
    return str(response.content)
