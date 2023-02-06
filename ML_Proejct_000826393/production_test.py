from joblib import load
clf = load('sentiment_clf.joblib')
vectorizer = load('sentiment_vectorizer.joblib')

while True:
    utterance = input(">>> ")
    vector = vectorizer.transform([utterance])
    prediction = clf.predict(vector)
    if prediction[0] == 1:
        print("Positive")
    else:
        print("Negative")
