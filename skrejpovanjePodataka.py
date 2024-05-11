import requests
from bs4 import BeautifulSoup
import csv
from collections import Counter
import stanza

# Reči koje želite da prebrojite (ključne reči u zaglavlju CSV fajla)
kljucne_rijeci = [
    "klub", "gol", "meč", "igrač", "predsednik",
    "parlament", "skupština", "vlada", "skandal",
    "nastup", "peva", "pesma"
]

# Preuzimanje srpskog modela za Stanza alat
stanza.download("sr")

# Učitavanje srpskog modela(Natural Language Processing)
nlp = stanza.Pipeline("sr")

# Lista URL-ova koji se skrejpuju
urls = [
    "https://sportal.blic.rs/fudbal/medjunarodni-fudbal/liga-sampiona/real-vec-vratio-polovinu-ulozenog-novca-u-belingema-dobar-deo-zasluga-za-to-snosi-i-sjajni-englez/2023121316465907304",
    "https://sportal.blic.rs/fudbal/medjunarodni-fudbal/serija-a/navijaci-pokazali-razocarenje-igrama-napolija/2024010717243094500",
    "https://sportal.blic.rs/fudbal/medjunarodni-fudbal/sasa-ilic-je-nepobediv-u-grckoj-vec-dva-meseca/2024010715420284487",
    "https://sportal.blic.rs/fudbal/torino-pobedio-napoli-lacio-pobedio-udineze-u-seriji-a/2024010716050379572",
    "https://sportal.blic.rs/fudbal/medjunarodni-fudbal/liverpul-pobedio-arsenal-u-londonu-u-mecu-3-kola-fa-kupa/2024010716162470361",
    "https://sportal.blic.rs/fudbal/medjunarodni-fudbal/serija-a/napadacu-verone-prete-smrcu-zbog-promasenog-penala-protiv-intera/2024010714553416388",
    "https://sportal.blic.rs/fudbal/medjunarodni-fudbal/tadic-se-nije-proslavio-na-bozic-srbin-promasio-penal-u-petardi-fenera-dusanov-saigrac-dao-cetiri-gola/2024010714392608905",
    "https://sportal.blic.rs/fudbal/medjunarodni-fudbal/sportal-intervju-marko-milosevic-o-odlasku-iz-debrecina-i-sansi-da-se-vrati-u-srbiju/2024010701511220066",
    "https://sportal.blic.rs/fudbal/reprezentacija-srbije/a-tim/dragan-stojkovic-piksi-veliki-intervju-za-sportal-o-ostanku-na-mestu-selektora-srbiji-nasem-fudbalu-zvezdi-partizanu-i-evropskom-prvenstvu-2024/2023123023291257677",
    "https://sportal.blic.rs/fudbal/srbija/partizan/mateus-saldanja-za-sportal-o-duljaju-partizanu-srbiji-i-cevapima-ronaldu-rambu-fudbalu-i-kosarci/2023122920151169834"    
]

# Inicijalizacija praznog rječnika za čuvanje rezultata za sve URL-ove
brojac_svih_rijeci = {url: Counter({rijec: 0 for rijec in kljucne_rijeci}) for url in urls}

# Iteriranje kroz svaki URL
for url in urls:
    # Poslati zahtev ka URL-u
    response = requests.get(url)

    # Provjera da li je zahtjev uspešan (status code 200 znači uspješan zahtjev)
    if response.status_code == 200:
        # Kreiranje BeautifulSoup objekta za parsiranje HTML-a
        soup = BeautifulSoup(response.content, "html.parser")

        # Nalaženje elemenata koji sadrže tekst članka
        article = soup.find("div", class_="single-news-content")

        if article:
            # Izvlačenje teksta članka
            paragraphs = article.find_all("p")
            text = "\n".join([paragraph.get_text() for paragraph in paragraphs])

            # Lematizovanje riječi(pretvaranje u osnovni oblik riječi) i konverzija cijele riječi u mala slova
            doc = nlp(text)
            lemmatized_words = [rijec.lemma.lower() for sent in doc.sentences for rijec in sent.words]

            # Prebrojavanje traženih riječi u tekstu
            for rijec in lemmatized_words:
                if rijec in kljucne_rijeci:
                    brojac_svih_rijeci[url][rijec] += 1

        else:
            print(f"Tekst članka nije pronađen za URL: {url}")
    else:
        print(f"Greška pri pristupanju stranici {url}: {response.status_code}")

# Čuvanje svih rezultata u jedan CSV fajl
with open('brojacRijeciPoUrlovima.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    # Kreiranje reda sa zaglavljem (ključne riječi)
    writer.writerow(kljucne_rijeci)
    # Dodavanje redova sa brojem riječi za svaki URL
    for url in urls:
        brojac_jednog_urla = [brojac_svih_rijeci[url][rijec] for rijec in kljucne_rijeci]
        writer.writerow(brojac_jednog_urla)

print("Rezultati za svaki URL su sačuvani u brojacRijeciPoUrlovima.csv fajlu.")
