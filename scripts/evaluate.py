import csv
import json
import time
from datetime import datetime
from pathlib import Path

from app.engine.runner import run_engine


def score_response(expected: str, actual: str) -> float:
    expected_words = set(expected.lower().split())
    actual_words = set(actual.lower().split())

    if not expected_words:
        return 0.0

    matches = expected_words.intersection(actual_words)
    return round(len(matches) / len(expected_words), 2)


def evaluate_modes(dataset, n_questions=4):
    print("\n🔄 Comparativa RAG vs ReAct vs Dynamic")
    print("=" * 70)

    results = []

    for i, item in enumerate(dataset[:n_questions]):
        print(f"\n📝 Pregunta {i+1}: {item['question'][:60]}...")

        for mode in ["rag", "react", "dynamic"]:
            start_time = time.perf_counter()
            result = run_engine(item["question"], mode=mode)
            latency = round(time.perf_counter() - start_time, 2)

            score = score_response(item["expected"], result["answer"])
            predicted_intent = result.get("intent", "unknown")
            expected_intent = item.get("expected_intent", "unknown")
            intent_match = predicted_intent == expected_intent

            print(
                f"  {mode.upper():8} | expected: {expected_intent:10} | "
                f"predicted: {predicted_intent:10} | "
                f"match: {str(intent_match):5} | "
                f"tools: {len(result.get('tools_used', [])):2} | "
                f"score: {score:4.2f} | lat: {latency:4.2f}s"
            )

            row = {
                "question": item["question"],
                "expected": item.get("expected"),
                "expected_intent": expected_intent,
                "mode": mode,
                "predicted_answer": result["answer"][:300],
                "predicted_intent": predicted_intent,
                "intent_match": intent_match,
                "tools_used": result.get("tools_used", []),
                "score": score,
                "latency": latency,
            }

            results.append(row)

    print("\n📊 RESUMEN POR MODO")
    print("-" * 50)

    for mode in ["rag", "react", "dynamic"]:
        mode_results = [r for r in results if r["mode"] == mode]

        if not mode_results:
            continue

        avg_score = round(sum(r["score"] for r in mode_results) / len(mode_results), 2)
        avg_latency = round(sum(r["latency"] for r in mode_results) / len(mode_results), 2)
        avg_tools = round(sum(len(r["tools_used"]) for r in mode_results) / len(mode_results), 2)
        intent_accuracy = round(
            sum(1 for r in mode_results if r["intent_match"]) / len(mode_results), 2
        )

        print(
            f"{mode.upper()}: score medio {avg_score} | "
            f"accuracy intent {intent_accuracy} | "
            f"tools promedio {avg_tools} | "
            f"latencia media {avg_latency}s"
        )

    return results


def evaluate():
    Path("output").mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = f"output/eval_results_sprint12_{timestamp}.json"
    csv_path = f"output/eval_results_sprint12_{timestamp}.csv"

    with open("tests/eval_dataset_grounded.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)

    results = evaluate_modes(dataset, n_questions=4)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "question",
                "expected",
                "expected_intent",
                "mode",
                "predicted_answer",
                "predicted_intent",
                "intent_match",
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


if __name__ == "__main__":
    evaluate()