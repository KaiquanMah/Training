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








# Exploring datasets on the Hub!
The Hugging Face hub is home to 100,000's of datasets, across domains, languages, sizes, and modalities.
You've been provided with a dataset from the Hub designed to help LLMs reason about math problems.
https://assets.datacamp.com/production/repositories/6536/datasets/cf0dd3d85082816f10216621777f5de6a5226168/hub_dataset.png

Considering the dataset card, which of the following statements are true?
YES    There are > 4 million rows
YES    It is available under the MIT license
NO    The dataset contain images
YES    The dataset is called MathX-5M







# Loading datasets
After you've chosen your dataset, it's time to load it with the datasets library!
In this case, you'll load the "validation" split of the "TIGER-Lab/MMLU-Pro" dataset, which is a benchmark evaluation dataset.
The load_dataset module from the datasets package is already loaded for you.
Use the correct function to load the "TIGER-Lab/MMLU-Pro" dataset and specify the "validation" split.
```
# Load the "validation" split of the TIGER-Lab/MMLU-Pro dataset
my_dataset = load_dataset("TIGER-Lab/MMLU-Pro", split="validation")

# Display dataset details
print(my_dataset)
```
<script.py> output:
    Dataset({
        features: ['question_id', 'question', 'options', 'answer', 'answer_index', 'cot_content', 'category', 'src'],
        num_rows: 70
    })





# Working with huggingface datasets
There will likely be many occasions when you will need to preprocess/work with a dataset before using it within a ML task.
2 common preprocessing tasks are filtering and selecting (or slicing).
Given the size of these datasets, Hugging Face leverages arrow file types.

This means performing preprocessing is slightly different than what you might be used to.
Fortunately, there's already methods to help with this!

The dataset is already loaded for you under wikipedia.

Part 1
- Filter the dataset for rows with the term "football" in the text column and save as filtered.
- Select a single example from the filtered dataset and save as example.
```
# Filter the documents
filtered = wikipedia.filter(lambda row: "football" in row["text"])

# Create a sample dataset
example = filtered.select(range(1))

print(example[0]["text"])
```
    Luis Miguel Aparecido Alves (born May 25, 1985), known as Gugu, is a Brazilian football player currently playing for Iraklis Psachna F.C.
    
    External links
    
    1985 births
    Living people
    Brazilian men's footballers
    Thrasyvoulos F.C. players
    Ionikos F.C. players
    Super League Greece players
    Expatriate men's footballers in Greece
    Brazilian expatriate men's footballers
    Men's association football midfielders



    
Part 2
- Which soccer player, born May 25, was the single example returned from the filtered list?
YES    Luis Miguel Aparecido Alves
Lionel Messi
Diego Maradona




