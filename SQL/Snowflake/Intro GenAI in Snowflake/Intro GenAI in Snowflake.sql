How accurate are Snowflake Cortex AI’s translation and sentiment analysis functions?
Cortex AI leverages large language models (LLMs) for translation and sentiment analysis, providing high accuracy. 
However, results may vary based on
- CONTEXT,
- LANGUAGE complexity, and
- INDUSTRY-specific jargon.
It’s recommended to validate outputs for critical business applications.


  
Can I integrate Snowflake Cortex AI with other AI services or external tools?
Yes! You can combine Cortex AI functions with
- Snowpark to build advanced ML workflows or 
- integrate it into Tableau or PowerBI to VIZ insights

  
What are some best practices for using Snowflake Cortex AI efficiently?
- Optimize queries by SELECTING ONLY NECESSARY text FIELDS.
- PREPROCESS text data to REMOVE NOISE before applying AI functions.
- Use CACHING and INDEXING for frequently accessed text summaries.
- MONITOR query COSTS to avoid unnecessary compute usage.







RECAP - PYTHON
```
snowflake.cortex.summarize
snowflake.cortex.complete
snowflake.cortex.classify_text
snowflake.cortex.translate
snowflake.cortex.extract_answer


  
  
response = summarize(review)



  
response = complete(model='llama3.1-8b',
                  prompt = prompt,
                  # Set temperature and limit tokens
        options={
                    'temperature': 0.3,
                    'max_tokens': 80
                    }
                )

  
def classification(text):
    # Use the relevant Snowflake Cortex function 
    result = classify_text(
        str_input=text,
        categories=categories
    )
    # Convert result into a dictionary 
    result_dict = json.loads(result)
    return result_dict['label']

# Apply the classification function
reviews["category"] = reviews["DESCRIPTION"].apply(classification)
reviews["category"].value_counts()





  
translated = translate(text=review, 
                  from_language='es', 
                  to_language='en')

  
response = extract_answer(
    from_text=review,
    question='What is the main issue with this review?'
)  
```




  
RECAP - SQL
```SQL
AI_COMPLETE
AI_SENTIMENT
  
AI_COMPLETE(
  'llama3.1-8b',
  -- Complete a prompt
  PROMPT('Write a polite 1-sentence response to this hotel review: {0}.', DESCRIPTION),
  -- Set temperature and limit tokens
  {'temperature': 0.5, 'max_tokens': 60}
) AS completion


AI_SENTIMENT(DESCRIPTION)['categories'][0]['sentiment']
```

===============================


  
  



-- Snowflake notebook ipynb
```python
# Import python packages
import streamlit as st
import pandas as pd

# We can also use Snowpark for our analyses!
from snowflake.snowpark.context import get_active_session
session = get_active_session()
```

```sql
-- Welcome to Snowflake Notebooks!
-- Try out a SQL cell to generate some data.
SELECT 'FRIDAY' as SNOWDAY, 0.2 as CHANCE_OF_SNOW
UNION ALL
SELECT 'SATURDAY',0.5
UNION ALL 
SELECT 'SUNDAY', 0.9;
```


```python
# Then, we can use the python name to turn cell2 into a Pandas dataframe
my_df = cell2.to_pandas()

# Chart the data
st.subheader("Chance of SNOW ❄️")
st.line_chart(my_df, x='SNOWDAY', y='CHANCE_OF_SNOW')

# Give it a go!
st.subheader("Try it out yourself and show off your skills 🥇")
```








====================================================
  
--python variable substitution
```python
# Create a country filter for hotel reviews in Mexico
country_filter = 'Mexico'
```

``sql
SELECT country, COUNT(*) AS num_reviews
FROM HOTELS.REVIEWS
-- Apply the country_filter
WHERE country = '{{country_filter}}'
GROUP BY country
```
  country num_reviews
0	Mexico	1353













====================================================

Summarizing a review
-- packages: select 'snowflake-ml-python'
-- similar to a pip install
  

```python
review = """
It was the last night of our road trip and we wanted 
to treat ourselves and stay somewhere a bit nicer. 
We stayed out of season so it was affordable. 
Beautiful hotel and great service.
We called prior to arriving to ask about parking. 
They said not to worry and they would park the car when we arrived.
They didn't; however tell us parking was 45euro a night. 
That is my only criticism. We could have moved the car
but we felt a bit embarrassed so we left it there for the night (we didn't want to look cheap). 
Loved the hotel I just think they should be a bit clearer about that 
sort of cost because it really did add to the price of our stay as a couple 
who don't often frequent five-star hotels. 
Otherwise; lovely staff. We felt very welcome.
"""

# Import the summarize function
from snowflake.cortex import summarize

# Summarize the review
response = summarize(review)
print(response)
```
  
On our last night of the road trip, we stayed at an expensive hotel with great service, but were surprised by a 45 euro nightly parking fee, which was not disclosed beforehand. 
Despite this, we enjoyed the hotel and the staff were welcoming.





  


  


====================================================

Extracting and responding to a review
-- packages: select 'snowflake-ml-python'

```sql
SELECT DESCRIPTION
FROM HOTELS.REVIEWS
WHERE date = '2023-07-14'
    AND RATING < 6
```

  
```python
# Import packages
import pandas as pd
from snowflake.cortex import complete

# Convert the review to a pandas DataFrame
df = cell1.to_pandas()

# Extract the review as a string
review = df["DESCRIPTION"].iloc[0]
print(review)
# The entrance is quite good but my room has a very old; dirty carpet. 
# Even though I stayed in a premium room; it was not spacious at all; the rolling chair was hard to accommodate even by the desk. 
# I selected this hotel based on reviews which were misleading. There is no question I paid way too much for a very bad room!



prompt = f"""Write a 2-sentence response to the following review:\n---\n{review}
        \n---\nAcknowledge the feedback and outline planned actions. 
        Return only the response text."""

# Generate and print a response
response = complete(model='llama3.1-8b',
                    prompt = prompt,
                    # Set temperature and limit tokens
					options={
                    	'temperature': 0.3,
                    	'max_tokens': 80
                    	}
                	)
print(response)
```
We apologize for the disappointing experience in our premium room, particularly with the condition of the carpet and the comfort of the furniture. 
We will take your feedback seriously and take immediate action to address these issues, including deep cleaning and replacing the carpet, 
as well as reviewing our room layout and furniture to ensure a more comfortable and spacious experience for our guests.





  



Generating responses with AI_COMPLETE()
In this exercise, you'll use the AI_COMPLETE() function in SQL to generate batch responses for multiple reviews.
Note: No packages need to be installed - AI_COMPLETE() works natively in SQL cells.
```sql
SELECT 
  DESCRIPTION,
  -- Generate a response
  AI_COMPLETE(
    'llama3.1-8b',
    -- Complete a prompt
    PROMPT('Write a polite 1-sentence response to this hotel review: {0}.', DESCRIPTION),
    -- Set temperature and limit tokens
    {'temperature': 0.5, 'max_tokens': 60}
  ) AS completion
FROM HOTELS.REVIEWS
WHERE RATING > 8
AND COUNTRY = 'France'
ORDER BY DATE DESC
LIMIT 2

```
,DESCRIPTION,COMPLETION
0,Had an absolutely wonderful stay at the Hyatt Nice!,"Thank you so much for sharing your wonderful experience at our hotel, we're thrilled to hear that you had a great stay at the Hyatt Nice!"
1,Awesome place to stay & relatively cheap for the Monaco Area. The Nobu inside is a great addition to the experience as well,"""Thank you for sharing your wonderful experience at our hotel, we're glad you enjoyed your stay and appreciated the convenience of our Nobu restaurant!"""


  






===================================================

text classification
-- packages: select 'snowflake-ml-python'

```python
import pandas as pd
import json

# Import the required function
from snowflake.cortex import classify_text
```

```sql
SELECT *
FROM HOTELS.REVIEWS
WHERE city = 'Geneva'
	AND RATING < 6
    ORDER BY DATE DESC
LIMIT 5
```
,DATE,RATING,DESCRIPTION,HOTEL_NAME,CITY,COUNTRY,LANGUAGE
0,2023-07-14,4,The entrance is quite good but my room has a very old; dirty carpet. Even though I stayed in a premium room; it was not spacious at all; the rolling chair was hard to accommodate even by the desk. I selected this hotel based on reviews which were misleading. There is no question I paid way too much for a very bad room!,Warwick Geneva,Geneva,Switzerland,en
1,2023-06-22,4,We booked two rooms for a family of 4. One of the rooms had such a strong cigarette smell that it was unbearable to sleep in. 3 of us ended up squeezing in one room and I didn’t sleep the whole night because of the strong smell.,Warwick Geneva,Geneva,Switzerland,en
2,2023-06-14,4,We arrived at the hotel after midnight and they said there was no room for us; despite a confirmed reservation.  We had called up earlier in the day to say that we wouldn’t arrive until after midnight and they had said ‘no problem’.  The management was very apologetic and found us a room (very small) in a nearby hotel; but we were less than pleased!,Warwick Geneva,Geneva,Switzerland,en
3,2023-06-02,2,DONT STAY HERE. INSECTS IN THE BED. If I could share ZERO stars; I would. I checked into this hotel on the night of 29 May. I was escorted to a room with a door smaller than the rest of the rooms in the hallway; only wide enough for my one checked luggage to fit through. I requested to be moved to the proper room; which they obliged; but only after claiming this was technically an upgrade (IT WASNT — it is the room I originally paid for. A classic room). Nonetheless; i didnt complain. As I got ready for bed; I moved the pillows and blanket out of place only to find 8-10 small insects buried underneath (see photo of what it looked like). These insects also flew on me throughout the night. I called the reception and told them id like to check out and request a refund and they said I would have to handle this with Expedia; who I booked and prepaid the four nights with. There were also no available hotels at that time for me to go to (it was midnight). I waited until day break and went down to the reception to tell them what happened. They very nonchalantly told me there were flies during this time of year. Upon calling expedia to resolve the matter and get my money back for the nights i didnt stay there; the hotel refused. DONT STAY HERE unless you want bugs in your hair and clothes. I’m still waiting for Expedia to get back to me on resolving the issue. So disappointed in how well this hotel is rated on Expedia.,Warwick Geneva,Geneva,Switzerland,en
4,2023-02-24,4,The hotel’s fine.  But they outrageously added minbar items to my bill and charged me after i’d left the hotel.  They won’t acknowledge my queries on this.,Warwick Geneva,Geneva,Switzerland,en



```python
categories = ["overall_experience", "location", "staff",
            "food_beverages", "facilities"]

reviews = cell2.to_pandas()

def classification(text):
    # Use the relevant Snowflake Cortex function 
    result = classify_text(
        str_input=text,
        categories=categories
    )
    # Convert result into a dictionary 
    result_dict = json.loads(result)
    return result_dict['label']

# Apply the classification function
reviews["category"] = reviews["DESCRIPTION"].apply(classification)
reviews["category"].value_counts()
  
```
category,count
overall_experience,3
facilities,2






==================================================================

sentiment analysis

```sql
SELECT 
    DESCRIPTION, 
    
    -- Perform sentiment analysis
    AI_SENTIMENT(DESCRIPTION)['categories'][0]['sentiment']
FROM HOTELS.REVIEWS
WHERE hotel_name = 'Hyatt Regency Palais'

    -- Filter records for Sep 2023
	AND EXTRACT(MONTH FROM DATE) = 9
    AND EXTRACT(YEAR FROM DATE) = 2023
ORDER BY DATE DESC
```

,DESCRIPTION,AI_SENTIMENT(DESCRIPTION)['CATEGORIES'][0]['SENTIMENT']
0,Had an absolutely wonderful stay at the Hyatt Nice!,"""positive"""
1,Very standard hotel. Great location.,"""positive"""
2,Very friendly and helpful Staff at the Hotel,"""positive"""
3,Hotel was in a prime location and the service we received was outstanding. Concierge was a real highlight taking care of everting we wanted to book. Extremely helpful.,"""positive"""
4,We absolutely loved the Hyatt Regency Nice. It was a wonderful hotel with excellent staff,"""positive"""









===================================================

Translate
-- packages: select 'snowflake-ml-python'

```sql
SELECT DESCRIPTION
FROM HOTELS.REVIEWS
-- Filter for Spanish reviews
WHERE language = 'es'
ORDER BY DATE DESC 
LIMIT 1;
```
,DESCRIPTION
0,Excelente hotel super limpieza y buena atencion


  
```python
df = cell1.to_pandas()
review = df["DESCRIPTION"].iloc[0]
print(review)

# Import the relevant function
from snowflake.cortex import translate

# Call the function and print the result
translated = translate(text=review, 
                  from_language='es', 
                  to_language='en')

print(translated)
```
Excellent hotel, super clean and good care


  












-- packages: select 'snowflake-ml-python'

```sql
SELECT DESCRIPTION
FROM HOTELS.REVIEWS
WHERE LANGUAGE = 'fr'
-- Sort results by date from newest to oldest
ORDER BY DATE DESC
LIMIT 1;
```
,DESCRIPTION
0,Très bon hôtel comme attendu. On s’occupe de vous sans hésitation. Je recommande




```python
df = cell1.to_pandas()
review = df["DESCRIPTION"].iloc[0]

print(review)

# Import the relevant function
from snowflake.cortex import translate

# Translate into English and German
english = translate(text=review, 
                  from_language='fr', 
                  to_language='en')

german = translate(text=english, 
                  from_language='en', 
                  to_language='de')

# Print the original, English, and German reviews
print(f"Original (French): {review}\nEnglish: {english}\nGerman: {german}")
```
Original (French): Très bon hôtel comme attendu. On s’occupe de vous sans hésitation. Je recommande  
English: Very good hotel as expected. They take care of you without hesitation. I recommend  
German: Sehr gutes Hotel, wie erwartet. Sie kümmern sich ohne zu zögern um Sie. Ich empfehle





The translate() function does not have a temperature argument - the model will always translate content literally from one language to another.





  

===================================================

Extract ans
-- packages: select 'snowflake-ml-python'

```SQL
SELECT DESCRIPTION
FROM HOTELS.REVIEWS
-- Set the appropriate filters
WHERE HOTEL_NAME = 'Grand Fiesta Americana'
    AND DATE = '2023-07-30'
    AND RATING < 6
LIMIT 1;
```
,DESCRIPTION
0,We paid more to stay in this hotel due to the kids pool area; amenities and reviews however once there; the gym was closed and in construction; kids pool area inactive (picture taken from the top of the hotel and the kids pool section is closed). The room had drainage issue in the bathtub and sink and took them 2 days to try to fix it without success. We kept requesting to change room without success and gave up to avoid further stress. Food was ok but not the best. The daily activity journal we only received on the last two days (we stayed 5 days) and on the date of the activity that makes you loose the morning free activity if you are interested. I would suggest to put the journal on the day before in the room when they set up the beds. The beach area is restricted and if you like to have a walk; choose another hotel. Overall unfortunately; I would not recommend the hotel that is pricey for what they offer.




```python
df = cell1.to_pandas()
review = df["DESCRIPTION"].iloc[0]

print(review)

# Import the relevant function
from snowflake.cortex import extract_answer

# Find out what the main issue was
response = extract_answer(
    from_text=review,
    question='What is the main issue with this review?'
)

# Print the response
print(response)

```
[  
  {  
    "answer": "the gym was closed and in construction ; kids pool area inactive ( picture taken from the top of the hotel and the kids pool section is closed ). the room had drainage issue",  
    "score": 0.72192985  
  }  
]


score is between 0 and 1
A score of 1 indicates absolute certainty, so this is quite unlikely.
Anything below approx 0.7 might suggest that a human review would be beneficial, as the model is not particularly confident in how well it has answered your question.


















  


--extract foreign language ans (originally in foreign language)
-- packages: select 'snowflake-ml-python'
```SQL
SELECT DESCRIPTION
FROM HOTELS.REVIEWS
-- Filter for Italian reviews
WHERE language = 'it'
ORDER BY DATE DESC 
LIMIT 1;
```
,DESCRIPTION
0,Buona struttura personale preparato e disponibile.



```python
df = cell1.to_pandas()
review = df["DESCRIPTION"].iloc[0]

print(review)

# Import the relevant function
from snowflake.cortex import extract_answer

# Find out what the main issue was
response = extract_answer(
    from_text=review,
    question='What is this review about?'
)

# Print the response
print(response)

```
[  
  {  
    "answer": "struttura personale preparato e disponibile",  
    "score": 0.0013839254  
  }  
]


Response was in the original foreign language
Looks like if you need to extract an answer about a review, then you should translate it first.








  


===================================================

Multi-step AI workflow

--SUMMARISE THEN CLASSIFY
-- packages: select 'snowflake-ml-python'

```SQL
SELECT DESCRIPTION
FROM HOTELS.REVIEWS
WHERE LANGUAGE = 'en'
ORDER BY DATE
-- Return a single row
LIMIT 1
```
,DESCRIPTION
0,You know what to expect in Cannes - crazy prices and properties that are stuck in a time warp. This was my second time at the Majestic - the outside of the hotel is lovely; lobby is gilded and elegant; and Le Fouquet is nice but over the top expensive; but unless you get a modernized room; be prepared to be very disappointed. Room service charges 15 euros for silverware; Diet Coke from the minibar is 11 euros; wifi with a very weak signal is 15 euros per day. You get the idea. Best reason to stay at the Majestic is that it is literally 2 blocks from Palais des Festivals.



```python
df = cell1.to_pandas()
review = df["DESCRIPTION"].iloc[0]

print(review)

from snowflake.cortex import summarize, classify_text
  
# Summarize the English review
summarized = summarize(
    text=review
)

print(summarized)
# The Majestic hotel in Cannes is beautiful but expensive, with high prices for food, room service, wifi, and outdated rooms. 
# The best reason to stay is its proximity to Palais des Festivals.
  


# Create categories
categories = ['staff', 
              'location', 
              'cleanliness', 
              'food and drink']

# Classify the summarized review
review_category = classify_text(
    str_input=review,
    categories=categories
)

# Print the category
print(review_category)
```
{  
  "label": "location"  
}

















-- TRANSLATE (from foreign language to EN) > SUMMARISE > COMPLETE/RESPOND > TRANSLATE (from EN back to original foreign language)
-- packages: select 'snowflake-ml-python'

```sql
SELECT DESCRIPTION
FROM HOTELS.REVIEWS
WHERE LANGUAGE = 'es'
ORDER BY DATE
LIMIT 1;
```
,DESCRIPTION
0,Buen hotel y bien situado pero desafortunadamente no me toco buena suerte con el servicio; el aire no servía; pedí la cama extra tres veces; la cafetera estaba dañada; y me sacaron las maletas fuera porque argumentaron que no hice Check out; siendo que era un día despues; pero su sistema lo marco antes; una total descortesía hecharme del cuarto y cancelar mis llaves; regresar de caminar y darse cuenta que han tomado tus cosas fuera es increíble y mas aun sin ninguna disculpa; yo no volvería ahí aunque la vrd el hotel es bueno y su jubilación el trato me decepciono



```python
df = cell1.to_pandas()
review = df['DESCRIPTION'].iloc[0]

print(review)

from snowflake.cortex import translate, summarize, complete

# Translate the review into English
translated = translate(
    text=review,
    from_language='es',
    to_language='en'
)
print(translated)
# Good hotel and well located but unfortunately I did not have good luck with the service; the air did not work; I asked for the extra bed three times; the coffee pot was broken; and they took my bags out because they argued that I did not check out; being that it was a day later; but their system marked it before; a total discourtesy to kick me out of the room and cancel my keys; returning from walking and realizing that they have taken your things out is incredible and even more so without any apology; I would not go back there even though the hotel is good and its retirement the treatment disappointed me  

  
# Summarize the English review
summarized = summarize(
    text=translated
)
print(summarized)
# The hotel was good but the service was disappointing; 
# the air conditioning didn't work, extra bed was not provided, coffee pot was broken, bags were taken despite not checking out, and there was no apology for the inconvenience.




# Generate a response
response = complete(
    model='llama3.1-8b',
    prompt=f"""Write a short, professional response to the following review:\n---\n{summarized}.
               \n---\nReturn only the response text.""",
    options={
        'temperature': 0.2,
        'max_tokens': 100
    }
)
print(response)
# "I apologize for the disappointing service you experienced during your stay. 
# We fell short of our standards in several areas, including the air conditioning, extra bed, coffee pot, and handling of your bags.
# I will share your feedback with our team to ensure we take corrective action to prevent such issues in the future.
# We appreciate your feedback and hope you will give us the opportunity to serve you better in the future."  
  

# Translate the response into Spanish
spanish_response = translate(
    text=response,
    from_language='en',
    to_language='es'
)

print(spanish_response)
```
"Me disculpo por el decepcionante servicio que experimentó durante su estadía.
No cumplimos con nuestros estándares en varias áreas, incluyendo el aire acondicionado, cama adicional, cafetera y manejo de sus maletas.
Compartiré su opinión con nuestro equipo para asegurar que tomemos medidas correctivas para prevenir tales problemas en el futuro.
Agradecemos su opinión y esperamos que nos dé la oportunidad de servirle mejor en el futuro."






