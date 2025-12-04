# Building a text generation pipeline
Hugging Face pipelines make it simple to use machine learning models for a variety of tasks. 
In this exercise, you'll **build a text generation pipeline using the gpt2 model and customize the output by adjusting its parameters**.
Feel free to **experiment with different prompts** in the pipeline, such as "What if …?", "How to …?", or any other creative idea you'd like to explore.

- Complete the missing code to build a text generation pipeline using the "gpt2" model.
- Provide a custom sentence of your choice as the **input prompt**; keep it **short to prevent timeouts**.
- Configure the pipeline to **generate up to 10 tokens and produce 2 outputs**.


```
from transformers import pipeline 

gpt2_pipeline = pipeline(task="text-generation", model="openai-community/gpt2")

# Generate three text outputs with a maximum length of 10 tokens
# results = gpt2_pipeline("What if AI", max_new_tokens=10, num_return_sequences=2)
results = gpt2_pipeline("AI Governance in SG", max_new_tokens=10, num_return_sequences=2)

for result in results:
    print(result['generated_text'])
```

AI Governance in SG&A 1.0 (Masters in Govern
AI Governance in SGD-II: An Analysis of the Evidence from


```
results = gpt2_pipeline("AI Governance in Singapore", max_new_tokens=10, num_return_sequences=2)
```
AI Governance in Singapore, which was run by the National Trust for the
AI Governance in Singapore

The following is an edited extract from a










# Inference providers
In some cases, you may lack the hardware to run Hugging Face models locally. 
Large-parameter LLMs, and image and video generation models in particular often require Graphics Processing Units (GPUs) to parallelize the computations. 
Hugging Face providers inference providers to outsource this hardware to third-party partners.

Drag the code snippets into the correct order to send a prompt to the DeepSeek-V3 model hosted on Together.ai.
```
from huggingface_hub import InferenceClient


client = InferenceClient(provider="together",
                         api_key=os.environ["HF_TOKEN"],
                        )


completion = client.chat.completions.create(model="deepseek-ai/DeepSeek-V3",
                                            messages=[
                                                      {"role": "user",
                                                       "content": "What is the capital of Belgium?"
                                                      }
                                                     ],
                                            )


print(completion.choices[0].message)
```
The capital of Belgium is Brussels. It serves as the administrative center of the European Union and is known for landmarks like the Grand Place, Atomium, and Manneken Pis.




