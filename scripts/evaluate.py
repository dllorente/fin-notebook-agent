import json
from app.engine.graph.graph import build_graph

def evaluate():
    # 1. Carga el dataset
    with open("tests/eval_dataset.json") as f:
        dataset = json.load(f)
    # 2. Construye el grafo
    graph = build_graph()
    results = []
    for item in dataset:
        result = graph.invoke({
            "question": item["question"],      
            "session_id": "eval",
            "intent": "",
            "context": "",
            "answer": "",
            "messages": []
        })
        results.append({
            "question": item["question"],
            "expected": item["expected"],
            "actual": result['answer'][:100],
            "intent": result['intent']   
        })
        print(f"Q: {item['question']}")
        print(f"Intent: {result['intent']}")
        print(f"Actual: {result['answer'][:100]}...")
        print("---")
    
    return results

if __name__ == "__main__":
    evaluate()