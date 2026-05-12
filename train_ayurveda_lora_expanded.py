"""
Expanded Ayurveda LoRA training entrypoint.

Loads every data/ayurveda*.jsonl file, deduplicates examples, and trains using
the existing train_ayurveda_lora pipeline.
"""

import argparse
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def load_all_ayurveda_data(data_dir="data"):
    data = []
    seen = set()
    files = sorted(Path(data_dir).glob("ayurveda*.jsonl"))
    for file_path in files:
        file_count = 0
        with file_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                example = json.loads(line)
                question = example.get("question", "").strip()
                answer = example.get("answer", "").strip()
                key = (question.lower(), answer.lower())
                if not question or not answer or key in seen:
                    continue
                seen.add(key)
                data.append({"question": question, "answer": answer})
                file_count += 1
        logger.info("Loaded %s examples from %s", file_count, file_path)
    logger.info("Loaded %s total expanded Ayurveda examples", len(data))
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Jarvis on expanded Ayurveda data.")
    parser.add_argument("--prepare-only", action="store_true", help="Load and count data without starting model training.")
    args = parser.parse_args()

    train_data = load_all_ayurveda_data()
    if not train_data:
        raise SystemExit("No Ayurveda training examples found.")
    if args.prepare_only:
        print(f"Prepared {len(train_data)} expanded Ayurveda examples.")
        raise SystemExit(0)

    original_read_text = Path.read_text

    def read_text_utf8(self, encoding=None, errors=None):
        return original_read_text(self, encoding=encoding or "utf-8", errors=errors)

    Path.read_text = read_text_utf8

    from train_ayurveda_lora import train_ayurveda_model

    train_ayurveda_model(train_data, output_dir="models/medical-lora")
