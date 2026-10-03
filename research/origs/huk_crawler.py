# -*- coding: utf-8 -*-


import json
import os
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
import random
import math
from difflib import SequenceMatcher
import requests
import pandas as pd
from utils import HrServiceURL as URL
from utils import HrPayload as Payload
from utils import FilePath as FPath
from utils import create_dir
from utils import ergo_proxies as ep
from utils import random_header


def merge(dictionary_list):
    """kombiniert Liste von Dictionaries zu einem großen Dictionary"""
    result = {}
    for dictionary in dictionary_list:
        result = result | dictionary
    return result


def recommend_price(area, rec=700):
    """liefert zu Fläche und empfohlenen Preis pro m^2 VSU in Tausend"""
    return int(area* rec) #int(math.ceil(area * rec / 1000)) nach anpassung offer link angepasst


def standardize_city(base_city, plz, proxies, header):
    """bestimmt die im Namen zu base_city ähnlichste Stadt aus der Liste von Städten die vom Server zur Postleitzahl angebeben werden"""
    resp = requests.get(url=URL.PLZ.format(plz=plz), proxies=proxies, headers=header, timeout=60)
    try:
        city_list = resp.json()
    except ValueError:
        print(resp)
        return base_city
    else:
        comparison_score = dict(zip(city_list, [SequenceMatcher(None, base_city, city).ratio() for city in city_list]))
        return max(comparison_score, key=comparison_score.get)


def complete_address(plz, street, city, proxies, header):
    """
    füllt Adresse zur Eingabe passend aus

    Übergabewerte dürfen nicht leer sein
    sucht Adresse, die zur gegebenen PLZ passt, und deren Straßen-/Stadtnamen mit den jeweiligen Eingabe-Strings starten
    """
    response = requests.get(url=URL.ADDRESS.format(plz=plz, street=street, city=city), proxies=proxies, headers=header, timeout=60)  # gibt als Antwort Liste mit möglichen Adressen zurück
    try:
        return response.json()[0]  # erste Adresse aus der Liste
    except ValueError:  # falls keine Adresse gefunden wird, sendet die Website keine Antwort: Zeile 64 liefert JSONDecodeError
        return 0  # siehe Zeile 119


def translate(row, calc_model):
    """
    überschreibt übergebenes calc_model Dictionary
    mit Daten aus übergebener row/Zeile vom DataFrame
    und passt sie so an, dass sie Sinn ergeben
    """
    for key, value in row.items():
        if key == "berufsgruppe":
            calc_model[key] = value

        if key == "versicherungssumme":
            calc_model["angebot"][key] = recommend_price(area=row["wohnflaeche"]) if math.isnan(value) else value  # nehme empfohlenen Preis, falls keiner vorgegeben
        elif key == "selbstbeteiligung":
            calc_model["angebot"][key] = value
        elif key in ["glas", "elementar", "erdbeben", "schutzbrief", "fdcheck", "fdversicherungssumme"]:
            if key.startswith("fd"):
                new_key = key.replace("fd", "")
                calc_model["angebot"]["options"]["fahrraddiebstahl"][new_key] = value
            else:
                calc_model["angebot"]["options"][key] = value
        elif key in ["zahlungsweise", "produktlinie"]:
            calc_model["angebot"]["product"][key] = value
            # hrPlus == True <=> produktlinie == 'CLASSIC_PLUS', nicht in Eingabedaten erhalten, sondern wird hergeleitet
            if key == "produktlinie":
                calc_model["angebot"]["options"]["hrPlus"] = value == "CLASSIC_PLUS"
        elif key == "schadenverlauf":
            calc_model[key] = value
        elif key in ["haustyp", "wohnflaeche"]:
            calc_model["apartment"][key] = value
    # 'schutzbrief' sollte nicht existieren, falls Basis beantragt wird
    if calc_model["angebot"]["product"]["produktlinie"] == "BASIC":
        del calc_model["angebot"]["options"]["schutzbrief"]


def crawlworker(data, proxies, header_list):
    """
    Crawler-Arbeiter

    generiert aus DataFrame Input ein Dictionary mit Preisen zu jeder Zeile im DataFrame als Eingabe
    """
    result = {}
    for index, row in data.iterrows():  # iteriere durch jede Zeile
        print("Bearbeite Zeile " + str(index)+"...")
        payload = Payload()
        calc_model = payload.calc_model  # erstelle Standard-Payload, der überschrieben wird
        random.seed(index)  # für Reproduzierbarkeit in Zeile 70
        translate(row, calc_model)  # überschreibe mit Werten aus der Zeile
        full_plz = str(row['plz']).zfill(5)  # auffüllen der PLZ mit Nullen links
        # nachdem PLZ formatkonform ist, wird im Anschluss eine passende Adresse zur PLZ gesucht
        std_city = row["stadt"]
        sample_address = 0
        letters = [chr(x) for x in random.sample([*range(65, 91)], 26)]  # zufällige Anordnung der (Groß-)Buchstaben A-Z
        while sample_address == 0 and letters:  # Schleife endet, sobald eine echte Adresse gefunden wird, oder wenn alle Buchstaben ausprobiert wurden
            if len(letters) == 16:  # falls bei complete_addresss nichts gefunden wird, kann es an dem Namen der Stadt liegen, suche richtigen Stadtnamen, falls 10 Buchstaben ausprobiert wurden
                std_city = standardize_city(std_city, full_plz, proxies, header_list[0])
            sample_address = complete_address(plz=full_plz, street=letters[0], city=std_city, proxies=proxies, header=header_list[0])
            del letters[0]
        if sample_address != 0:  # findet complete_address eine Adresse, wird diese nun ins Payload geschrieben
            calc_model["apartment"]["adresse"]["plzOrt"]["plz"] = sample_address["zip"]
            calc_model["apartment"]["adresse"]["plzOrt"]["ort"] = sample_address["city"]
            calc_model["apartment"]["adresse"]["strasse"] = sample_address["street"]
            calc_model["apartment"]["adresse"]["ortsteil"] = sample_address["district"]
        else:  # falls nach dem Loop trz. keine Antwort zurück kommt, wird die Stadt aus dem DataFrame reingeschrieben und 'street' auf Standardwert 'a' gesetzt
            calc_model["apartment"]["adresse"]["plzOrt"]["ort"] = std_city
        resp = requests.post(URL.OFFER, json=calc_model, proxies=proxies, headers=header_list[1], timeout=60)
        # frage Preise ab
        # Ergebnisse einer Abfrage abspeichern in calc_data
        calc_data = {}
        calc_data["id"] = index
        calc_data["berechnungsdatum"] = datetime.now().strftime("%d%h%y")
        calc_data["adresse"] = calc_model["apartment"]["adresse"]
        try:
            calc_data["response"] = resp.json()
        except ValueError:  # analog zu Zeile 65
            calc_data["response"] = "status code " + str(resp.status_code) + " - " + bytes.decode(resp.content) + " - hier ist etwas schiefgelaufen!"
            print(str(index) + ": " + calc_data["response"])
        finally:
            result[calc_data["id"]] = calc_data  # Ergebins einer Abfrage einbetten
            time.sleep(random.uniform(2, 4))  # Pause zwischen jeder Abfrage, um die Seite zu entlasten / nicht aufzufallen
    return result


def mp_crawl(data, num_processes, proxies):
    """
    Parallelisierung der Crawler-Arbeiter in crawlworker
    Nimmt Datensatz und spaltet ihn gleichmäßig auf
    führt parallel crawlworker mit gespaltenen Daten aus und aggregiert diese
    Ein Header für alle Anfragen
    """
    chunksize = int(math.ceil(len(data) / num_processes))  # Anzahl Daten / Anzahl paralleler Prozesse auf nächsthöhere ganze Zahl gerundet
    num_processes = int(math.ceil(len(data) / chunksize))  # passt Anzahl der Arbeiter auf das Nötige an
    data_chunked = [data.iloc[chunksize * i: chunksize * (i + 1)] for i in range(num_processes)]  # Datensatz in mehrere aufgeteilt, verpackt in einer Liste
    header_list = random_header()
    with ThreadPoolExecutor() as executor:
        results = executor.map(crawlworker, data_chunked, repeat(proxies), repeat(header_list))  # wertet pro Eintrag der Übergabe (hier pro Datensatz) crawlworker aus
    return list(results)  # Ergebnis ist ein Iterable, deswegen kann man es nicht einfach so zurückgeben


def edit_huk_output(input_csv, data):
    rows_list = []
    # Output für je eine Zeile im csv
    for index in data:
        dict1 = {}
        try:
            dict1.update({k: v for k, v in data[index]['adresse'].items() if k in ['strasse', 'hausnummer', 'ortsteil']})
            dict1.update({'ort': data[index]['adresse']['plzOrt']['ort']})
            dict1.update(data[index]['response'])
        except TypeError:
            print(index)
        finally:
            rows_list.append(dict1)
    df = pd.DataFrame(rows_list)
    result = pd.concat([input_csv.loc[:, input_csv.columns != 'doof'], df], axis=1)  # kombinieren
    return result


if __name__ == "__main__":
    # preliminary
    DATUM = datetime.now().strftime('%d%h%y')
    DATA_STRING = 'standard_input.csv'
    INPUTPATH = FPath.HR_INPUT_DIR + '\\' + DATA_STRING
    INPUTDATA = pd.read_csv(INPUTPATH, sep=',', encoding='latin-1')
# crawlen (und Timer)
    start_time = time.time()
    NUM_PROCS = 1  # Anzahl paralleler Prozesse, am besten 1
    res = merge(mp_crawl(INPUTDATA, NUM_PROCS, proxies=ep.proxies))
    comp_time = "--- %s seconds ---" % (time.time() - start_time)
# Ordner erstellen
    mother_path = os.path.join(FPath.HR_OUTPUT_DIR, 'huk_' + DATUM)
    create_dir(mother_path)
# finale JSON-Datei
    json_dict = {'num_processes': NUM_PROCS, 'Computation Time': comp_time, 'Daten': res}
# Dateipfäde erstellen
    result_path_string = DATA_STRING + '_result'
    result_path_json = os.path.join(mother_path, result_path_string + '.json')
    result_path_xlsx = os.path.join(mother_path, result_path_string + '.xlsx')
# raw JSON ausschreiben
    with open(result_path_json, 'w+', encoding='latin-1') as db:
        json.dump(json_dict, db, indent=4, ensure_ascii=False)
# Output editieren / mit Input kombinieren
    with open(result_path_json) as f:
        huk_data = json.load(f)['Daten']  # lese Daten aus dem oben abgeschriebenen JSON wieder aus, eigentlich nicht nötig, weil es intern gespeichert ist
    huk_df = edit_huk_output(INPUTDATA, huk_data)
# in Excelsheet schreiben
    with pd.ExcelWriter(result_path_xlsx, mode='w') as writer:
        huk_df.to_excel(writer, sheet_name='Huk_Output')
# Laufzeit
    print("--- %s seconds ---" % (time.time() - start_time))
