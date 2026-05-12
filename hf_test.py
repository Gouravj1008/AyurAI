from huggingface_hub import InferenceClient
import os

client = InferenceClient(
    model="google/flan-t5-large",
    token=os.getenv("HF_API_KEY")
)

print(client.text_generation("Explain Python in one line", max_new_tokens=50))
