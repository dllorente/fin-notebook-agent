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
    agent_mode = st.radio(
        "Modo del agente:",
        ["Grafo estático", "Agente ReAct", "Dynamic agent"],
        index=0,
    )

MODE_MAP = {
    "Grafo estático": "rag",
    "Agente ReAct": "react",
    "Dynamic agent": "dynamic",
}


@traceable(name="streamlit_ask", metadata={"version": "0.7.0", "interface": "streamlit"})
def invoke_graph(question: str, messages: list, engine_mode: str) -> dict:
    graph = build_graph()
    return graph.invoke(
        {
            "question": question,
            "intent": "",
            "session_id": "default",
            "context": "",
            "answer": "",
            "messages": messages,
            "engine_mode": engine_mode,
        }
    )


def extract_tools_used(messages) -> list[str]:
    tools_used = []

    for msg in messages:
        if hasattr(msg, "name") and msg.name:
            tools_used.append(msg.name)

    return list(dict.fromkeys(tools_used))


def normalize_result(answer: str, intent: str, tools_used: list[str]) -> dict:
    return {
        "answer": answer,
        "intent": intent,
        "tools_used": tools_used,
    }


if "messages" not in st.session_state:
    st.session_state.messages = []

if "metadata" not in st.session_state:
    st.session_state.metadata = []

for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant" and i // 2 < len(st.session_state.metadata):
            meta = st.session_state.metadata[i // 2]
            st.badge(f"Intención: {meta.get('intent', 'unknown')}", icon="🎯")
            st.caption(f"🧠 Motor usado: {meta.get('engine_mode', 'unknown')}")

            if meta.get("tools_used"):
                st.caption(f"🔧 Tools usadas: {', '.join(meta['tools_used'])}")

if prompt := st.chat_input("Escribe tu pregunta..."):
    with st.chat_message("human"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "human", "content": prompt})

    chat_history = [
        HumanMessage(content=m["content"]) if m["role"] == "human" else AIMessage(content=m["content"])
        for m in st.session_state.messages[:-1]
    ]

    engine_mode = MODE_MAP[agent_mode]

    result = invoke_graph(
        question=prompt,
        messages=chat_history,
        engine_mode=engine_mode,
    )

    tools_used = result.get("tools_used", [])

    with st.chat_message("assistant"):
        st.markdown(result["answer"])
        st.badge(f"Intención: {result.get('intent', 'unknown')}", icon="🎯")
        st.caption(f"🧠 Motor usado: {engine_mode}")

        if tools_used:
            st.caption(f"🔧 Tools usadas: {', '.join(tools_used)}")

    st.session_state.messages.append({"role": "assistant", "content": result["answer"]})

    st.session_state.metadata.append(
        {
            "intent": result.get("intent", "unknown"),
            "engine_mode": engine_mode,
            "tools_used": tools_used,
        }
    )
