import pickle
import time
import pandas as pd
from pandasql import sqldf
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Union
import json

import re # Regular expressions
import string # String manipulation
import math # Math operations

from deep_translator import GoogleTranslator # To translate non english words
from num2words import num2words # To convert numbers and ordinals to words
from deep_translator import GoogleTranslator # To translate non english words
import emoji # For emoji character manipulation
# import pattern
# from pattern.en import lemma

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler, OrdinalEncoder
from sklearn.compose import make_column_selector, make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

# from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from textwrap import wrap
from nltk.stem import WordNetLemmatizer
# nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
# nltk.download('vader_lexicon')


def execute_train(csv_url):
    data = {"message": f"Getting the CSV data from {csv_url}.."}
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"
    time.sleep(0.5)
    df = pd.read_csv(csv_url)
    row, col = df.shape
    data['message'] = f"File downloaded, found {col} columns and {row} rows"
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"
    time.sleep(0.5)


    data['message'] = f"Renaming columns..."
    # Rename columns to a proper name
    # Create first a dictionary as a map of the old column names and the new column names
    cols_to_rename = {
        'Timestamp': 'timestamp',
        'Email Address': 'email',
        'DATA PRIVACY ACT\n\nTo ensure the protection of personal information collected through this Google Form, we are committed to complying with the provisions of Republic Act No. 10173 or the Data Privacy Act of 2012. This law protects the personal information of individuals by regulating its collection, use, storage, and distribution. \n\nWe take data privacy seriously and assure you that any information shared with us will be kept confidential and used only for the purpose stated in this form.\n\nBy clicking the "Agree", you consent to the use of your data for the said purpose in accordance with the Data Privacy Act.': 'data_privacy',
        'FULL NAME: (Please select)': 'evaluator',
        'POSITION': 'position',
        'PRESENT DURING LOCAL CAF 2024?': 'present',
        'I WANT TO EVALUATE:': 'evaluatee',
        'He/She was well-prepared for his/her responsibilities during the Local CAF 2024?': 'responsibility_rating',
        'He/She effectively communicated with his/her team members before and during the Local CAF 2024?': 'team_communication_rating',
        'He/She was able to delegate tasks effectively and ensure he/she were completed on time?': 'task_delegation_rating',
        'He/She remained calm and collected under pressure during the event?': 'calmness_rating',
        'He/She was able to adapt to unexpected challenges and changes before or during the Local CAF 2024?': 'adaptability_rating',
        'He/She consistently displayed a positive and enthusiastic attitude throughout the Local CAF 2024?': 'attitude_rating',
        'Do you think he/she face any difficulties with communication or collaboration during the event?': 'no_comm_collab_rating',
        'In any external factors that threatened the success of the event, did he/she respond relatively?': 'external_resp_rating',
        'He/She did not effectively manage his/her time during the event?': 'no_time_management_rating',
        'He/She did not collaborate effectively with other CSG officers or committees?': 'no_collab_rating',
        'He/She was not flexible in his/her approach to problem-solving during the Local CAF 2024?': 'no_flexible_rating',
        'He/She did not take responsibility for his/her mistakes or the mistakes of his/her team?': 'no_accountability_rating',
        'Please answer in ENGLISH: \nWhat do you think is his/her greatest contribution and what opportunity did he/she unlock during Local CAF 2024 event? (Please insert "N/A" if none)': 'event_contribution',
        'Do you have any comment, suggestion/s, and recommendation/s?  (Please insert "N/A" if none)': 'comment_feedback'
    }

    # Execute the rename using the dictionary
    df = df.rename(columns=cols_to_rename)
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    data['message'] = f"Column rename completed. New column names are as follows: {df.columns}"
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    # Drop unnecessary columns
    # Set the columns to be dropped
    columns_to_drop = ['timestamp','email','data_privacy']
    data['message'] = f"Removing unneeded columns: {str(columns_to_drop)}"
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    # Check if columns to drop are still in the data frame
    existing_cols = df.columns.intersection(columns_to_drop)

    # If columns to drop is still in the dataframe, drop it in the dataframe
    # Else, show info of not found or already removed
    if len(existing_cols) > 0:
        df = df.drop(columns=existing_cols)
        data['message'] = f"Unnecessary columns successfully removed"
    else:
        data['message'] = f"Failed to remove unnecessary columns"
    
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"
    
    data['message'] = f"Deduplicating data..."
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"
    
    # Check for duplicates
    hasDuplicates = df.duplicated().any()

    # If there are duplicates in the dataset, we will drop them
    # Else, show an info of no duplicates
    if hasDuplicates:
        df.drop_duplicates(inplace=True)
        data['message'] = f"Duplicates removed"
    else:
        data['message'] = f"No duplicates removed"
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"


    data['message'] = f"Transforming the performance rating data in the dataset..."
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    data['message'] = f"Transforming positive-rating columns..."
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"
    # Update those column with the right data
    # For positive type of rating columns
    positive_rating_value = {
        'Strongly Agree': 5,
        'Agree': 4,
        'Neutral': 3,
        'Disagree': 2,
        'Strongly Disagree': 1
    }

    # Replace values of the column based on the positive rating value map
    df['responsibility_rating'] = df['responsibility_rating'].replace(positive_rating_value)
    df['team_communication_rating'] = df['team_communication_rating'].replace(positive_rating_value)
    df['task_delegation_rating'] = df['task_delegation_rating'].replace(positive_rating_value)
    df['calmness_rating'] = df['calmness_rating'].replace(positive_rating_value)
    df['adaptability_rating'] = df['adaptability_rating'].replace(positive_rating_value)
    df['attitude_rating'] = df['attitude_rating'].replace(positive_rating_value)
    df['attitude_rating'] = df['attitude_rating'].replace(positive_rating_value)
    df['external_resp_rating'] = df['external_resp_rating'].replace(positive_rating_value)

    data['message'] = f"Transforming positive-rating columns completed"
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    data['message'] = f"Transforming negative-rating columns..."
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"
    
    # For negative type of rating columns
    negative_rating_value = {
        'Strongly Agree': 'Strongly Disagree',
        'Agree': 'Disagree',
        'Neutral': 'Neutral',
        'Disagree': 'Agree',
        'Strongly Disagree': "Strongly Agree"
    }

    # Replace values of the column based on the negative rating value map
    df['no_comm_collab_rating'] = df['no_comm_collab_rating'].replace(negative_rating_value)
    df['no_time_management_rating'] = df['no_time_management_rating'].replace(negative_rating_value)
    df['no_collab_rating'] = df['no_collab_rating'].replace(negative_rating_value)
    df['no_flexible_rating'] = df['no_flexible_rating'].replace(negative_rating_value)
    df['no_accountability_rating'] = df['no_accountability_rating'].replace(negative_rating_value)

    # Replace values of the column based on the positive rating value map
    df['comm_collab_rating'] = df['no_comm_collab_rating'].replace(positive_rating_value)
    df['time_management_rating'] = df['no_time_management_rating'].replace(positive_rating_value)
    df['collab_rating'] = df['no_collab_rating'].replace(positive_rating_value)
    df['flexible_rating'] = df['no_flexible_rating'].replace(positive_rating_value)
    df['accountability_rating'] = df['no_accountability_rating'].replace(positive_rating_value)

    # We need to remove the columns that are negatively-rated
    negative_rated_cols = ["no_comm_collab_rating", "no_time_management_rating", "no_collab_rating", "no_flexible_rating", "no_accountability_rating"]
    df = df.drop(columns=negative_rated_cols)

    data['message'] = f"Transforming negative-rating columns completed"
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    data['message'] = f"Transforming Comments and Feedback columns.."
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    data['message'] = f"Transforming to lower case.."
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"
        # Transform the columns into lower case
    df['comment_feedback'] = df['comment_feedback'].str.lower()
    df['event_contribution'] = df['event_contribution'].str.lower()

    data['message'] = f"Imputing values to the columns with null values.."
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"
    # Check for blank/null data in each columns, if there are blank columns, impute accordingly
    # Impute null/blank values to 'no review'
    df['comment_feedback'].fillna(value='no review', inplace=True)
    df['event_contribution'].fillna(value='no review', inplace=True)

    # Create map for replacing no review
    replace_na =  {
        'n/a': 'no review',
        'na': 'no review',
        'n/a\n': 'no review',
        'm/a': 'no review'
    }

    df['comment_feedback'] = df['comment_feedback'].replace(replace_na)
    df['event_contribution'] = df['event_contribution'].replace(replace_na)
    
    data['message'] = f"Transforming Comments and Feedback columns completed"
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"
    
    data['message'] = f"Dropping rows with noise data (e.g. no review values).."
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    # Dropping rows with 'no review' values
    df = df[(df['comment_feedback'] != 'no review') & (df['event_contribution'] != 'no review')] 

    data['message'] = f"Noise values removed."
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"


    data['message'] = f"Translating non-English words.."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"
    
    # Function to translate text
    def translate_text(text):
        translated = GoogleTranslator(source='filipino', target='en').translate(text)
        return translated
    
    # Translate the columns for non-English texts
    df['new_comment_feedback'] = df['comment_feedback'].apply(translate_text)
    df['new_event_contribution'] = df['event_contribution'].apply(translate_text)

    data['message'] = f"Translation completed."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    data['message'] = f"Expanding contractions.."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"


    # Create list of contractions and its expanded form
    contractions_dict = { "ain't": "are not","'s":" is","aren't": "are not",
                     "can't": "cannot","can't've": "cannot have",
                     "'cause": "because","could've": "could have","couldn't": "could not",
                     "couldn't've": "could not have", "didn't": "did not","doesn't": "does not",
                     "don't": "do not","hadn't": "had not","hadn't've": "had not have",
                     "hasn't": "has not","haven't": "have not","he'd": "he would",
                     "he'd've": "he would have","he'll": "he will", "he'll've": "he will have",
                     "how'd": "how did","how'd'y": "how do you","how'll": "how will",
                     "I'd": "I would", "I'd've": "I would have","I'll": "I will",
                     "I'll've": "I will have","I'm": "I am","I've": "I have", "isn't": "is not",
                     "it'd": "it would","it'd've": "it would have","it'll": "it will",
                     "it'll've": "it will have", "let's": "let us","ma'am": "madam",
                     "mayn't": "may not","might've": "might have","mightn't": "might not",
                     "mightn't've": "might not have","must've": "must have","mustn't": "must not",
                     "mustn't've": "must not have", "needn't": "need not",
                     "needn't've": "need not have","o'clock": "of the clock","oughtn't": "ought not",
                     "oughtn't've": "ought not have","shan't": "shall not","sha'n't": "shall not",
                     "shan't've": "shall not have","she'd": "she would","she'd've": "she would have",
                     "she'll": "she will", "she'll've": "she will have","should've": "should have",
                     "shouldn't": "should not", "shouldn't've": "should not have","so've": "so have",
                     "that'd": "that would","that'd've": "that would have", "there'd": "there would",
                     "there'd've": "there would have", "they'd": "they would",
                     "they'd've": "they would have","they'll": "they will",
                     "they'll've": "they will have", "they're": "they are","they've": "they have",
                     "to've": "to have","wasn't": "was not","we'd": "we would",
                     "we'd've": "we would have","we'll": "we will","we'll've": "we will have",
                     "we're": "we are","we've": "we have", "weren't": "were not","what'll": "what will",
                     "what'll've": "what will have","what're": "what are", "what've": "what have",
                     "when've": "when have","where'd": "where did", "where've": "where have",
                     "who'll": "who will","who'll've": "who will have","who've": "who have",
                     "why've": "why have","will've": "will have","won't": "will not",
                     "won't've": "will not have", "would've": "would have","wouldn't": "would not",
                     "wouldn't've": "would not have","y'all": "you all", "y'all'd": "you all would",
                     "y'all'd've": "you all would have","y'all're": "you all are",
                     "y'all've": "you all have", "you'd": "you would","you'd've": "you would have",
                     "you'll": "you will","you'll've": "you will have", "you're": "you are",
                     "you've": "you have"}

    # Regular expression for finding contractions
    contractions_re = re.compile('(%s)' % '|'.join(contractions_dict.keys()))

    # Function for expanding contractions
    def expand_contractions(text,contractions_dict=contractions_dict):
        def replace(match):
            return contractions_dict[match.group(0)]
        return contractions_re.sub(replace, text)

    # Expanding Contractions in the reviews
    df['new_comment_feedback'] = df['new_comment_feedback'].apply(lambda x:expand_contractions(x))
    df['new_event_contribution'] = df['new_event_contribution'].apply(lambda x:expand_contractions(x))

    data['message'] = f"Expanding contractions completed."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    data['message'] = f"Removing punctuations.."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    # Remove punctuations
    punctuation_to_replace = string.punctuation.replace('[^\w\s]', '')

    df['new_comment_feedback'] = df['new_comment_feedback'].apply(lambda x: ''.join([' ' if char in punctuation_to_replace else char for char in x]))
    df['new_event_contribution'] = df['new_event_contribution'].apply(lambda x: ''.join([' ' if char in punctuation_to_replace else char for char in x]))

    data['message'] = f"Removing punctuations completed."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    data['message'] = f"Translation of numbers into words.."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    # Function to translate numbers into words
    def translate_numbers(text):
        words = text.split()
        translated_words = []
        # Loop through the words in the columns
        for word in words:
            if word.isdigit(): # Check if the word is a digit
                # If it is a number, translate the number to words then append to translated_words variable
                translated_words.append(num2words(int(word)))
            elif word.endswith(('st', 'nd', 'rd', 'th')) and word[:-2].isdigit(): # Check if the word is an ordinal number (1st, 2nd, 3rd..)
                # If it is an ordinal number, translate the number to words then append to translated_words variable
                translated_number = num2words(int(word[:-2]), ordinal=True)
                translated_suffix = word[-2:]  # Get the ordinal suffix

                # Append translated number and suffix if it's not present
                if translated_suffix not in translated_number:
                    translated_words.append(translated_number + translated_suffix)
                else:
                    translated_words.append(translated_number)
            else:
                translated_words.append(word)

        return ' '.join(translated_words)

    # Apply translation function to the 'text' column
    df['new_comment_feedback'] = df['new_comment_feedback'].apply(translate_numbers)
    df['new_event_contribution'] = df['new_event_contribution'].apply(translate_numbers)

    data['message'] = f"Translation of numbers into words completed."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    data['message'] = f"Removing emojis.."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    # We are using the emoji module to replace emoji with blanks
    df['new_comment_feedback'] = df['new_comment_feedback'].apply(lambda s: emoji.replace_emoji(s, ''))
    df['new_event_contribution'] = df['new_event_contribution'].apply(lambda s: emoji.replace_emoji(s, ''))

    # Transform casing in lower case
    df['new_comment_feedback'] = df['new_comment_feedback'].str.lower()
    df['new_event_contribution'] = df['new_event_contribution'].str.lower()

    data['message'] = f"Removing emojis completed."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    data['message'] = f"Removing Stopwords/Tokenization/Lemmatization.."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    # Get all the English stopwords
    stop_words = [
        'i','me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
    ]

    lemmatizer = WordNetLemmatizer()

    # Function to lemmatize text using Pattern
    tag_map = defaultdict(lambda : wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV

    def lemmatize_with_pattern(text):
        tokens = word_tokenize(text)  # Split text into tokens (assuming text is already preprocessed)
        tokens_tags = pos_tag(tokens)
        lemmatized_tokens = [lemmatizer.lemmatize(token, pos=tag_map[tag[0]]) for token, tag in tokens_tags if token not in stop_words]
        return ' '.join(lemmatized_tokens)

    # Apply lemmatization function to DataFrame columns
    df['new_comment_feedback'] = df['new_comment_feedback'].apply(lemmatize_with_pattern)
    df['new_event_contribution'] = df['new_event_contribution'].apply(lemmatize_with_pattern)

    data['message'] = f"Removing Stopwords/Tokenization/Lemmatization completed."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    data['message'] = f"Sentiment scoring.."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    # Define the custom lexicon map
    # Define the custom lexicon map
    # swotify_lexicon = {
    #     '': -1, 'able': 1, 'absent': -1, 'acad': 0, 'academic': 0, 'accommodate': 0, 'accomodate': 0, 'accompany': 0, 'accurately': 1, 'achieved': 1,
    #     'acquire': 0, 'act': 0, 'action': 0, 'actively': 1, 'activity': 0, 'actually': 0, 'additional': 0, 'additionally': 0, 'adjust': 0, 'adjusted': 0,
    #     'admit': 0, 'advice': 0, 'afterwards': 0, 'agenda': 0, 'agree': 1, 'ahead': 1, 'alex': 0, 'alleviate': 1, 'almost': 0, 'alone': -1, 'already': 0,
    #     'always': 0, 'amd': 0, 'among': 0, 'another': 0, 'answer': 0, 'anyway': 0, 'applicable': 0, 'appreciate': 0, 'area': 0, 'arnie': 0, 'aspire': 1,
    #     'assist': 0, 'attentive': 1, 'audience': 0, 'audio': 0, 'auditor': 0, 'authority': 0, 'available': 0, 'avoid': -1, 'awarding': 0, 'awful': -1,
    #     'awkwardly': -1, 'bad': -1, 'bare': 0, 'barely': 0, 'beautiful': 1, 'beautifully': 1, 'become': 0, 'beforehand': 0, 'believe': 1, 'best': 1,
    #     'beverage': 0, 'bhie': 0, 'big': 1, 'bit': 0, 'blame': -1, 'bombard': -1, 'brave': 1, 'break': 0, 'breakfast': 0, 'bring': 0, 'broad': 0,
    #     'broaden': 0, 'budgetary': 0, 'burst': 0, 'busy': 0, 'buy': 0, 'caf': 0, 'caller': 0, 'calm': 0, 'captivate': 1, 'care': 1, 'caril': 0, 'cause': 0,
    #     'ceremony': 0, 'cert': 0, 'cha': 0, 'chairperson': 0, 'challenge': 0, 'charge': 0, 'check': 0, 'cherry': 0, 'chill': 0, 'choose': 0, 'clearly': 0,
    #     'collaborate': 0, 'collaboration': 0, 'collaborative': 0, 'comfort': 1, 'coming': 0, 'commend': 1, 'comment': 0, 'committee': 0, 'committees': 0, 'comms': 0,
    #     'communicate': 0, 'communication': 1, 'companion': 0, 'compare': 0, 'complete': 0, 'completion': 0, 'compliance': 0, 'confidence': 1, 'confident': 1,
    #     'congrats': 1, 'congratulation': 1, 'congratulations': 1, 'consider': 0, 'consistent': 1, 'consult': 0, 'contact': 1, 'contestant': 1, 'continue': 1,
    #     'contribute': 1, 'contribution': 0, 'contributions': 1, 'control': 0, 'cooperate': 1, 'cooperation': 1, 'coordinate': 1, 'coordinated': 1, 'coordinating': 1,
    #     'courage': 1, 'course': 0, 'craft': 0, 'create': 0, 'creative': 1, 'creativity': 1, 'critic': 0, 'criticism': 0, 'cry': -1, 'cute': 1, 'cuteness': 1, 'dare': 0,
    #     'dark': -1, 'day': 0, 'deadline': 0, 'decide': 0, 'decision': 0, 'decisiveness': 1, 'dedication': 1, 'deeply': 0, 'delay': -1, 'delayed': -1, 'depend': 0,
    #     'deserb': 1, 'deserve': 1, 'design': 1, 'designing': 0, 'despite': 0, 'detail': 0, 'dig': 0, 'discover': 0, 'distribute': 0, 'dj': 0, 'djer': 0, 'do': 0,
    #     'documentation': 0, 'documents': 0, 'done': 0, 'drea': 0, 'due': 0, 'duty': 0, 'easy': 0, 'eat': 0, 'edit': 0, 'effective': 0, 'efficiently': 1, 'effort': 0,
    #     'elaborate': 0, 'embrace': 1, 'encode': 0, 'end': 0, 'endeavor': 0, 'energy': 1, 'ensure': 0, 'entertained': 1, 'entire': 0, 'equip': 0, 'equipment': 0,
    #     'error': 0, 'euni': 0, 'evaluation': 0, 'event': 0, 'ever': 0, 'every': 0, 'everyone': 0, 'everything': 0, 'everywhere': 0, 'expenses': 0, 'experience': 0,
    #     'experienced': 0, 'external': 0, 'face': 0, 'feel': 0, 'feeling': 0, 'figure': 0, 'fine': 0, 'finish': 1, 'flexibility': 1, 'flexible': 1, 'flow': 0, 'food': 0,
    #     'forget': 0, 'former': 0, 'forms': 0, 'free': 0, 'frequently': 0, 'friend': 0, 'fulfill': 1, 'full': 0, 'functional': 1, 'further': 0, 'future': 0, 'gain': 0,
    #     'gap': 0, 'get': 0, 'give': 0, 'gives': 0, 'good': 1, 'graduate': 1, 'graduation': 1, 'great': 1, 'greatest': 1, 'group': 0, 'growth': 1, 'guest': 0, 'guide': 1,
    #     'hand': 0, 'handled': 1, 'handling': 1, 'hans': 0, 'happen': 0, 'hard': 1, 'hardworking': 1, 'health': 0, 'hear': 0, 'help': 1, 'helped': 1, 'helpful': 1,
    #     'helping': 1, 'helps': 1, 'hesitate': -1, 'high': 1, 'home': 0, 'honest': 1, 'honestly': 1, 'hope': 0, 'horizon': 0, 'host': 1, 'hosting': 0, 'however': 0,
    #     'hungry': 0, 'hydrated': 0, 'immediate': 0, 'immediately': 0, 'impact': 0, 'impossible': 0, 'improve': 0, 'improvement': 1, 'incompetent': -1, 'incredible': 1, 'inform': 0,
    #     'infrequent': -1, 'initiative': 0, 'inspiration': 1, 'instance': 0, 'intermission': 0, 'internal': 0, 'internally': 0, 'intrusive': -1, 'issue': -1, 'item': 0,
    #     'jfinex': 0, 'job': 1, 'jolo': 0, 'jt': 0, 'judge': 0, 'justice': 0, 'kai': 0, 'karil': 0, 'keep': 1, 'kudos': 1, 'label': 0, 'lack': -1, 'lakambini': 0, 'lakan': 0,
    #     'lapel': 0, 'lead': 0, 'leader': 0, 'leadership': 1, 'leading': 0, 'learn': 0, 'legal': 0, 'legit': 1, 'life': 0, 'limit': -1, 'limited': -1, 'listen': 1, 'listener': 1,
    #     'literally': 0, 'lively': 1, 'logistics': 0, 'long': 0, 'lose': -1, 'love': 1, 'lovely': 0, 'maine': 0, 'major': 0, 'man': 0, 'manage': 1, 'maneuver': 0,
    #     'manpower': 0, 'matter': 0, 'may': 0, 'maybe': 0, 'medal': 0, 'member': 0, 'message': 0, 'minded': 0, 'minimize': 0, 'minimum': 0, 'mira': 0, 'miscommunication': -1,
    #     'misguided': -1, 'moment': 0, 'money': 0, 'moreover': 0, 'morning': 0, 'mostly': 0, 'much': 1, 'multi': 0, 'music': 0, 'name': 0, 'natural': 1, 'necessary': 0,
    #     'need': 0, 'negative': -1, 'neglect': -1, 'neutral': 0, 'neutralize': 0, 'never': -1, 'new': 0, 'nicely': 1, 'nothing': -1, 'notice': 0, 'nowhere': -1,
    #     'obedient': 1, 'observant': 0, 'observe': 0, 'occur': 0, 'often': 0, 'okay': 0, 'online': 0, 'open': 0, 'operation': 0, 'opinion': 0, 'opportunity': 1, 'order': 0,
    #     'org': 0, 'organization': 0, 'organize': 1, 'organized': 1, 'orgs': 0, 'orient': 0, 'oriented': 1, 'outside': 0, 'overlap': -1, 'oversee': -1, 'paper': 0,
    #     'paperwork': 0, 'parent': 0, 'participant': 0, 'participants': 0, 'particularly': 0, 'passion': 1, 'passionate': 1, 'patience': 0, 'patient': 0, 'perfect': 1,
    #     'performance': 0, 'performer': 0, 'perseverance': 1, 'photography': 0, 'pic': 0, 'place': 0, 'plan': 0, 'position': 0, 'positive': 1, 'possess': 0, 'possibility': 1,
    #     'possible': 1, 'posting': 0, 'potential': 1, 'practice': 0, 'pre': 0, 'prefer': 0, 'prepare': 1, 'pres': 0, 'presence': 0, 'president': 0, 'pressure': -1,
    #     'pressured': -1, 'prevent': 0, 'printer': 0, 'prior': 0, 'prioritize': 0, 'privilege': 0, 'pro': 0, 'proactively': 0, 'problem': 0, 'process': 0,
    #     'profession': 0, 'procurement': 0, 'professional': 1, 'professionally': 1, 'progress': 1, 'prompt': 0, 'promptly': 0, 'proper': 0, 'properly': 0, 'proposal': 0,
    #     'protect': 0, 'proud': 1, 'provide': 1, 'publication': 0, 'put': 0, 'queen': 1, 'quick': 0, 'radiate': 0, 'react': 0, 'real': 0, 'really': 0, 'reason': 0,
    #     'receipt': 0, 'recommendation': 0, 'relate': 0, 'related': 0, 'relations': 0, 'relationship': 0, 'release': 0, 'reliability': 1, 'reliable': 0, 'requests': 0,
    #     'require': 0, 'requirement': 0, 'resolution': 0, 'resource': 0, 'respect': 1, 'response': 0, 'responsibilities': 0, 'responsible': 1, 'responsiblity': 0, 'responsive': 1,
    #     'rest': 0, 'review': 0, 'rhode': 0, 'right': 0, 'run': 0, 'salute': 1, 'sap': 0, 'sash': 0, 'say': 0, 'school': 0, 'score': 0, 'second': 0, 'secretary': 0, 'secure': 0,
    #     'see': 0, 'seem': 0, 'self': 0, 'serve': 0, 'service': 1, 'shortcoming': -1, 'show': 0, 'shy': -1, 'sick': 0, 'sign': 0, 'signature': 0, 'significant': 0, 'siklabuhay': 0,
    #     'sinag': 0, 'since': 0, 'situation': 0, 'slay': 1, 'slaying': 1, 'smile': 1, 'smoother': 1, 'smoothly': 1, 'social': 0, 'special': 0, 'sponsor': 0, 'sponsorship': 0,
    #     'start': 0, 'stay': 0, 'stem': 0, 'step': 0, 'stick': 0, 'still': 0, 'stress': -1, 'stressed': -1, 'strict': -1, 'strong': 1, 'struggle': -1, 'student': 0, 'submit': 0,
    #     'success': 1, 'successful': 1, 'sudden': 0, 'sufficiently': 1, 'suggestion': 0, 'super': 1, 'supply': 0, 'support': 1, 'surprising': 1, 'surrounding': 0, 'tabulation': 0,
    #     'take': 0, 'tala': 0, 'talk': 0, 'tap': 0, 'task': 0, 'tasks': 0, 'team': 0, 'tear': 0, 'tech': 0, 'technician': 0, 'technology': 0, 'tell': 0, 'terrible': -1,
    #     'thank': 1, 'thankful': 1, 'theater': 0, 'therefore': 0, 'thing': 0, 'things': 0, 'though': 0, 'thought': 0, 'three': 0, 'thru': 0, 'time': 0, 'times': 0, 'tiredness': -1,
    #     'title': 0, 'told': 0, 'towards': 0, 'track': 0, 'trea': 0, 'treas': 0, 'treasurer': 0, 'trophy': 0, 'trunk': 0, 'try': 0, 'understand': 0, 'unexpected': 0, 'uni': 0,
    #     'unlock': 1, 'unwilling': -1, 'update': 1, 'upset': -1, 'useful': 1, 'vibe': 0, 'vice': 0, 'visit': 0, 'vp': 0, 'wait': 0, 'waste': -1, 'watch': 0, 'way': 0,
    #     'well': 1, 'whenever': 0, 'without': -1, 'witness': 0, 'work': 1, 'working': 1, 'world': 0, 'would': 0, 'yeah': 1, 'yes': 1, 'ysabel': 0, 'zone': 0, 'bits': 0, 'promotion': 1,
    #     'transparent': 0, 'workflow': 0, 'poor': -1, 'mediocre': 0, 'quality': 1,'generous': 1, 'cooperative': 0, 'tasking': 0, 'uncooperative': -1, 'backdrop': 0
    # }




    data['message'] = f"Sentiment scoring completed."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    


    df_tbl = df.head(2).to_html(index=False, max_cols=8, classes="table is-narrow")
    data['message'] = f"{df_tbl}"
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    data['message'] = "Training completed"
    yield f"event: mlfinish\ndata: {json.dumps(data)}\n\n"

