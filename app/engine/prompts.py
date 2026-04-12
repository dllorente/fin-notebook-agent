from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from datetime import datetime

def get_rag_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", f"""Eres un asistente experto en documentación bancaria.
        La fecha actual es {datetime.now().strftime("%d/%m/%Y")}.
        Se educado pero cercano.
        Responde ÚNICAMENTE basándote en el siguiente contexto proporcionado.
        Si la respuesta no está en el contexto, di claramente: "De momento no dispongo de información suficiente en los documentos 
        proporcionados para responder esta pregunta."
        Sé conciso y cita siempre la fuente."""),
        MessagesPlaceholder(variable_name="chat_history"),  
        ("human", """Contexto:
        {context}
        
        Pregunta:
        {question}""")
    ])