# -*- coding: utf-8 -*-


import os
from pathlib import Path
from getpass import getuser
from random import choice


class ergo_proxies(object):
    user = getuser()
    password = Path('C:/Users/' + user + '/Documents/password.txt').read_text()
    proxies = {
        'http': 'http://' + user + ':' + password + '@proxy:81',
        'https': 'http://' + user + ':' + password + '@proxy:81'
    }


class HrServiceURL(object):
    PLZ = 'https://www.huk.de/loc/api/cities/zbnr?postalcode={plz}' # https://www.huk.de/loc/api/cities/zbnr?postalcode=
    DISTRICT = 'https://www.huk.de/as/api/standardize'  # sucht zu Input ähnlichste Adresse(PLZ, Ort, Ortsteil, ggf. Straße). Achtung: verändert ggf. PLZ(z.B. Mayen-Umland wird zu Mayen), deswegen nicht benutzen!
    ADDRESS = 'https://www.huk.de/as/api/complete/params?zip={plz}&street={street}&city={city}'  # gibt Liste von möglichen Adressen zurück bei nicht vollständiger Eingabe, evtl. nicht nötig wg. standardize
    OFFER = 'https://www.huk.de/hr/api/13/tarifiere' # NIK: von 12 zu 13 angepasst


def create_dir(path, parents=False):
    Path(path).mkdir(parents=parents, exist_ok=True)


DEBUG_OUTPUT = True

current_dir = os.path.dirname(__file__)
LANDING_DIR = os.path.join(current_dir, 'LANDING_DIR')


class FilePath(object):
    HR_INPUT_DIR = os.path.join(LANDING_DIR, 'input')
    HR_OUTPUT_DIR = os.path.join(LANDING_DIR, 'result')
    PAYLOAD_DIR = os.path.join(LANDING_DIR, 'payload')
    LOG_DIR = os.path.join(LANDING_DIR, 'meta')


def random_header():
    user_agents = ['Mozilla\\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\\/537.36 (KHTML, like Gecko) Chrome\\/114.0.0.0 Safari\\/537.36',
                   'Mozilla\\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\\/537.36 (KHTML, like Gecko) Chrome\\/114.0.0.0 Safari\\/537.36',
                   'Mozilla\\/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko\\/20100101 Firefox\\/114.0',
                   'Mozilla\\/5.0 (X11; Linux x86_64) AppleWebKit\\/537.36 (KHTML, like Gecko) Chrome\\/114.0.0.0 Safari\\/537.36',
                   'Mozilla\\/5.0 (X11; Linux x86_64; rv:109.0) Gecko\\/20100101 Firefox\\/114.0',
                   'Mozilla\\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\\/537.36 (KHTML, like Gecko) Chrome\\/113.0.0.0 Safari\\/537.36',
                   'Mozilla\\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\\/537.36 (KHTML, like Gecko) Chrome\\/113.0.0.0 Safari\\/537.36',
                   'Mozilla\\/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko\\/20100101 Firefox\\/113.0',
                   'Mozilla\\/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko\\/20100101 Firefox\\/114.0',
                   'Mozilla\\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\\/605.1.15 (KHTML, like Gecko) Version\\/16.5 Safari\\/605.1.15',
                   'Mozilla\\/5.0 (Windows NT 10.0; rv:114.0) Gecko\\/20100101 Firefox\\/114.0',
                   'Mozilla\\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\\/537.36 (KHTML, like Gecko) Chrome\\/114.0.0.0 Safari\\/537.36 Edg\\/114.0.1823.43',
                   'Mozilla\\/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko\\/20100101 Firefox\\/114.0',
                   'Mozilla\\/5.0 (X11; Linux x86_64; rv:102.0) Gecko\\/20100101 Firefox\\/102.0',
                   'Mozilla\\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\\/537.36 (KHTML, like Gecko) Chrome\\/113.0.0.0 Safari\\/537.36 OPR\\/99.0.0.0',
                   'Mozilla\\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\\/537.36 (KHTML, like Gecko) Chrome\\/109.0.0.0 Safari\\/537.36']
    user_agent = choice(user_agents)
    address_header = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Referer': 'https://www.huk.de/tarifrechner/hr/angebotsdaten',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': user_agent
    }
    offer_header = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://www.huk.de',
        'Referer': 'https://www.huk.de/tarifrechner/hr/angebotsdaten',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': user_agent
    }
    header_list = [address_header, offer_header]
    return header_list

# Standard-Payload, der ggf. modifiziert wird


class HrPayload(object):
    def __init__(self):
        self._calc_model = {
            'berufsgruppe': 'OEFFENTLICHER_DIENST',  # oder NICHT_OEFFENTLICHER_DIENST
            'angebot': {
                'versicherungssumme': 800,  # in Tausend €, 700-1500€/m^2, standardmäßig Wohnfläche(m^2)*700(€/m^2) aufgerundet auf nächstliegende Tausend
                'selbstbeteiligung': 'SELBSTBETEILIGUNG_300',  # 300 oder 0€
                'options': {
                    'glas': False,
                    'elementar': False,  # fest auf False, falls Objekt in Zone 0 oder 4 liegt
                    'elemPruef': False,  # existiert nur, falls Zone 0 oder 4 (und der Kunde Option hinzu nehmen möchte), ersetzt Funktionalität von 'elementar'
                    'erdbeben': False,  # manchmal nicht möglich auszuwählen wg. Lage, existiert aber immer im Hintergrund
                    'hrPlus': False,  # true gdw. Classic Plus ausgewählt, gibt Aufpreis von Classic zu Classic Plus an
                    'schutzbrief': False,  # existiert nicht für Basis-Schutz
                    'fahrraddiebstahl': {
                        'check': False,              # NIK: Switched          
                        'versicherungssumme': 1000,  # NIK: Switched - standardmäßig 1000, auch wenn check == False, 200-10000€
                        "fahrradanzahl": 1,          # NIK: Added
                        "fahrradproduktlinie": "DIEBSTAHL", # NIK: Added
                        "verschleiss": False         # NIK: Added
                    }
                },
                'product': {
                    'zahlungsweise': 'JAEHRLICH',
                    #'paymentInterval': 1,  # 1=jährlich, 2=halbjährlich, 4=vierteljährlich # alter Code ab Q2 24 Zeile darüber
                    'produktlinie': 'CLASSIC'  # relevant für Zusatzoptionen
                }
            },
            'schadenverlauf': 'SCHADENVERLAUF_JA',  # oder SCHADENVERLAUF_NEIN. JA bedeutet keinen Schaden in den letzten 5 Jahren
            'apartment': {
                'haustyp': 'HAUS',  # wird abgefragt, wenn Glasversicherung zugebucht wird, sonst erst nach Abfrage, wirkt sich nur auf 'beitragHrGlas' aus (teurer für Einfamilienhaus)
                'wohnflaeche': 125,  # gibt Richtlinine für Versicherungssumme, 20-300m^2
                'adresse': {
                    'plzOrt': {
                        'plz': '74722',  # immer 5 Ziffern, evtl. mit Nullen auffüllen
                        'ort': 'Buchen'  # wird bei gegebener PLZ automatisch ausgefüllt
                    },
                    'strasse': 'a',   # Straßenname muss nicht voll ausgeschrieben werden, wird automatisch ergänzt(ist dann aber nicht mehr deterministisch), aber darf nicht leer sein
                    'hausnummer': '1',  # nicht zwingend erforderlich, kann evtl. zu verschiedenen Preisen führen, höchstwahrscheinlich aber nicht
                    'ortsteil': ''  # kommt automatisch im Hintergrund dazu, manchmal auch empty string
                }
            }
        }

    @property
    def entry(self):
        return self._entry.copy()

    @property
    def calc_model(self):
        calc_model = self._calc_model.copy()
        return calc_model
