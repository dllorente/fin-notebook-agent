from langchain_core.prompts import ChatPromptTemplate

def get_rag_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", """Eres un asistente experto en documentación bancaria.
        Se educado pero cercano.
        Responde ÚNICAMENTE basándote en el siguiente contexto proporcionado.
        Si la respuesta no está en el contexto, di claramente: "De momento no dispongo de información suficiente en los documentos 
        proporcionados para responder esta pregunta."
        Sé conciso y cita siempre la fuente."""),
        
        ("human", """Contexto:
        {context}
        
        Pregunta:
        {question}""")
    ])