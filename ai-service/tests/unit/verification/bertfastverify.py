from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(
    r"C:\Hackathons\ARC\models\bge-base-en-v1.5",
    use_fast=True,
)

print("Type                :", type(tokenizer))
print("is_fast             :", tokenizer.is_fast)
print("Backend tokenizer   :", getattr(tokenizer, "backend_tokenizer", None))
print("Tokenizer file      :", tokenizer.init_kwargs)