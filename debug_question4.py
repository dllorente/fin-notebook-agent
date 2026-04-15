import time
from app.engine.runner import run_engine

question = "¿Qué experiencia tienes con LangChain y LangGraph, y en qué se diferencian ambos frameworks?"
print("🧪 Test pregunta 4...")

for mode in ["rag", "react", "dynamic"]:
    print(f"\n{mode.upper()}:")
    start = time.time()
    try:
        result = run_engine(question, mode=mode)
        latency = round(time.time() - start, 2)
        print(f"  ✅ OK | intent: {result.get('intent')} | tools: {len(result.get('tools_used', []))} | lat: {latency}s")
    except Exception as e:
        print(f"  ❌ ERROR: {str(e)[:100]}")
