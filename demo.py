from huggingface_hub import login
from transformers import pipeline
login('Enter your hugging face login key here')
generator = pipeline('text-generation',model='gpt2',do_sample=True)
res = generator('python interview questions',max_length=100,num_return_sequences=1,truncation=True)
print(res)
