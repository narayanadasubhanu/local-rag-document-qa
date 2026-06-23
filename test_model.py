from llama_cpp import Llama

print("Starting model load...")

llm = Llama(
    model_path="models/qwen2.5-3b-instruct-q4_k_m.gguf",
    verbose=True
)

print("Model loaded successfully!")