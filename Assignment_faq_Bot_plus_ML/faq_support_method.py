"""
Jongeun Kim, 000826393, Mohawk College, 19/Oct/2022

"""

import spacy
import regex as re
from spacy.matcher import Matcher

# File Loader
def file_loader(filename):
    """_summary_
    Loads each line of the file onto a list and returns it.
    Args:
        filename (string): a path of file 

    Returns:
        a list 
    """
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip())
    return lines


# using pattern matcher
def pick_match_words(nlp, matcher, utterance):
    """_summary_

    Args:
        nlp (_type_): an Object of English pipeline
        matcher (_type_): an instance of Matcher class
        utterance (_type_): intent or questions

    Returns:
        Tuple : (token.text, token.id)
    """
    try:
        user_intent = nlp(utterance)
        matches = matcher(user_intent)
        # an object of comparison for figuring out the length of token
        # longest token length I will use it.
        doc = matches[0]
        locations=[]
        
        # Find longest token length
        for match in matches:
            locations.append(user_intent[match[1]:match[2]])
            if match[2] - match[1] > doc[2] - doc[1]:
                doc = match
        
        dic = (user_intent[doc[1]:doc[2]], doc[0])
        return dic
    except:
        return -1
    
def flexiable_answer(nlp, matcher, utterance):
    try:
        doc = nlp(utterance)
        matches = matcher(doc)
        for match_id, start, end in matches:
            if nlp.vocab.strings[match_id] == "asking":
                answer = "I am not sure, but what " + doc[start+6].text.lower() + " " + doc[start:start+5].text.lower()
                print(answer)
                break
        return answer
    except IndexError:
        return -1