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

# Metrics
from sklearn.metrics import (
    accuracy_score,
    recall_score,
    precision_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)


# from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk # General NLP tool
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize # For tokenization
from nltk.corpus import stopwords # For getting the stopwords
from nltk.corpus import wordnet as wn
from collections import defaultdict

nltk.download('wordnet')
nltk.download('stopwords')
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
    stop_words = stopwords.words('english')

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

    data['message'] = f"Getting the sentiment scores for each rows.."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    # Define the custom lexicon map
    swotify_lexicon = {
        '': -1, 'able': 1, 'absent': -1, 'acad': 0, 'academic': 0, 'accommodate': 0, 'accomodate': 0, 'accompany': 0, 'accurately': 1, 'achieved': 1,
        'acquire': 0, 'act': 0, 'action': 0, 'actively': 1, 'activity': 0, 'actually': 0, 'additional': 0, 'additionally': 0, 'adjust': 0, 'adjusted': 0,
        'admit': 0, 'advice': 0, 'afterwards': 0, 'agenda': 0, 'agree': 1, 'ahead': 1, 'alex': 0, 'alleviate': 1, 'almost': 0, 'alone': -1, 'already': 0,
        'always': 0, 'amd': 0, 'among': 0, 'another': 0, 'answer': 0, 'anyway': 0, 'applicable': 0, 'appreciate': 0, 'area': 0, 'arnie': 0, 'aspire': 1,
        'assist': 0, 'attentive': 1, 'audience': 0, 'audio': 0, 'auditor': 0, 'authority': 0, 'available': 0, 'avoid': -1, 'awarding': 0, 'awful': -1,
        'awkwardly': -1, 'bad': -1, 'bare': 0, 'barely': 0, 'beautiful': 1, 'beautifully': 1, 'become': 0, 'beforehand': 0, 'believe': 1, 'best': 1,
        'beverage': 0, 'bhie': 0, 'big': 1, 'bit': 0, 'blame': -1, 'bombard': -1, 'brave': 1, 'break': 0, 'breakfast': 0, 'bring': 0, 'broad': 0,
        'broaden': 0, 'budgetary': 0, 'burst': 0, 'busy': 0, 'buy': 0, 'caf': 0, 'caller': 0, 'calm': 0, 'captivate': 1, 'care': 1, 'caril': 0, 'cause': 0,
        'ceremony': 0, 'cert': 0, 'cha': 0, 'chairperson': 0, 'challenge': 0, 'charge': 0, 'check': 0, 'cherry': 0, 'chill': 0, 'choose': 0, 'clearly': 0,
        'collaborate': 0, 'collaboration': 0, 'collaborative': 0, 'comfort': 1, 'coming': 0, 'commend': 1, 'comment': 0, 'committee': 0, 'committees': 0, 'comms': 0,
        'communicate': 0, 'communication': 1, 'companion': 0, 'compare': 0, 'complete': 0, 'completion': 0, 'compliance': 0, 'confidence': 1, 'confident': 1,
        'congrats': 1, 'congratulation': 1, 'congratulations': 1, 'consider': 0, 'consistent': 1, 'consult': 0, 'contact': 1, 'contestant': 1, 'continue': 1,
        'contribute': 1, 'contribution': 0, 'contributions': 1, 'control': 0, 'cooperate': 1, 'cooperation': 1, 'coordinate': 1, 'coordinated': 1, 'coordinating': 1,
        'courage': 1, 'course': 0, 'craft': 0, 'create': 0, 'creative': 1, 'creativity': 1, 'critic': 0, 'criticism': 0, 'cry': -1, 'cute': 1, 'cuteness': 1, 'dare': 0,
        'dark': -1, 'day': 0, 'deadline': 0, 'decide': 0, 'decision': 0, 'decisiveness': 1, 'dedication': 1, 'deeply': 0, 'delay': -1, 'delayed': -1, 'depend': 0,
        'deserb': 1, 'deserve': 1, 'design': 1, 'designing': 0, 'despite': 0, 'detail': 0, 'dig': 0, 'discover': 0, 'distribute': 0, 'dj': 0, 'djer': 0, 'do': 0,
        'documentation': 0, 'documents': 0, 'done': 0, 'drea': 0, 'due': 0, 'duty': 0, 'easy': 0, 'eat': 0, 'edit': 0, 'effective': 0, 'efficiently': 1, 'effort': 0,
        'elaborate': 0, 'embrace': 1, 'encode': 0, 'end': 0, 'endeavor': 0, 'energy': 1, 'ensure': 0, 'entertained': 1, 'entire': 0, 'equip': 0, 'equipment': 0,
        'error': 0, 'euni': 0, 'evaluation': 0, 'event': 0, 'ever': 0, 'every': 0, 'everyone': 0, 'everything': 0, 'everywhere': 0, 'expenses': 0, 'experience': 0,
        'experienced': 0, 'external': 0, 'face': 0, 'feel': 0, 'feeling': 0, 'figure': 0, 'fine': 0, 'finish': 1, 'flexibility': 1, 'flexible': 1, 'flow': 0, 'food': 0,
        'forget': 0, 'former': 0, 'forms': 0, 'free': 0, 'frequently': 0, 'friend': 0, 'fulfill': 1, 'full': 0, 'functional': 1, 'further': 0, 'future': 0, 'gain': 0,
        'gap': 0, 'get': 0, 'give': 0, 'gives': 0, 'good': 1, 'graduate': 1, 'graduation': 1, 'great': 1, 'greatest': 1, 'group': 0, 'growth': 1, 'guest': 0, 'guide': 1,
        'hand': 0, 'handled': 1, 'handling': 1, 'hans': 0, 'happen': 0, 'hard': 1, 'hardworking': 1, 'health': 0, 'hear': 0, 'help': 1, 'helped': 1, 'helpful': 1,
        'helping': 1, 'helps': 1, 'hesitate': -1, 'high': 1, 'home': 0, 'honest': 1, 'honestly': 1, 'hope': 0, 'horizon': 0, 'host': 1, 'hosting': 0, 'however': 0,
        'hungry': 0, 'hydrated': 0, 'immediate': 0, 'immediately': 0, 'impact': 0, 'impossible': 0, 'improve': 0, 'improvement': 1, 'incompetent': -1, 'incredible': 1, 'inform': 0,
        'infrequent': -1, 'initiative': 0, 'inspiration': 1, 'instance': 0, 'intermission': 0, 'internal': 0, 'internally': 0, 'intrusive': -1, 'issue': -1, 'item': 0,
        'jfinex': 0, 'job': 1, 'jolo': 0, 'jt': 0, 'judge': 0, 'justice': 0, 'kai': 0, 'karil': 0, 'keep': 1, 'kudos': 1, 'label': 0, 'lack': -1, 'lakambini': 0, 'lakan': 0,
        'lapel': 0, 'lead': 0, 'leader': 0, 'leadership': 1, 'leading': 0, 'learn': 0, 'legal': 0, 'legit': 1, 'life': 0, 'limit': -1, 'limited': -1, 'listen': 1, 'listener': 1,
        'literally': 0, 'lively': 1, 'logistics': 0, 'long': 0, 'lose': -1, 'love': 1, 'lovely': 0, 'maine': 0, 'major': 0, 'man': 0, 'manage': 1, 'maneuver': 0,
        'manpower': 0, 'matter': 0, 'may': 0, 'maybe': 0, 'medal': 0, 'member': 0, 'message': 0, 'minded': 0, 'minimize': 0, 'minimum': 0, 'mira': 0, 'miscommunication': -1,
        'misguided': -1, 'moment': 0, 'money': 0, 'moreover': 0, 'morning': 0, 'mostly': 0, 'much': 1, 'multi': 0, 'music': 0, 'name': 0, 'natural': 1, 'necessary': 0,
        'need': 0, 'negative': -1, 'neglect': -1, 'neutral': 0, 'neutralize': 0, 'never': -1, 'new': 0, 'nicely': 1, 'nothing': -1, 'notice': 0, 'nowhere': -1,
        'obedient': 1, 'observant': 0, 'observe': 0, 'occur': 0, 'often': 0, 'okay': 0, 'online': 0, 'open': 0, 'operation': 0, 'opinion': 0, 'opportunity': 1, 'order': 0,
        'org': 0, 'organization': 0, 'organize': 1, 'organized': 1, 'orgs': 0, 'orient': 0, 'oriented': 1, 'outside': 0, 'overlap': -1, 'oversee': -1, 'paper': 0,
        'paperwork': 0, 'parent': 0, 'participant': 0, 'participants': 0, 'particularly': 0, 'passion': 1, 'passionate': 1, 'patience': 0, 'patient': 0, 'perfect': 1,
        'performance': 0, 'performer': 0, 'perseverance': 1, 'photography': 0, 'pic': 0, 'place': 0, 'plan': 0, 'position': 0, 'positive': 1, 'possess': 0, 'possibility': 1,
        'possible': 1, 'posting': 0, 'potential': 1, 'practice': 0, 'pre': 0, 'prefer': 0, 'prepare': 1, 'pres': 0, 'presence': 0, 'president': 0, 'pressure': -1,
        'pressured': -1, 'prevent': 0, 'printer': 0, 'prior': 0, 'prioritize': 0, 'privilege': 0, 'pro': 0, 'proactively': 0, 'problem': 0, 'process': 0,
        'profession': 0, 'procurement': 0, 'professional': 1, 'professionally': 1, 'progress': 1, 'prompt': 0, 'promptly': 0, 'proper': 0, 'properly': 0, 'proposal': 0,
        'protect': 0, 'proud': 1, 'provide': 1, 'publication': 0, 'put': 0, 'queen': 1, 'quick': 0, 'radiate': 0, 'react': 0, 'real': 0, 'really': 0, 'reason': 0,
        'receipt': 0, 'recommendation': 0, 'relate': 0, 'related': 0, 'relations': 0, 'relationship': 0, 'release': 0, 'reliability': 1, 'reliable': 0, 'requests': 0,
        'require': 0, 'requirement': 0, 'resolution': 0, 'resource': 0, 'respect': 1, 'response': 0, 'responsibilities': 0, 'responsible': 1, 'responsiblity': 0, 'responsive': 1,
        'rest': 0, 'review': 0, 'rhode': 0, 'right': 0, 'run': 0, 'salute': 1, 'sap': 0, 'sash': 0, 'say': 0, 'school': 0, 'score': 0, 'second': 0, 'secretary': 0, 'secure': 0,
        'see': 0, 'seem': 0, 'self': 0, 'serve': 0, 'service': 1, 'shortcoming': -1, 'show': 0, 'shy': -1, 'sick': 0, 'sign': 0, 'signature': 0, 'significant': 0, 'siklabuhay': 0,
        'sinag': 0, 'since': 0, 'situation': 0, 'slay': 1, 'slaying': 1, 'smile': 1, 'smoother': 1, 'smoothly': 1, 'social': 0, 'special': 0, 'sponsor': 0, 'sponsorship': 0,
        'start': 0, 'stay': 0, 'stem': 0, 'step': 0, 'stick': 0, 'still': 0, 'stress': -1, 'stressed': -1, 'strict': -1, 'strong': 1, 'struggle': -1, 'student': 0, 'submit': 0,
        'success': 1, 'successful': 1, 'sudden': 0, 'sufficiently': 1, 'suggestion': 0, 'super': 1, 'supply': 0, 'support': 1, 'surprising': 1, 'surrounding': 0, 'tabulation': 0,
        'take': 0, 'tala': 0, 'talk': 0, 'tap': 0, 'task': 0, 'tasks': 0, 'team': 0, 'tear': 0, 'tech': 0, 'technician': 0, 'technology': 0, 'tell': 0, 'terrible': -1,
        'thank': 1, 'thankful': 1, 'theater': 0, 'therefore': 0, 'thing': 0, 'things': 0, 'though': 0, 'thought': 0, 'three': 0, 'thru': 0, 'time': 0, 'times': 0, 'tiredness': -1,
        'title': 0, 'told': 0, 'towards': 0, 'track': 0, 'trea': 0, 'treas': 0, 'treasurer': 0, 'trophy': 0, 'trunk': 0, 'try': 0, 'understand': 0, 'unexpected': 0, 'uni': 0,
        'unlock': 1, 'unwilling': -1, 'update': 1, 'upset': -1, 'useful': 1, 'vibe': 0, 'vice': 0, 'visit': 0, 'vp': 0, 'wait': 0, 'waste': -1, 'watch': 0, 'way': 0,
        'well': 1, 'whenever': 0, 'without': -1, 'witness': 0, 'work': 1, 'working': 1, 'world': 0, 'would': 0, 'yeah': 1, 'yes': 1, 'ysabel': 0, 'zone': 0, 'bits': 0, 'promotion': 1,
        'transparent': 0, 'workflow': 0, 'poor': -1, 'mediocre': 0, 'quality': 1,'generous': 1, 'cooperative': 0, 'tasking': 0, 'uncooperative': -1, 'backdrop': 0
    }
    # Function to calculate polarity score based on custom lexicon map
    def custom_polarity_score(text):
        words = text.split()
        pos, neg, neu = 0, 0, 0
        for word in words:
            if word in swotify_lexicon:
                if swotify_lexicon[word] > 0:
                    pos += 1
                elif swotify_lexicon[word] < 0:
                    neg += 1
                else:
                    neu += 1
        total = pos + neg + neu
        if total == 0:
            return {"pos": 0, "neg": 0, "neu": 1, "compound": 0}
        return {
            "pos": pos / total,
            "neg": neg / total,
            "neu": neu / total,
            "compound": (pos - neg) / total
        }
    
    df.reset_index(inplace=True, drop=True)
    df['index'] = df.index

    # Run the polarity score on the entire dataset
    ec_res = {}
    cf_res = {}

    # Iterate every row, get all cleaned event_contribution and comment_feedback
    for i, row in df.iterrows():
        ec = row['new_event_contribution']
        cf = row['new_comment_feedback']
        myid = i

        # Save the polarity score in the dictionary identified with its index
        ec_res[myid] = custom_polarity_score(ec)
        cf_res[myid] = custom_polarity_score(cf)

    # Create a dataframe from the dictionary of polarity scores
    ec_sa_df = pd.DataFrame(ec_res).T
    cf_sa_df = pd.DataFrame(cf_res).T

    # Reset the index to get the index as a column in the polarity scores
    ec_sa_df = ec_sa_df.reset_index()
    cf_sa_df = cf_sa_df.reset_index()

    # Rename the columns to its specific column to prevent it from mixing with the other polarity scores dataframe
    ec_sa_df_col_names = {
        "neg" : "ec_neg",
        "neu" : "ec_neu",
        "pos" : "ec_pos",
        "compound" : "ec_compound",
    }
    cf_sa_df_col_names = {
        "neg" : "cf_neg",
        "neu" : "cf_neu",
        "pos" : "cf_pos",
        "compound" : "cf_compound",
    }

    # Replace the columns with the new column names
    ec_sa_df.rename(columns=ec_sa_df_col_names, inplace=True)
    cf_sa_df.rename(columns=cf_sa_df_col_names, inplace=True)

    # Merge the polarity scores data frame to the main dataframe so that we can see the sentiment scores with our data
    df = df.merge(ec_sa_df, how="right")
    df = df.merge(cf_sa_df, how="right")
    
    # Getting the final compound by averaging the ec_compound and cf_compound
    df['final_compound'] = (df['ec_compound'] + df['cf_compound']) / 2

    # determining the final sentiment classification based on the condition

    # Setting the positive sentiment and adding its textual value
    df.loc[df['final_compound'] > 0, 'sentiment_class'] = 1
    df.loc[df['final_compound'] > 0, 'sentiment'] = 'Positive'

    # Setting the negative sentiment
    df.loc[df['final_compound'] < 0, 'sentiment_class'] = 2
    df.loc[df['final_compound'] < 0, 'sentiment'] = 'Negative'

    # Setting the neutral sentiment
    df.loc[df['final_compound'] == 0, 'sentiment_class'] = 0
    df.loc[df['final_compound'] == 0, 'sentiment'] = 'Neutral'

    # Now sia_df contains the sentiment analysis results with customed swotify lexicon

    data['message'] = f"Sentiment scoring completed."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    data['message'] = f"Preparing for training... this might take a while"  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"
    
    data['message'] = f"Selected the needed columns for the training..."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    # Select the relevant columns for modeling
    needed_cols = [
        # 'position',
        'responsibility_rating',
        'team_communication_rating',
        'task_delegation_rating',
        'calmness_rating',
        'adaptability_rating',
        'attitude_rating',
        'comm_collab_rating',
        'external_resp_rating',

        'time_management_rating',
        'collab_rating',
        'flexible_rating',
        'accountability_rating',
        'sentiment_class',
        'sentiment'
    ]

    final_data = df[needed_cols]

    final_data = final_data.drop_duplicates()

    data['message'] = f"Selected the needed columns for the training... DONE"  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    data['message'] = f"Setting up scorer and evaluation functions..."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    # Create evaluation function for easier checking
    # Define a function that takes in arguments and prints out a classification report and confusion matrices
    def eval_classification(model, X_test, y_test, cmap=None,
                                normalize='true', classes=None, figsize=(5,3),
                                title="Confusion Matrix"):
        """Given a model, features, and labels, prints a classification report and
        confusion matrices"""

        test_preds = model.predict(X_test)
        return (classification_report(y_test, test_preds, target_names=classes))

    def evaluate_classification(y_true, y_predicted, average=None):
        accuracy = accuracy_score(y_true, y_predicted, normalize=True)
        recall = recall_score(y_true, y_predicted, average=average)
        precision = precision_score(y_true, y_predicted, average=average)
        f1 = f1_score(y_true, y_predicted, average=average)

        return accuracy, recall, precision, f1

    data['message'] = f"Setting up scorer and evaluation functions... DONE"  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    data['message'] = f"Splitting the data into train and test dataset..."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    # Identify features
    X = final_data.drop(columns=['sentiment_class', 'sentiment'])

    # Identify target
    y = final_data['sentiment_class']

    # Splitting the data into training and testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, stratify=y)

    data['message'] = f"Splitting the data into train and test dataset... DONE"  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"
    
    data['message'] = f"Train Dataset: {X_train.shape}  | Test Dataset: {X_test.shape}"  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"


    data['message'] = f"Setting up the machine learning pipeline..."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"
    # Creating the column selectors

    # Selecting only the numerical columns in the dataset
    numericals = X_train.select_dtypes(include='number')

    # Select all columns that are nominal in nature
    categoricals = X_train.select_dtypes(include='object')

    # Instantiating the imputers
    mean_imputer = SimpleImputer(strategy='mean')
    freq_imputer = SimpleImputer(strategy='most_frequent')

    # Fitting and transforming the numerical dataset

    # Create the standard scaler instance
    scaler = StandardScaler()

    # Fit the numerical columns
    scaler.fit(numericals)

    # Tranform to scaled dataset
    scaled_num_data = scaler.transform(numericals)

    num_pipeline = make_pipeline(mean_imputer, scaler)
    num_tuple = (num_pipeline, numericals.columns)
    transformer = make_column_transformer(num_tuple, remainder = 'passthrough')

    data['message'] = f"Setting up the machine learning pipeline...DONE"  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    data['message'] = f"Pipeline Configuration: {transformer}"  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    data['message'] = f"Data Modelling Started..."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    # List of models to be implemented
    models = {
        'KNeighborsClassifier': KNeighborsClassifier(),
        'RandomForestClassifier': RandomForestClassifier(random_state=42),
        'SVC': SVC(random_state=42),
        'XGBClassifier': XGBClassifier(random_state=42),
        'LogisticRegression': LogisticRegression(random_state=42)
    }


    data['message'] = f"Models to be executed: {models.keys()}"  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    metrics_list = []
    model_container = {}

    # Initial modeling with default parameters
    for i, (m, model) in enumerate(models.items()):
        # Create the pipeline from transforming to the selected model

        data['message'] = f"Training data for {m} ongoing..."  
        yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

        model_pipe = make_pipeline(transformer, model)

        data['message'] = f"Fitting data for {m}"  
        yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"
        # Fit the training data to the pipe
        model_pipe.fit(X_train, y_train)

        # Predict the value
        train_pred = model_pipe.predict(X_train)
        test_pred = model_pipe.predict(X_test)

        model_container[m] = model_pipe

        data['message'] = f"Scoring initial trained model {m}"  
        yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"
        # Evaluate the classification of the train and test data to the prediction
        train_accuracy, train_recall, train_precision, train_f1 = evaluate_classification(y_train, train_pred, average='weighted')
        test_accuracy, test_recall, test_precision, test_f1 = evaluate_classification(y_test, test_pred, average='weighted')

        # Save the details in the row
        row = {
            'Model Used': m,
            'Training Accuracy': train_accuracy,
            'Training Recall': train_recall,
            'Training Precision': train_precision,
            'Training F1 score': train_f1,
            'Testing Accuracy': test_accuracy,
            'Testing Recall': test_recall,
            'Testing Precision': test_precision,
            'Testing F1 score': test_f1,
            }
        metrics_list.append(row)

        data['message'] = f"Training data for {m} ongoing... COMPLETED"  
        yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"
    
    
    data['message'] = f"Intial Model Performance:"  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    df_tbl = pd.DataFrame(metrics_list).to_html(index=False, classes="table is-narrow")
    data['message'] = f"{df_tbl}"
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"


    data['message'] = f"Executing model tuning using the Hyperparameters ..."  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"
    
    # Setting all the parameters for tuning all of the models

    knn_param_grid = {
        'kneighborsclassifier__n_neighbors': range(1,100),
        'kneighborsclassifier__leaf_size': range(1,30),
    }

    rfc_param_grid = {
        'randomforestclassifier__n_estimators': range(10, 110, 10),
        'randomforestclassifier__max_depth' : range(1,10),
    }

    svc_param_grid = {
        'svc__C': [0.1, 1, 10, 100, 1000],
        'svc__kernel': ['rbf','linear'],
    }

    lr_param_grid = {
        'logisticregression__C': [0.1, 1, 10, 100, 1000],
        'logisticregression__solver': ['lbfgs', 'liblinear'],
    }

    xgbc_param_grid = {
        'xgbclassifier__n_estimators': range(10, 110, 10),
        'xgbclassifier__max_depth': range(1,10),
    }


    # Consolidating the parameter list
    params = {
        'KNeighborsClassifier': knn_param_grid,
        'RandomForestClassifier': rfc_param_grid,
        'SVC': svc_param_grid,
        'LogisticRegression': lr_param_grid,
        'XGBClassifier': xgbc_param_grid,
    }

    
    # Initiate metrics list for output
    tuned_metrics_list = []

    # Hold the tuned models
    best_model_container = {}
    # Initial modeling with default parameters
    for i, (m, model) in enumerate(models.items()):
        # Create the pipeline from transforming to the selected model
        model_pipe = make_pipeline(transformer, model)
        
        data['message'] = f"Tuning model for {m} ongoing..."  
        yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"
        
        data['message'] = f"Hyperparameter used for {m}: {str(params[m])}"  
        yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"
        
        data['message'] = f"Hyperparameter used for {m}: Cross Validation = 3 | Scoring = Weighted F1"  
        yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

        # We are going to get the best estimator based on accuracy
        grid = GridSearchCV(model_pipe, params[m], scoring = 'f1_weighted', cv=3, n_jobs=-1, verbose=True)


        data['message'] = f"Grid fitting for tuning {m} ongoing..."  
        yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"
        # Fit the training data to the pipe
        grid.fit(X_train, y_train)

        # Get the best model
        best_model = grid.best_estimator_

        # Store tuned models for future use
        best_model_container[m] = best_model

        # Predict the value
        train_pred = best_model.predict(X_train)
        test_pred = best_model.predict(X_test)

        # Evaluate the classification of the train and test data to the prediction
        train_accuracy, train_recall, train_precision, train_f1 = evaluate_classification(y_train, train_pred, average='weighted')
        test_accuracy, test_recall, test_precision, test_f1 = evaluate_classification(y_test, test_pred, average='weighted')

        # Save the details in the row
        row = {
            'Model Used': m,
            'Training Accuracy': train_accuracy,
            'Training Recall': train_recall,
            'Training Precision': train_precision,
            'Training F1 score': train_f1,

            'Testing Accuracy': test_accuracy,
            'Testing Recall': test_recall,
            'Testing Precision': test_precision,
            'Testing F1 score': test_f1,

            'Hyperparameters': str(grid.best_params_)
            }
        tuned_metrics_list.append(row)
        
        data['message'] = f"Tuning model for {m} ongoing... COMPLETED"  
        yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"
    
    data['message'] = f"Tuned Model Performance:"  
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    df_tbl = pd.DataFrame(tuned_metrics_list).to_html(index=False, classes="table is-narrow")
    data['message'] = f"{df_tbl}"
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    df_tbl = df.head(2).to_html(index=False, max_cols=8, classes="table is-narrow")
    data['message'] = f"{df_tbl}"
    yield f"event: mlstep\ndata: {json.dumps(data)}\n\n"

    data['message'] = "Training completed"
    yield f"event: mlfinish\ndata: {json.dumps(data)}\n\n"

