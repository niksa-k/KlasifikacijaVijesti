import random
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

file_path = r"C:\Niksa\Faks\Strukture_podataka_i_algoritmi\SPA_projekat\generisaniPodaci.csv"
data = pd.read_csv(file_path, sep=',')
print(data.head())

# Zamijeniti nebrojevne vrijednosti sa NaN
data = data.apply(pd.to_numeric, errors='coerce')

# Izbaciti redove koji sadrže NaN vrijednosti
data = data.dropna()

print("******************************************************************************************************\n" 
      + "    klasa" )
print(data['klasa'])

# Miješanje skupa podataka
random.seed(10)
promijesani_podaci = data.sample(frac=1, random_state=10)
# Dijeljenje podataka na trening i test skupove (80% trening, 20% test)
split_index = int(len(promijesani_podaci) * 0.8)
train_data = promijesani_podaci.iloc[:split_index]
test_data = promijesani_podaci.iloc[split_index:]

# Priprema podataka za trening i testiranje
studyX = train_data.drop('klasa', axis=1)
testX = test_data.drop('klasa', axis=1)
studyY = train_data['klasa']
testY = test_data['klasa']
print(testY)

# Računanje euklidskog rastojanja između dvije instance (najbliže rastojanje između dvije instance)
def euclid(prvaInst, drugaInst):
    # Provjera da li su instance stringovi, ako jesu, ignoriši ih (Lorem ipsum scenario)
    if isinstance(prvaInst, str) or isinstance(drugaInst, str):
        return None
    rastojanje = np.sqrt(np.sum(np.square(np.subtract(prvaInst, drugaInst))))
    return rastojanje

# Implementacija algoritma k najbližih susjeda
def kNN(studyX, testX, studyY, k):
    studyX = studyX.apply(pd.to_numeric)
    testX = testX.apply(pd.to_numeric)

    pogadjanja = []
    for test_pt in testX.to_numpy():
        dists = []
        for study_pt, study_label in zip(studyX.to_numpy(), studyY):
            difference = euclid(study_pt, test_pt)
            dists.append((difference, study_label))
        dists.sort(key=lambda x: x[0])
        closestK = dists[:k]
        predictions = [label for _, label in closestK]
        prediction = predict(predictions)
        pogadjanja.append(prediction)

    print("Pogadjanja:")
    print(pogadjanja)
    return pogadjanja

# Na osnovu liste najbližih susjeda, funkcija predvidja klasu izborom klase sa najvećim brojem ponavljanja
def predict(najblizi):
    countClass = {}

    for outcome in najblizi:
        if outcome in countClass:
            countClass[outcome] += 1
        else:
            countClass[outcome] = 1

    prediction = max(countClass, key=countClass.get)
    return prediction

# Evaluacija i ispis rezultata
for k_value in range(3, 9):
    print(f"K = {k_value}:")
    # Pravimo predvidjanja
    pogadjanja = kNN(studyX, testX, studyY, k=k_value)
    # Tačnost -> tačnost klasifikacije
    accuracy = accuracy_score(testY, pogadjanja)
    print(f"Tačnost za {k_value} najbljižih susjeda: {accuracy}")
    rnpRes = classification_report(testY, pogadjanja)
    print("Preciznost i odziv:\n" + str(rnpRes))
    print("-" * 100)

print("\nDolazimo do zakljucka da je 5 najoptimalniji broj susjeda. \nSusjedi oko 5 takodje mogu uci u obzir, dok, sto idemo dalje od optimalnog broja, tacnost je losija.\n")


# precision -> tačnost pogadjanja za odredjenu klasu
#              (od svih klasa za koje je dao predikciju da su ta klasa, npr. 60% je bilo ta klasa)
# recall -> postotak tacno pogodjenih instanci u odnosu na ukupan broj tacnih instanci
#           (od svih test klasa koje su u csv-u bile klasifikovane kao sport je zapravo pogodio npr. 75% njih, 
#            25% sport klase nije pogodio)
# f1-score -> harmonijska sredina precision-a i recall-a ==> 2*[(precision * recall)/(precision + recall)]
# support -> podjela izmedju 20 test instanci
# macro avg -> aritmetička sredina vrijednosti metrika za svaku klasu(svaka klasa ima jednak uticaj, 
#              bez obzira na broj instanci u toj klasi)
# weighted avg -> uzima prosječnu vrijednost metrika, s tim da svaka klasa dobija težinsku vrijednost proporcionalnu
#                 broju instanci u toj klasi, npr. weighted avg za preciznost
#                 ==> [4*0.6 + 14*0.91 + 2*0.5]/20 = 0.81 

