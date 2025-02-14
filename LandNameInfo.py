from iso3166 import countries
import pycountry
import translators as ts

class GetLandNameInfo:                   #sammelt Nameninformationen von Ländern

        def __init__(self, offer_land: str):
                self.land_in_en=ts.translate_text(offer_land, to_language='en') #übersetzt Land in englisch
                self.land_info=str(pycountry.countries.search_fuzzy(self.land_in_en)) #sucht Land in Länderverzeichnis
                self.land_kuerzel=self.land_info.split("'")[1]          #gibt Kürzel des Landes aus



        def get_Kuerzel(self):          #gibt Kürzel des Landes aus
           return self.land_kuerzel

