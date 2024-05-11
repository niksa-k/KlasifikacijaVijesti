import csv
import random

# Početni podaci
pocetni_podaci = [
    ["klub", "gol", "meč", "igrač", "predsednik", "parlament", "skupština", "vlada", "skandal", "nastup", "peva", "pesma"],
    [2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 8, 5, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 9, 6, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [11, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [5, 5, 5, 21, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 3, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0]
]
# Funkcija za generisanje dodatnih redova
def generisi_dodatne_redove(pocetni_podaci, ukupno_redova):
    rijeci = [
        ["klub", "gol", "meč", "igrač"],
        ["predsednik", "parlament", "skupština", "vlada"],
        ["skandal", "nastup", "peva", "pesma"]
    ]

    dodatni_redovi = []
    for _ in range(ukupno_redova):
        red = [0] * 13  # Dodajemo jednu kolonu za 'klasu'
        grupa_rijeci = random.choice(rijeci)

        for rijec in grupa_rijeci:
            if rijec not in pocetni_podaci[0]:
                continue

            index = pocetni_podaci[0].index(rijec)
            red[index] = random.randint(0, 10)

        # Određivanje klase
        if set(grupa_rijeci).issubset(pocetni_podaci[0][:4]):
            red[-1] = 1
        elif set(grupa_rijeci).issubset(pocetni_podaci[0][4:8]):
            red[-1] = 2
        elif set(grupa_rijeci).issubset(pocetni_podaci[0][8:]):
            red[-1] = 3

        dodatni_redovi.append(red)

    return dodatni_redovi

# Generisanje dodatnih 90 redova
dodatni_podaci = generisi_dodatne_redove(pocetni_podaci, 100)

# Spajanje dodatnih redova sa postojećim podacima
finalni_podaci = [pocetni_podaci[0] + ["klasa"]] + dodatni_podaci  # Dodavanje naslova kolona

# Ispis rezultujuće matrice u CSV fajl
csv_file = "generisaniPodaci.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    
    for red in finalni_podaci:
        writer.writerow(red)

print(f"Podaci su uspješno sačuvani u {csv_file}.")