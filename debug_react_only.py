from app.engine.runner import run_engine

question = "¿Qué experiencia tienes con LangChain y LangGraph, y en qué se diferencian ambos frameworks?"
print("🔍 React solo...")

try:
    result = run_engine(question, mode="react")
    print("✅ React completó:")
    print(f"  Intent: {result.get('intent')}")
    print(f"  Tools: {result.get('tools_used', [])}")
    print(f"  Answer preview: {result['answer'][:100]}")
except Exception as e:
    print(f"❌ React error: {type(e).__name__}: {str(e)[:150]}")
