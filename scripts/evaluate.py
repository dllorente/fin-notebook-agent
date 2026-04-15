import csv
import json
import time
from datetime import datetime
from pathlib import Path

from app.engine.runner import run_engine

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
json_path = f"output/eval_results_sprint12_{timestamp}.json"
csv_path = f"output/eval_results_sprint12_{timestamp}.csv"

def score_response(expected: str, actual: str) -> float:
    expected_words = set[str](expected.lower().split())
    actual_words = set[str](actual.lower().split())
    matches = expected_words.intersection(actual_words)
    return round(len(matches) / len(expected_words), 2)


def evaluate():
    with open("tests/eval_dataset_grounded.json") as f:
        dataset = json.load(f)

    results = evaluate_modes(dataset, n_questions=4)

    Path("output").mkdir(exist_ok=True)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "question",
                "expected",
                "mode",
                "answer",
                "intent",
                "tools_used",
                "score",
                "latency",
            ],
        )
        writer.writeheader()

        for row in results:
            writer.writerow(
                {
                    **row,
                    "tools_used": ", ".join(row["tools_used"]),
                }
            )

    print(f"\n💾 Resultados guardados en {json_path}")
    print(f"💾 Resultados guardados en {csv_path}")
    return results

def evaluate_modes(dataset, n_questions=4):  # limitamos a 5 para ir rápido
    print("\n🔄 Comparativa RAG vs ReAct vs Dynamic")
    print("=" * 70)
    
    results = []
    total_scores = {"rag": 0, "react": 0, "dynamic": 0}
    
    for i, item in enumerate(dataset[:n_questions]):
        print(f"\n📝 Pregunta {i+1}: {item['question'][:60]}...")
        
        for mode in ["rag", "react", "dynamic"]:
            start_time = time.time()
            result = run_engine(item["question"], mode=mode)
            latency = round(time.time() - start_time, 2)
            
            score = score_response(item["expected"], result["answer"])
            total_scores[mode] += score
            
            print(f"  {mode.upper():8} | intent: {result.get('intent', 'N/A'):10} | "
                  f"tools: {len(result.get('tools_used', [])):2} | "
                  f"score: {score:4.2f}s | lat: {latency:4.2f}s")
            
            results.append({
                "question": item["question"],
                "expected": item["expected"],
                "mode": mode,
                "answer": result["answer"][:100],
                "intent": result.get("intent", "unknown"),
                "tools_used": result.get("tools_used", []),
                "score": score,
                "latency": latency,
            })
    
    # Resumen por modo
    print("\n📊 RESUMEN POR MODO")
    print("-" * 50)

    for mode in ["rag", "react", "dynamic"]:
        mode_results = [r for r in results if r["mode"] == mode]

        avg_score = round(
            sum(r["score"] for r in mode_results) / len(mode_results), 2
        )
        avg_latency = round(
            sum(r["latency"] for r in mode_results) / len(mode_results), 2
        )
        avg_tools = round(
            sum(len(r["tools_used"]) for r in mode_results) / len(mode_results), 2
        )

        print(
            f"{mode.upper()}: score medio {avg_score} | "
            f"tools promedio {avg_tools} | "
            f"latencia media {avg_latency}s"
        )
    
    return results

if __name__ == "__main__":
    evaluate()
