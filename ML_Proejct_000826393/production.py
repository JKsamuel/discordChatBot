## Load docs and labels

filenames = ["amazon_cells_labelled.txt", "imdb_labelled.txt", "yelp_labelled.txt", "JongeunKim_custom_labelled.txt"]
docs = []
labels = []
for filename in filenames:
    with open("sentiment/"+filename) as file:
        for line in file:
            line = line.strip()
            labels.append(int(line[-1]))
            docs.append(line[:-2].strip())

## Vectorize
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(min_df=1, max_df=0.9)
vectors = vectorizer.fit_transform(docs)

## Train
from sklearn.neural_network import MLPClassifier
clf = MLPClassifier(activation="tanh", hidden_layer_sizes=(300, 550, 100))
clf.fit(vectors, labels)
print(clf.score(vectors, labels))

# Pickle
from joblib import dump

dump(clf, "sentiment_clf.joblib")
dump(vectorizer, "sentiment_vectorizer.joblib")


print("Has been pickled")




