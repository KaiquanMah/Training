# AIAP Assessment 20 - Kaiquan Mah

This repository contains the end-to-end data preprocessing and machine learning pipeline for AIAP Assessment 20.

We will cover a few topics:
1. [Folder structure](#1-folder-structure)
2. [Flow of the pipeline](#2-flow-of-the-pipeline)
3. [Explanation of fields selected for classification](#3-explanation-of-fields-selected-for-classification)
4. [Explanation of models selected](#4-explanation-of-models-selected)
5. [Explanation of hyperparameters tuned](#5-explanation-of-hyperparameters-tuned)
6. [Explanation of metrics used](#6-explanation-of-metrics-used)
7. [Explanation of results from our best, tuned models](#7-explanation-of-results-from-our-best-tuned-models)
8. [Some closing remarks on customer characteristics](#8-some-closing-remarks-on-customer-characteristics)
9. [Screenshots of successful pipeline run and folder structure](#9-screenshots-of-successful-pipeline-run-and-folder-structure)


# 1. Folder structure
The folder structure of the repository is as follows:
```
|--.github
|--data
    |--.gitignore
|--src
    |--__init__.py
    |--config.py
    |--datapreprocessor.py
    |--model_training.py
|--results
    |--training_results_<yyyyMMdd_hhmmss>.txt
    |--*.png
|--README.md
|--eda.ipynb
|--requirements.txt
|--run.sh
```

Here are reasons for the folder structure:
* .github: GitHub Actions to run pipeline in GitHub and verify run is successful
* data: Folder containing .db data file, downloaded from the URL only during the pipeline run
  * `.gitignore`: Tells Git not to commit all files in the data folder from our local machine to GitHub, eg the .db file
* src: Folder containing python files that make up the end-to-end ML pipeline in .py format
  * `__init__.py`: For python to treat 'src' directory as a package
  * `config.py`: Configuration for a pipeline run
  * `datapreprocessor.py`: Data preprocessing
  * `model_training.py`: Model training
* results: Optional folder containing training results and screenshots of successful pipeline run. Though not required in the AIAP assessment, I prefer to create this folder to store results for analysis and documentation purposes.
  * `training_results_<yyyyMMdd_hhmmss>.txt`: For each pipeline run to tune hyperparameters
  * `*.png`: Screenshot of successful pipeline run
* `eda.ipynb`: Exploratory data analysis notebook
* `requirements.txt`: List of dependencies
* `run.sh`: Main file to run


# 2. Flow of the pipeline

## 2.1 Full Pipeline
![Full Pipeline](results/readme_diagram_fullpipeline.png)
At a high-level, the full pipeline flow is as follows:
* run.sh
  * downloads the .db dataset from the URL to the data folder
  * runs the pipeline
* datapreprocessor.py
  * loads the .db dataset
  * preprocesses data
  * more details are in [section 2.2 'Data Preprocessing Pipeline'](#22-data-preprocessing-pipeline)
* model_training.py
  * reads configuration from config.py
  * loads the preprocessed dataset
  * initialises each of the 3 models
  * performs hyperparameter tuning
  * saves results of each pipeline run to a .txt file in the results folder

The model training pipeline is in the `model_training.py` file.
* It contains and runs the train_and_evaluate function, performing the steps outlined above
* Refer to the following sections for:
  * [section 4. Explanation of models selected](#4-explanation-of-models-selected)
  * [section 5. Explanation of hyperparameters tuned](#5-explanation-of-hyperparameters-tuned)
  * [section 6. Explanation of metrics used](#6-explanation-of-metrics-used)
  * [section 7. Explanation of results from our best, tuned models](#7-explanation-of-results-from-our-best-tuned-models)


## 2.2 Data Preprocessing Pipeline
![Data Preprocessing Pipeline](results/readme_diagram_datapreprocessor.png)
At a high-level, the data preprocessing flow is as follows:
* loads data
* cleans data
* group categories of interest
* bin numeric variables
* filter columns
* one-hot encoding
* validate data
* and only in the case of hyperparameter tuning, we
  * upsample the minority class (because 10% of customers do not subscribe to a term deposit) using SMOTE
  * split data into training and validation sets

The data preprocessing pipeline is in the `datapreprocessor.py` file.
* It has a 'DataPreprocessor' class which allows us to retrieve relevant attributes from the data pipeline, which can be used later in the model training pipeline
* The 'DataPreprocessor' class
  * Has supporting methods defined for each of the data preprocessing steps
  * Which can simplify our understanding of the data preprocessing pipeline flow, instead of having 1 function calling another function (and another function) and not sure where that originates and ends
  * Has the following methods
    * load_data: Loads data from SQLite database (.db file) into a dataframe
    * clean_df
      * Fill NAs for 'Housing Loan' and 'Personal Loan' with 'unknown'
      * Correct negative 'Campaign Calls' values to cutoff at 0
      * Fix 'Contact Mehod' values (grouped similar categories together)
      * Fix data types for categorical and numeric variables
    * group_categories: In specific categories of interest, group other categories which do not contribute to 'Subscription Status' classification into 'others'
    * bin numeric variables into categories
      * transform_campaign_calls: ['<=5', '6-10', '11+']
      * transform_age_groups: ['<=40', '41-60', '61-80', '81+']
      * transform_contact_days: ['<=50', '50-998', '999 (no contact)']
    * filter_selected_cols: Filters columns relevant to predict 'Subscription Status' class
    * onehotencode_df: One-hot encode categorical variables
    * Reference categories (i.e. categories with an 'average' or lower subscription rate identified during EDA):
        1. Occupation: others
        2. Education Level: literate
        3. Credit Default: yes
        4. Contact Method: telephone
        5. Age: <=40
        6. Previous Contact Days: <=50
        7. Subscription Status (our target variable): 'no' (ie. 0)
    * validate_preprocessing
    * Check for missing values
    * Check 'Subscription Status' (target variable) is in the dataframe
    * Check all features are numeric
    * split_and_balance_data: Upsample the minority subscription status 'no' class to balance the dataset then split into train and test set
    * preprocessing_only
      * runs the above data preprocessing steps except split_and_balance_data
    * preprocessing_for_inference
      * an optional method, which would be useful during inference (out of scope of this assessment)
      * runs 'preprocessing_only'
    * preprocessing_for_training
      * runs 'preprocessing_only' then 'split_and_balance_data'



# 3. Explanation of fields selected for classification
In the original dataset, there were 12 fields - 11 possible features and 1 target variable ('Subscription Status').

During exploratory data analysis (EDA), we discovered 6 fields which were the most relevant for 'Subscription Status' classification:
1. **Occupation - Retirees and students have a higher subscription rate**
2. **Education Level - illiterate has a higher subscription rate**
3. **Credit Default**
  * Keep 'No', 'Unknown', 'Yes' categorical values. 
  * **'No' has the highest subscription rate of 10%.** 'Unknown' has a lower subscription rate of approx 5%. 'Yes' has a 0% subscription rate
4. **Contact Method**
  * Combine 'Telephone' and 'telephone' into 'telephone'. Also combine 'Cell' and 'cellular' into 'cellular'
  * **'cellular' (15%) has a higher subscription rate than 'telephone' (5%)**
  * **customers collectively using cellular as a contact method has a 15% subscription rate, which is higher, maybe because cellular customers have a higher income which leads to a higher subscription rate**
5. **Age**
   * group into 4 bins (40 and below, 41 to 60, 61 to 80, 81 and above)
   * **from 41 to 60 years old, there is a slight increase in customers who do not subscribe. Maybe they are looking for more aggresive investments to grow their wealth before they retire. So avoid selling to customers between 41 and 60 years old**
6. **Previous Contact Days**
   * group into 3 groups (below 50, 51 to 998, 999)
   * **'999 (no contact)' has a higher subscription rate**
   * **for 80% of customers who subscribed, and for almost 100% of customers who did not subscribe to a term deposit, they have '999' for previous contact days, meaning the bank has not contacted them in the past**

For the 2 categorical fields 'Occupation' and 'Education Level', because the category values of interest do not span the full set of category values, we grouped the other categories into 'others' in the 'group categories of interest' step of our data preprocessing pipeline.


# 4. Explanation of models selected
In banking, decisions often need to be justified, to explain why a customer was approved or not approved for a product, where a loan or in this assessment, a term deposit. 

For this reason, we selected 3 models, prioritising explainability:
* Logistic Regression (LogisticRegression from [sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html))
  * Simple, interpretable, and fast to train
  * Acts as our baseline model
* Decision Tree (ClassificationTree from [sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html))
  * Simple, interpretable, and fast to train
* Explainable Boosting Machine (ExplainableBoostingClassifier from [Microsoft's interpret library](https://github.com/interpretml/interpret))
  * More complex
  * Offers similar accuracy to state of the art boosting models (eg XGBoost), and provides good explainability if visuals are required


# 5. Explanation of hyperparameters tuned
If we look at the hyperparameters used to tune each of the 3 selected models:
* Logistic Regression
  * class_weight does not need to be tuned because we have already performed SMOTE upsampling to balance the dataset in the data preprocessing pipeline
  * penalty: l1, l2
    * Explored the strength of loss penalty
  * C: 0.1, 1, 10
    * inverse of regularisation strength
    * Smaller C, higher regularisation
* Decision Tree
  * max_depth: 3, 5, 7, 10
    * higher depth, greater risk of overfitting
  * min_samples_split: 2, 5, 10
    * minimum samples before splitting at each tree node
    * too low can increase risk of overfitting
* Explainable Boosting Machine
  * learning_rate: 0.01, 0.02, 0.04, 0.06, 0.08, 0.1
    * learning_rate for boosting. Lower number for a slower, smoother learning

We also set the following parameters which were single values in the params_grid
  * seed for reproducibility
  * 'liblinear' solver in LogisticRegression (for small datasets and a binary classification problem)
  * 'max_iter' 1000 in LogisticRegression (to ensure convergence), because the default value of 100 was too low for our dataset
  

And in terms of the [best hyperparameters tuned for each model](results/training_results_20250510_023412.txt):
* Logistic Regression
  * C: 10
    * The highest C value (ie lowest regularisation) performed best
    * This allows for larger feature coefficients
  * penalty: l1
    * L1 regularisation performed best
    * This leads to a model which is more sparse, where some feature coefficients become zero
    * This can help with selecting relevant features and improving our understanding of how the model works
  * solver: liblinear
    * optimal for our small dataset, and allows us to explore tuning l1 vs l2 penalty
  * max_iter: 1000
    * To ensure convergence, because the default value of 100 was too low for our dataset
* Decision Tree
  * max_depth: 10
    * Allows 10 levels of decision splits to learn complex patterns, while preventing excessive overfitting (in the case of the default model behaviour which uses unlimited depth)
  * min_samples_split: 2
    * 2 is the default value, and it performed best
  * a higher depth or lower min_samples_split improves the fit of our model
  * the low min_samples_split may be reasonable for the model if there are some customer records with very rare characteristics that we want to learn from to classify better
* Explainable Boosting Machine
  * learning_rate: 0.01
    * The lowest learning rate performed best
    * Slower, smoother/more stable learning process for the model



# 6. Explanation of metrics used
When assessing the performance of our models, we used the following metrics relevant for binary classification:
* Accuracy
* Precision
* Recall
* F1 score
* ROC AUC
* Confusion Matrix
  * To visualise the True Positive (TP), True Negative (TN), False Positive (FP), False Negative (FN) numbers used to calculate the summary values - precision, recall, F1 score
* Classification Report
  * To visualise the precision, recall, F1 score, and support (ie number of records) for 'Subscription Status' class



# 7. Explanation of results from our best, tuned models
We will review [results from the last successful pipeline run](results/training_results_20250510_023412.txt)

In terms of the F1 score (which balances precision and recall)
* Decision Tree: F1 score 0.7001
  * Decision Tree had the highest F1 score, indicating it has the best balance between precision and recall
  * High Recall (81%): Captures 81% of true "yes" subscriptions
  * Low Precision (62%): Many false positives (in the denominator)
  * Decision Tree was the best at finding customers who tend to subscribe to a term deposit (ie. positives/"yes" subscriptions), than avoiding false alarms
  * The low precision and higher false positive/alarms mean that the bank may try to market to customers who are not likely to subscribe to a term deposit, which is not efficient and may decrease customer satisfaction
  * If revisit the bank's objective, the focus is to "accurately identify which clients are most likely to respond positively to these campaigns"
    * This means balancing between finding true positives (high recall) and avoiding false alarms (high precision)
    * And the metric which balances the 2 is the F1 score
    * So on the basis of the F1 score, we will choose the Decision Tree as our final model
* Explainable Boosting Machine: F1 score 0.6563
  * Precision: 0.6474
  * Recall: 0.6654
  * Slightly outperforms Logistic Regression
* Logistic Regression (Our baseline model): F1 score 0.6555
  * Precision: 0.6471
  * Recall: 0.6642




# 8. Some closing remarks on customer characteristics

Back in [section 3](#3-explanation-of-fields-selected-for-classification), we identified certain categorical fields and their categories of interest most relevant for 'Subscription Status' classification.

I would like to highlight the following:
1. Occupation - `Students have a higher subscription rate.`
   * Students might be the beneficiary and not the real buyer/customer of a term deposit
   * Instead, parents might be the real buyer/customer of a term deposit, on behalf of their children to fund their education
   * So the bank should check whether it has information on the parents of students in its database, and market to parents instead of students
2. Education Level - `illiterate has a higher subscription rate`
   * We need to assume that the term deposit here is a product that is easy to understand and save money, not like mini-bonds with a complex structure that caused the 2009 Financial Crisis
   * The illiterate might be subscribing to a 'vanilla' term deposit because it is one of the easiest financial products to understand and invest their money
   * However, I would like to challenge the team to consider other financial products which are similarly easy to understand, and can offer better returns than term deposits to illiterate customers. The intention is not to 'bias' the illiterate to earn lower returns, when they can actually earn better returns with other financial products
3. Credit Default - `'Yes' has a 0% subscription rate`
   * Is the subscription rate of a term deposit 0% for those who defaulted on credit in the past
     * a. even when the bank sells the term deposit to them?
     * b. or is it because the bank has an internal process which prevents the sale of term deposits to those who defaulted on credit in the past?
   * Questions (a) and (b) above should be explored further
   * For now, I have a strong feeling that (b) is the answer
   * And this leads to my next question, if a customer pays back their debt in full,
     * c. within the short term (eg 6 months) when the customer's credit score is still low, does the bank still prevent them from buying a term deposit?
     * d. after a longer duration (eg 2 to 3 years) when the customer's credit score has improved, does the bank still prevent them from buying a term deposit?
   * Questions (c) and (d) above should also be explored further



# 9. Screenshots of successful pipeline run and folder structure

Screenshot 1 - Run 5 of the pipeline on local machine (on 2025-05-10 UTC Time 023412, ie. SG Time 103510)
![Screenshot 1 run 5 pipeline](results/run5_pipeline_2025-05-10_023412_SGtime10_35_10.png)



Screenshot 2 - Folder structure of the repository (on 2025-05-10 UTC Time 023412, ie. SG Time 103510)
* repo folder: aiap20-kaiquan-mah-017B
* data folder: aiap20-kaiquan-mah-017B/data
* src folder: aiap20-kaiquan-mah-017B/src
* results folder: aiap20-kaiquan-mah-017B/results

![Screenshot 2 run 5 folder structure and files](results/run5_subfolder_contents_2025-05-10_023412_SGtime10_35_10.png)


Screenshot 3 - Run 6 of the pipeline on GitHub Actions (on 2025-05-10 SG Time 105139)
* You can verify the pipeline runs in [GitHub Actions](https://github.com/kaiquanmah0/aiap20-kaiquan-mah-017B/actions)
![Screenshot 3 run 6 GitHub Actions](results/run6_GitHubActions_2025-05-10_SGtime10_51_39.png)

