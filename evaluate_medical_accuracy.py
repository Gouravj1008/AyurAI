import argparse
import json
import os
import re

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def exact_match(pred: str, target: str) -> float:
    return 1.0 if normalize(pred) == normalize(target) else 0.0


def token_f1(pred: str, target: str) -> float:
    p_tokens = normalize(pred).split()
    t_tokens = normalize(target).split()
    if not p_tokens or not t_tokens:
        return 0.0

    p_set = {}
    for t in p_tokens:
        p_set[t] = p_set.get(t, 0) + 1

    t_set = {}
    for t in t_tokens:
        t_set[t] = t_set.get(t, 0) + 1

    common = 0
    for tok, c in p_set.items():
        if tok in t_set:
            common += min(c, t_set[tok])

    if common == 0:
        return 0.0

    precision = common / len(p_tokens)
    recall = common / len(t_tokens)
    return 2 * precision * recall / (precision + recall)


def load_records(path: str):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            q = str(obj.get("question", "")).strip()
            a = str(obj.get("answer", "")).strip()
            if q and a:
                rows.append((q, a))
    if not rows:
        raise ValueError(f"No valid records found in {path}")
    return rows


def build_prompt(question: str) -> str:
    return (
        "<|system|>You are Jarvis, a medical Q&A assistant. Give concise and safe answers.\n"
        f"<|user|>{question}\n<|assistant|>"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate medical QA performance")
    parser.add_argument("--data", default="data/medical_qa_eval.jsonl")
    parser.add_argument("--base-model", default="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    parser.add_argument("--adapter", default="models/medical-lora")
    parser.add_argument("--max-new-tokens", type=int, default=120)
    args = parser.parse_args()

    print("Loading model for evaluation...")
    tokenizer = AutoTokenizer.from_pretrained(args.base_model)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(args.base_model)

    if os.path.isdir(args.adapter):
        from peft import PeftModel

        model = PeftModel.from_pretrained(model, args.adapter)
        print(f"Loaded adapter: {args.adapter}")
    else:
        print("Adapter not found. Evaluating base model.")

    generator = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device=-1,
    )

    rows = load_records(args.data)

    em_scores = []
    f1_scores = []

    for question, target in rows:
        out = generator(
            build_prompt(question),
            max_new_tokens=args.max_new_tokens,
            temperature=0.1,
            do_sample=False,
            return_full_text=False,
            pad_token_id=tokenizer.pad_token_id,
        )[0]["generated_text"].strip()

        em_scores.append(exact_match(out, target))
        f1_scores.append(token_f1(out, target))

    em = sum(em_scores) / len(em_scores)
    f1 = sum(f1_scores) / len(f1_scores)

    print("\nEvaluation results")
    print(f"Samples: {len(rows)}")
    print(f"Exact Match: {em:.3f}")
    print(f"Token F1:    {f1:.3f}")


if __name__ == "__main__":
    main()
