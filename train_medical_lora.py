import argparse
import json
import os
from dataclasses import dataclass

from datasets import Dataset
from peft import LoraConfig, TaskType, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)


SYSTEM_PROMPT = (
    "You are Jarvis, a medical Q&A assistant. Provide concise, safe, and evidence-aligned "
    "answers. If information is insufficient, ask follow-up questions."
)


@dataclass
class Record:
    question: str
    answer: str


def load_jsonl_records(path: str) -> list[Record]:
    records: list[Record] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            question = str(obj.get("question", "")).strip()
            answer = str(obj.get("answer", "")).strip()
            if question and answer:
                records.append(Record(question=question, answer=answer))
    if not records:
        raise ValueError(f"No valid question/answer rows found in {path}")
    return records


def build_text(record: Record) -> str:
    return (
        f"<|system|>{SYSTEM_PROMPT}\n"
        f"<|user|>{record.question}\n"
        f"<|assistant|>{record.answer}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune TinyLlama with LoRA for medical Q&A")
    parser.add_argument("--data", default="data/medical_qa.jsonl", help="Path to JSONL with question/answer fields")
    parser.add_argument("--base-model", default="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    parser.add_argument("--output", default="models/medical-lora", help="Output path for LoRA adapter")
    parser.add_argument("--epochs", type=float, default=2.0)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--grad-accum", type=int, default=8)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--max-length", type=int, default=512)
    parser.add_argument("--max-steps", type=int, default=-1, help="Set >0 for a short training run")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    print("Loading tokenizer and base model...")
    tokenizer = AutoTokenizer.from_pretrained(args.base_model)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(args.base_model)

    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    print(f"Loading dataset: {args.data}")
    records = load_jsonl_records(args.data)
    texts = [build_text(r) for r in records]
    dataset = Dataset.from_dict({"text": texts})

    def tokenize_batch(batch):
        tokenized = tokenizer(
            batch["text"],
            truncation=True,
            padding="max_length",
            max_length=args.max_length,
        )
        tokenized["labels"] = tokenized["input_ids"].copy()
        return tokenized

    tokenized_dataset = dataset.map(tokenize_batch, batched=True, remove_columns=["text"])

    training_args = TrainingArguments(
        output_dir="outputs/medical-lora-checkpoints",
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        max_steps=args.max_steps,
        learning_rate=args.lr,
        logging_steps=10,
        save_strategy="epoch",
        report_to="none",
        fp16=False,
        bf16=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
    )

    trainer.train()

    print(f"Saving LoRA adapter to: {args.output}")
    model.save_pretrained(args.output)
    tokenizer.save_pretrained(args.output)
    print("Training complete.")


if __name__ == "__main__":
    main()
