# HuggingFace Dataset

1. Finding Datasets: You discovered that Hugging Face Hub hosts a wide range of community-curated datasets across various tasks and domains. You can use filters to search for datasets by task, language, size, or license.
2. Inspecting Datasets: You learned how to use the `load_dataset_builder` function to **inspect datasets before downloading them**. This function allows you to view dataset **metadata, such as descriptions and features**, without loading the entire dataset into your environment. For example:
```
from datasets import load_dataset_builder
reviews_builder = load_dataset_builder("derenrich/wikidata-en-descriptions-small")
print(reviews_builder.info.features)
```
3. Loading Datasets: You found out how to load datasets using the load_dataset function, specifying **parameters like split** to download only parts of the dataset you need. This is useful for managing resources when working with large datasets.
4. Preprocessing Datasets: Finally, you explored how to filter and select data from datasets. Since Hugging Face datasets use Apache Arrow for efficient data storage and querying, you learned to use methods like **.filter() and .select() for dataset preprocessing.**




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






# Text Classification Scenario 1 - Grammatical Correctness
* Text classification is the process of labeling an input text into a pre-defined category. This can take the form of sentiment - positive or negative; spam detection - spam or not spam; and even grammatical errors.
* Explore the use of a `text-classification` pipeline for checking an input sentence for grammatical errors.
* `pipeline` from the `transformers` library is already loaded for you.
* Create a pipeline for the task text-classification and use the model "abdulmatinomotoso/English_Grammar_Checker", saving the pipeline as grammar_checker.
* Use the grammar_checker to predict the grammatical correctness of the input sentence provided and save as output.

```
# Create a pipeline for grammar checking
grammar_checker = pipeline(
  task="text-classification", 
  model="abdulmatinomotoso/English_Grammar_Checker"
)

# Check grammar of the input text
output = grammar_checker("I will walk dog")
print(output)
```
    [{'label': 'LABEL_0', 'score': 0.9956323504447937}]
The grammar_checker pipeline classified the input text as "LABEL_0", or unacceptable grammar.




# Text Classification Scenario 2 - Question Natural Language Inference QNLI (Enuf info in the context to ans qn?)
* Another task under the text classification umbrella is Question Natural Language Inference, or QNLI.
* This checks if a premise contains **enough information to answer a posed question, determining whether the answer can be found in the given text.**
* Performing different tasks with the text-classification pipeline can be done by choosing different models.
* Each model is trained to predict specific labels and optimized for learning different context within a text.
* `pipeline` from the transformers library is already loaded for you.
* Create a text classification QNLI pipeline using the model "cross-encoder/qnli-electra-base" and save as classifier.
* Use this classifier to determine if the text provides enough information to answer the question.

```
# Create the pipeline
classifier = pipeline(task="text-classification", 
                model="cross-encoder/qnli-electra-base")

# Predict the output
output = classifier("Where is the capital of France?, Brittany is known for its stunning coastline.")

print(output)
```
    [{'label': 'LABEL_0', 'score': 0.016211988404393196}]
The QNLI pipeline showed that the **text could not answer the question**, with a **low score**. 



# Text Classification Scenario 3 - Dynamic category assignment
* Dynamic category assignment enables a model to classify text into **predefined categories, even without prior training for those categories.**
* Using Hugging Face’s pipeline() for the **zero-shot-classification task**, provide the text and predefined categories to identify the best match.
* Build a classifier to predict the label for the input text, which is a news headline already loaded for you.
* The pipelines from the transformers library is preloaded for your convenience.
* Note: We are using a customized version of the pipeline to help you learn how to use these functions without needing to download the model.
* Build the pipeline and save as classifier.
* Create a list of the labels - "politics", "science", "sports" - and save as categories.
* Predict the label of text using the classifier and predefined categories.

```
text = "AI-powered robots assist in complex brain surgeries with precision."

# Create the pipeline
classifier = pipeline(task="zero-shot-classification", 
                      model="facebook/bart-large-mnli")

# Create the categories list
categories = ["politics", "science", "sports"]

# Predict the output
output = classifier(text, categories)

# Print the top label and its score
print(f"Top Label: {output['labels'][0]} with score: {output['scores'][0]}")
```
    Top Label: science with score: 0.9510332942008972














