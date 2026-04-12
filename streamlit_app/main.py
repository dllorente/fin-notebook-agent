import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langsmith import traceable

from app.engine.graph.graph import build_graph

load_dotenv()

st.set_page_config(
    page_title="FinNotebook Agent",
    page_icon="icons/finotebook_agent_icon_v2.svg",
    layout="wide",
)

st.title("🏦 FinNotebook Agent")
st.caption("Asistente de documentación bancaria con IA")

with st.sidebar:
    st.subheader("⚙️ Configuración")
    agent_mode = st.radio("Modo del agente:", ["Grafo estático", "Agente ReAct"], index=1)


@traceable(name="streamlit_ask", metadata={"version": "0.6.0", "interface": "streamlit"})
def invoke_graph(question: str, messages: list) -> dict:
    graph = build_graph()
    return graph.invoke(
        {
            "question": question,
            "intent": "",
            "session_id": "default",
            "context": "",
            "answer": "",
            "messages": messages,
        }
    )


if "messages" not in st.session_state:
    st.session_state.messages = []
if "metadata" not in st.session_state:
    st.session_state.metadata = []

for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and i // 2 < len(st.session_state.metadata):
            meta = st.session_state.metadata[i // 2]
            st.badge(f"Intención: {meta['intent']}", icon="🎯")
            if meta.get("tools_used"):
                st.caption(f"🔧 Tools usadas: {', '.join(meta['tools_used'])}")

if prompt := st.chat_input("Escribe tu pregunta..."):
    with st.chat_message("human"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "human", "content": prompt})

    # Llamar al agente según modo
    if agent_mode == "Agente ReAct":
        from app.engine.react_agent import build_react_agent

        agent = build_react_agent()
        result_raw = agent.invoke({"messages": [HumanMessage(content=prompt)]})
        # Extraer tools usadas
        tools_used = [msg.name for msg in result_raw["messages"] if hasattr(msg, "name") and msg.name is not None]
        result = {
            "answer": result_raw["messages"][-1].content,
            "intent": "react",
            "tools_used": tools_used,
        }
    else:
        result = invoke_graph(
            question=prompt,
            messages=[
                (HumanMessage(content=m["content"]) if m["role"] == "human" else AIMessage(content=m["content"]))
                for m in st.session_state.messages
            ],
        )

    with st.chat_message("assistant"):
        st.markdown(result["answer"])
        st.badge(f"Intención: {result['intent']}", icon="🎯")
        # Mostrar tools usadas si es ReAct
        if agent_mode == "Agente ReAct" and "tools_used" in result:
            st.caption(f"🔧 Tools usadas: {', '.join(result['tools_used'])}")
    st.session_state.messages.append({"role": "assistant", "content": result["answer"]})

    # Guardar en historial
    st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
    st.session_state.metadata.append({"intent": result["intent"], "tools_used": result.get("tools_used", [])})
