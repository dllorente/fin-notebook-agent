import os

os.environ["LANGCHAIN_TRACING_V2"] = "false"

from app.engine.runner import run_engine

print("🏦 Pregunta bancaria...")
result = run_engine("¿Qué es API Governance en BBVA?")
print(f"✅ React bancario: {result}")
