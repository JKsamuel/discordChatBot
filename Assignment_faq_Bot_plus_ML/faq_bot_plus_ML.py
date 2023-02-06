"""
Jongeun Kim, 000826393, Mohawk College, 19/Oct/2022

"""
import spacy
import regex as re
from spacy.matcher import Matcher
from faq_support_method import *

## Load the questions, responses, reegular expression
intents = file_loader("questions.txt")
responses = file_loader("answers.txt")
regexP = file_loader("regex.txt")


# create English pipeline object based on the en_core_web_sm
nlp = spacy.load("en_core_web_sm")
# create a Matcher instance
global matcher
matcher = Matcher(nlp.vocab)

# create a list of words (classified the speeach of act of the utterance)
sort_climbing_adj_n = ["chalk", "competition", "free", "ice", "indoor", "ladder", "definition",
                        "pole", "rock", "sport", "top", "tower", "olympic", "olympics","kinds","types"]
sort_climbing_n = ["climbing", "bouldering", "buildering", "canyoneering","lumberjack", 
                    "mallakhamba","mountaineering", "olympic", "olympics", 
                    "sport", "roping","gear","equipment", "gears", "equipments", "event"]
greeting_word = ["hello", "hi", "good", "hey", "buddy", "mate"]
greeting_time = ["morning", "afternoon", "evening"]
farewell_word = ["bye", "day", "one", "quit", "goodbye"]
appreciation = ["thanks", "thx", "appreciate","tx"]

# pattern for question
pattern = [
    {"POS": {"IN": ["ADP", "PRON","VERB"]}, "OP": "?"},
    {"POS": {"IN": ["VERB", "AUX"]}, "OP": "?"},
    {"LOWER": {"IN": sort_climbing_adj_n}, "OP": "?"},
    {"LOWER": "of", "OP":"?"},
    {"LOWER": {"IN": sort_climbing_n}, "OP": "+"}
]
matcher.add("basicQuestion", [pattern])

# pattern for farewell
farewellPattern = [
    {"POS": "VERB", "OP": "?"},
    {"POS": "DET", "OP": "?"},
    {"POS": "ADJ", "OP":"?"},
    {"LOWER": {"IN": farewell_word}, "OP": "*"}
]
matcher.add("farewell", [farewellPattern])

# pattern for greeting
greetPattern = [
    {"LOWER": {"IN": greeting_word}, "OP": "*"},
    {"LOWER": {"IN": greeting_time}, "OP": "?"}
]
matcher.add("greeting", [greetPattern])

# pattern for appreciation
appreciationPattern = [
    {"TEXT": {"REGEX": "[Tt](hanks){e<=1,d<=1}"}, "OP": "*"},
    {"LOWER": {"IN": appreciation}, "OP": "*"}
]
matcher.add("appreciation", [appreciationPattern])

# pattern for asking
# Example: "Do you want to see a movie tonight?"
asking = [
    {"POS": {"IN": ["VERB", "AUX"]}, "OP": "+"},
    {"POS": {"IN": ["NOUN", "PRON"]}, "OP": "?"},
    {"POS": "VERB", "OP": "?"},
    {"POS": "PART", "OP": "?"},
    {"POS": "VERB", "OP": "?"},
    {"POS": "DET", "OP": "?"},
    {"POS": {"IN": ["NOUN", "PRON"]}, "OP": "+"},
    {"POS": "PUNCT", "OP":"?"}
]
matcher.add("asking", [asking])

# pattern for command
command = [
    {"LOWER": {"IN": ["ping", "roll"]}, "OP":"+"}
]
matcher.add("command", [command])

agree = [
    {"LOWER": {"IN": ["ok", "sure", "do", "course","yes","love","like","want"]}, "OP":"+"}
]
matcher.add("agree", [agree])

def generate(intent):
    """
    This function returns an appropriate response given a user's
    intent.
    """
    import openai
    openai.api_key = "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"     
    
    if intent == -2:
        responding = openai.Completion.create(engine="text-davinci-003", prompt=userAsking, max_tokens=64, temperature=0.7)
        print("Bot: ", (responding["choices"][0]["text"]).strip())
        return responding["choices"][0]["text"]
    
    global responses # declare that we will use a global variable
       
    return responses[intent]


def understand(utterance):
    """This function returns an index number of regex
    Args:
        utterance (string): user's utternace
    Returns:
        integer : index from answers text file
    """
    global userAsking
    userAsking = utterance
    
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.feature_extraction.text import TfidfVectorizer    
    ## Create a CountVectorizer and TF-IDF vectorizer objects for vectorizing
    vectorizer = CountVectorizer(min_df=1, max_df=0.9)
    vectorizer_tfidf = TfidfVectorizer()
    
    ## Create a vocabulary and a set of document vectors from the array of documents for training
    vectors = vectorizer.fit_transform(intents)    
    vectors_tfidf = vectorizer_tfidf.fit_transform(intents)
    
    ## Create a vocabulary and a set of document vectors from user's utterance for testing
    new_vector = vectorizer.transform([utterance])
    new_tfidf = vectorizer_tfidf.transform([utterance])
    
    ## for calculate a frequency of vectorized words.    
    sorted_words = sorted(vectorizer_tfidf.vocabulary_)
    questions_tfidf = vectors_tfidf.toarray();
    new_tfidf_words = new_tfidf.toarray()
    print(utterance)
    for i in range(len(questions_tfidf)):
        print(intents[i])
        for j in range(len(questions_tfidf[i])):
            if(questions_tfidf[i][j] > 0):
                print("    "+str(sorted_words[j])+":", round(questions_tfidf[i][j]* 100, 2),"%", end="  ")
        print("\n")
    print("\n")
    
    # the rate of matching words in user's utterance.
    print("TF-IDF (User's utterance)")
    for i in range(len(new_tfidf_words[0])):
        if(new_tfidf_words[0][i] > 0):
            print(str(sorted_words[i])+": ", round(new_tfidf_words[0][i]*100, 2),"%", end="   ")
    print("\n")      
    
    
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.metrics.pairwise import euclidean_distances
    ## Using Euclidean distance
    #similarities_tfidf = euclidean_distances(vectors_tfidf, new_tfidf)[0]
    similarities_tfidf = cosine_similarity(vectors_tfidf, new_tfidf)[0]
    tfidf_distance = 0    
    for i in range(len(similarities_tfidf)):
        # Find the shortest distance
        if similarities_tfidf[i] > similarities_tfidf[tfidf_distance]:
            tfidf_distance = i
    print("Result with TF-IDF: ", intents[tfidf_distance], "Similarity: " + str(round(similarities_tfidf[tfidf_distance]*100, 2)) + "%")
    # for i in range(len(similarities_tfidf)):
    #     # Find the shortest distance
    #     if similarities_tfidf[i] == similarities_tfidf.min():
    #         tfidf_distance = i
    # print("Result with TF-IDF: ", intents[tfidf_distance], "Euclidean distances : " + str(round(similarities_tfidf.min()*100, 2)))
    
    ## Using Cosine similarity
    similarities = cosine_similarity(new_vector, vectors)[0]
    index = 0
    for i in range(len(similarities)):
        if similarities[i] > similarities[index]:
            index = i
    print("Result with count vector: ",intents[index], "Similarity: " + str(round(similarities[index]*100, 2)) + "%")
    print("Index: ", index)    
    
    # The result of cosine similarity
    rate_similarity = similarities[index]
    print("Rate of similarity: ",rate_similarity)  
    # If the similarity is over 85% then the bot will find an answer from the array of responses
    tValue = 0.85
    
    from joblib import load    
    try:               
        # If the similarity is less than 85% then openAI api is called
        if rate_similarity < tValue:
            print("Similarity is less than 85%,and Euclidean distance is too high. The bot will call openAI api")
            # Load the object of classifier
            clf_joblib = load("sentiment_clf.joblib")
            # Load the object of vectorizer
            vectorizer_joblib = load("sentiment_vectorizer.joblib")
            
            vector = vectorizer_joblib.transform([utterance])
            prediction = clf_joblib.predict(vector)
            if prediction[0] == 1:
                print("Sentiment: Positive")
                return -2
            else:
                print("Sentiment: Negative")
                return -2
        else:
            return index
    except:
        pass      

def matcherMedia(utterance):
    """Using spaCy, this function will find matching user's intetns with pattern set
    Args:
        utterance (string): user's utterance
    Returns:
        integer : index number of responses
    """
    
    try:
        # data type of matchInfo variable is tuple and
        # it contain token.text and token.id
        # matchInfo contains user's intention
        matchInfo = pick_match_words(nlp, matcher, utterance)
        word = matchInfo[0]         # token.text
        print("word: "+ word.text)
        print("intent_ID: "+ nlp.vocab.strings[matchInfo[1]])
        
        for q in intents:
            # intentMatchInfo contains matching information with quesitons file.
            intentMatchInfo = pick_match_words(nlp, matcher, q)
            word_question = intentMatchInfo[0]
            # Ensure that there are words that match the user's intended words and patter I set.
            if word.text.lower() == word_question.text.lower():
                if nlp.vocab.strings[intentMatchInfo[1]] =="command" and word_question.text == "ping":
                    return 24
                elif nlp.vocab.strings[intentMatchInfo[1]] =="command" and word_question.text == "roll":
                    return 25
                else:
                    index = intents.index(q)
                    result = int(index / 2)
                    return result
            elif word.text == "climbing equipment" or word.text == "equipment" or word.text == "equipments" or word.text == "climbing equipments" or word.text == "gears" or word.text == "climbing gears" or  word.text == "climbing gear" or word.text =="gear":
                return 20
            elif nlp.vocab.strings[matchInfo[1]] == "greeting":
                return 21
            elif nlp.vocab.strings[matchInfo[1]] == "appreciation":
                return 22
            elif nlp.vocab.strings[matchInfo[1]] == "farewell":
                return 23
        
    except IndexError:
        return -1

def chat(utterance):
    asked = pick_match_words(nlp, matcher, utterance)
    sentence = asked[0]
    if nlp.vocab.strings[asked[1]] == "asking":
        answer = flexiable_answer(nlp, matcher, utterance)
        print(answer)
    return answer