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






# Summarizing long text
Summarization reduces large text into manageable content, helping readers quickly grasp key points from lengthy articles or documents.

There are 2 main types:
* extractive, which selects key sentences from the original text, and
* abstractive, which generates new sentences summarizing main ideas.

In this exercise, you’ll create an **abstractive summarization pipeline** using Hugging Face's pipeline() function and the cnicu/t5-small-booksum model. 
You’ll summarize text from a Wikipedia page on Greece, comparing the abstractive model's rephrased output to the original.

The pipeline function from the transformers library and the original_text have already been loaded for you.
* Create the summarization pipeline using the task "summarization" and save as summarizer.
* Use the new pipeline to create a summary of the text and save as summary_text.
* Compare the length of the original and summary text.


```
# Create the summarization pipeline
summarizer = pipeline(task="summarization", 
                      model="cnicu/t5-small-booksum")

# Summarize the text
summary_text = summarizer(original_text)

# Compare the length
print(f"Original text length: {len(original_tex
t)}")
print(f"Original text: {original_text}")
print(f"Summary length: {len(summary_text[0]['summary_text'])}")
print(f"Summary text: {summary_text[0]['summary_text']}")
```
Original text length: 829
Original text: 
Greece has many islands, with estimates ranging from somewhere around 1,200 to 6,000, depending on the minimum size to take into account. The number of inhabited islands is variously cited as between 166 and 227.
The Greek islands are traditionally grouped into the following clusters: the Argo-Saronic Islands in the Saronic Gulf near Athens; the Cyclades, a large but dense collection occupying the central part of the Aegean Sea; the North Aegean islands, a loose grouping off the west coast of Turkey; the Dodecanese, another loose collection in the southeast between Crete and Turkey; the Sporades, a small tight group off the coast of Euboea; and the Ionian Islands, chiefly located to the west of the mainland in the Ionian Sea. Crete with its surrounding islets and Euboea are traditionally excluded from this grouping.

Summary length: 473
Summary text: Greece has many islands, with estimates ranging from somewhere around 1,200 to 6,000 depending on the minimum size to take into account. The number of inhabited islands is variously cited as between 166 and 227. The Greek islands are traditionally grouped into the following clusters: the Argo-Saronic Islands in the Saronic Gulf near Athens; the Cyclades, a large but dense collection occupying the central part of the Aegean Sea; the North Aegesan islands, an loose group










# Adjusting the summary length
* The pipeline() function, has two important parameters: min_new_tokens and max_new_tokens.
* These are useful for adjusting the length of the resulting summary text to be short, longer, or within a certain number of words.
* You might want to do this if there are space constraints (i.e., small storage), to enhance readability, or improve the quality of the summary.
* You'll experiment with a short and long summarizer by setting these two parameters to a small range, then a wider range.
* pipeline from the transformers library and the original_text have already been loaded for you.

Part 1
* Create a summarization pipeline to summarize original_text to between 1 and 10 tokens.
```
# Generate a summary of original_text between 1 and 10 tokens
short_summarizer = pipeline(task="summarization", 
                            model="cnicu/t5-small-booksum", 
                            min_new_tokens=1, 
                            max_new_tokens=10)

short_summary_text = short_summarizer(original_text)

print(short_summary_text[0]["summary_text"])
```
    Greece has many islands, with estimates ranging from

    
Part 2
* Repeat these steps for a summarization pipeline that has a minimum length of 50 and maximum of 150.
```
long_summarizer = pipeline(task="summarization", 
                            model="cnicu/t5-small-booksum", 
                            min_new_tokens=50, 
                            max_new_tokens=150)

long_summary_text = long_summarizer(original_text)

print(long_summary_text[0]["summary_text"])
```
    Greece has many islands, with estimates ranging from somewhere around 1,200 to 6,000 depending on the minimum size to take into account. The number of inhabited islands is variously cited as between 166 and 227. The Greek islands are traditionally grouped into the following clusters: the Argo-Saronic Islands in the Saronic Gulf near Athens; the Cyclades, a large but dense collection occupying the central part of the Aegean Sea; the North Aegesan islands, an loose group








# When to use AutoModels and AutoTokenizers?
* Pipelines and AutoModels with AutoTokenizers are two approaches to working with Hugging Face models, each suited for different use cases.
* Pipelines offer simplicity, while AutoModels and AutoTokenizers provide more control and customization.

Pipelines
* **Quick** way to classify customer reviews as POS/NEG - **sentiment analysis**
* **Simple text summarisation** for news articles
* quickly **compare multiple text generation models**

Auto Classes
* customer support model tt **prioritises** 'Urgent' category more often
* **tokenise** Fin Rpts, **add custom tokens** for terms eg EBITDA, ROI




# Tokenizing text with AutoTokenizer
* AutoTokenizers simplify text preparation by automatically handling cleaning, normalization, and tokenization.
* They ensure the text is processed just as the model expects.
* In this exercise, explore how AutoTokenizer transforms text into tokens ready for machine learning tasks.
* Import the required class from transformers, load the tokenizer using the correct method, and split input text into tokens.

```
# Import necessary library for tokenization
from transformers import AutoTokenizer

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

# Split input text into tokens
tokens = tokenizer.tokenize("AI: Making robots smarter and humans lazier!")

# Display the tokenized output
print(f"Tokenized output: {tokens}")
```
    Tokenized output: ['ai', ':', 'making', 'robots', 'smarter', 'and', 'humans', 'la', '##zier', '!']
    



# Using AutoClasses
* You’ve seen how tokenizers work and explored their role in preparing text for models.
* Now, let’s take it a step further by combining AutoModels and AutoTokenizers with the pipeline() function.
* It's a nice balance of control and convenience.
* Continue with the sentiment analysis task and combine AutoClasses with the pipeline module.
* `AutoModelForSequenceClassification, AutoTokenizer and pipeline` from the transformers library have already been imported for you.
* Download the model and tokenizer and save as my_model and my_tokenizer, respectively.
* Create the pipeline and save as my_pipeline.
* Predict the output using my_pipeline and save as output.

```
# Download the model and tokenizer
my_model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
my_tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

# Create the pipeline
my_pipeline = pipeline(task="sentiment-analysis", 
                        model=my_model, 
                        tokenizer=my_tokenizer)

# Predict the sentiment
output = my_pipeline("This course is pretty good, I guess.")
print(f"Sentiment using AutoClasses: {output[0]['label']}")
```
Sentiment using AutoClasses: POSITIVE








# Text classification vs summarisation vs QnA
Text classification
* label news articles - sports, tech, public policy
* social media posts - POS/NEG

summarisation
* from contract, get list of key clauses
* from 10-page financial report, get brief overview

QnA
* From co doc, find maternity leave policy details
* From annual report, find Q3 REV





# Extracting text with PyPDF
PyPDF lets us extract text from PDFs, making it easy to work with multi-page documents like policy files.
In this exercise, you’ll load the US_Employee_Policy.pdf, extract its content page by page, and combine it into a single string, preparing the text for a question-answering pipeline.
* Import the required class from pypdf and use it to load the PDF file.
* Access each page and extract its content using the correct method.

```
from pypdf import PdfReader

# Extract text from the PDF
reader = PdfReader("US_Employee_Policy.pdf")

# Extract text from all pages
document_text = ""
for page in reader.pages: 
    document_text += page.extract_text()

print(document_text)
```
    US Employee Policy Document
    Welcome to the US Employee Policy document. This document outlines the policies and benefits
    available to all employees. Please read carefully to understand your entitlements and
    responsibilities.
    1. Vacation Policy:
    Employees are entitled to 25 vacation days annually.
    2. Sick Leave:
    Employees may take up to 10 sick days per year.
    3. Notice Period:
    Employees are required to give a 2-week notice before resignation.Work and Leave Policies
    4. Public Holidays:
    The company observes 12 public holidays annually.
    5. Maternity Leave:
    Employees are entitled to up to 16 weeks of maternity leave.
    6. Paternity Leave:
    Employees are entitled to up to 10 days of paternity leave.
    7. Volunteer Days:
    Each employee is allowed 1 volunteer day annually to contribute to social causes.Additional Information
    8. Probation Period:
    New employees undergo a 3-month probation period.
    9. Remote Work:
    Employees may work remotely up to 2 days per week.
    10. Retirement Age:
    The standard retirement age is 65 years.
    For further questions, please contact the HR department.






    



# Building a Q&A pipeline
In the previous exercise, we extracted text from a multi-page document using PyPDF and prepared it as a single string.
Now, you’ll build a question-answering pipeline using Hugging Face to retrieve specific answers from the document.
Both the pipeline module and document_text have been preloaded for you.
* Initialize a question-answering pipeline with the correct task and model.
* Pass the question and document_text to the pipeline.
* Print the result to view the answer.

```
# Load the question-answering pipeline
qa_pipeline = pipeline(task="question-answering", 
                       model="distilbert-base-cased-distilled-squad")

question = "What is the notice period for resignation?"

# Get the answer from the QA pipeline
result = qa_pipeline(question=question, 
                     context=document_text)

# Print the answer
print(f"Document text: {document_text}")
print(f"Result: {result}")
print(f"Answer: {result['answer']}")
```
    Document text: US Employee Policy Document
    Welcome to the US Employee Policy document. This document outlines the policies and benefits
    available to all employees. Please read carefully to understand your entitlements and
    responsibilities.
    1. Vacation Policy:
    Employees are entitled to 25 vacation days annually.
    2. Sick Leave:
    Employees may take up to 10 sick days per year.
    3. Notice Period:
    Employees are required to give a 2-week notice before resignation.Work and Leave Policies
    4. Public Holidays:
    The company observes 12 public holidays annually.
    5. Maternity Leave:
    Employees are entitled to up to 16 weeks of maternity leave.
    6. Paternity Leave:
    Employees are entitled to up to 10 days of paternity leave.
    7. Volunteer Days:
    Each employee is allowed 1 volunteer day annually to contribute to social causes.Additional Information
    8. Probation Period:
    New employees undergo a 3-month probation period.
    9. Remote Work:
    Employees may work remotely up to 2 days per week.
    10. Retirement Age:
    The standard retirement age is 65 years.
    For further questions, please contact the HR department.

    
    Result: {'score': 0.8854646682739258, 'start': 412, 'end': 418, 'answer': '2-week'}

    
    Answer: 2-week



