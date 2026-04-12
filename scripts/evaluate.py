import json

from app.engine.graph.graph import build_graph


def score_response(expected: str, actual: str) -> float:
    expected_words = set[str](expected.lower().split())
    actual_words = set[str](actual.lower().split())
    matches = expected_words.intersection(actual_words)
    return round(len(matches) / len(expected_words), 2)


def evaluate():
    # 1. Carga el dataset
    with open("tests/eval_dataset.json") as f:
        dataset = json.load(f)
    # 2. Construye el grafo
    graph = build_graph()
    results = []
    total_score = 0
    for item in dataset:
        result = graph.invoke(
            {
                "question": item["question"],
                "session_id": "eval",
                "intent": "",
                "context": "",
                "answer": "",
                "messages": [],
            }
        )
        score = score_response(item["question"], result["answer"])
        total_score += score
        results.append(
            {
                "question": item["question"],
                "expected": item["expected"],
                "actual": result["answer"][:100],
                "intent": result["intent"],
                "score": score,
            }
        )
        print(f"Q: {item['question']}")
        print(f"Intent: {result['intent']}")
        print(f"Score: {score}")
        print(f"Actual: {result['answer'][:100]}...")
        print("---")
    avg_score = round(total_score / len(dataset), 2)
    print(f"✅ Score medio: {avg_score}")
    return results


if __name__ == "__main__":
    evaluate()
