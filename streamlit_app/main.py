import streamlit as st
from dotenv import load_dotenv
from app.engine.graph.graph import build_graph

load_dotenv()

#configuración de página
st.set_page_config(
    page_title="FinNotebook Agent",
    page_icon="icons/finotebook_agent_icon_v2.svg",
    layout="wide"
)

st.title("🏦 FinNotebook Agent")
st.caption("Asistente de documentación bancaria con IA")

#Streamlit usa st.session_state para mantener datos entre interacciones. El historial de chat se guarda así:
if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Escribe tu pregunta..."):
    # aquí dentro va todo lo que pasa cuando el usuario envía un mensaje
    # Mostrar mensaje
    with st.chat_message("human"):
        st.markdown(prompt)
    # Añadir al historial
    st.session_state.messages.append({"role": "human", "content": prompt})

    # Llamar al grafo
    graph = build_graph()
    result = graph.invoke({
        "question": prompt,
        "session_id": "default",
        "context": "",
        "answer": ""
    })

    # Mostrar respuesta
    with st.chat_message("assistant"):
        st.markdown(result["answer"])
        st.badge(f"Intención: {result['intent']}", icon="🎯")

    # Añadir respuesta al historial
    st.session_state.messages.append({"role": "assistant", "content": result["answer"]})