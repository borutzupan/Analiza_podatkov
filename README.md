# Analiza podatkov


Za projektno nalogo pri predmetu Programiranje 1 bom analiziral prvih 50 strani na spletni strani
[Anime-planet](https://www.anime-planet.com/anime/all) glede na popularnost. Podatke sem uredil v csv in json datoteke. 


**1.** V mapi **Csv_files** so shranjene naslednje datoteke:
- *anime-planet.csv*, kjer sem zajel:
  * id
  * naslov (tudi alternativni naslov)
  * tip
  * studio
  * število epizod
  * leto izida
  * povprečno oceno
- *anime-planet_tags.csv*, kjer sem zajel:
  * oznake


**2.** V mapi **Json** je shranjena datoteka:
- *anime-planet.json*, kjer sem v jason obliki zajel iste podatke kot v datoteki *anime-planet.csv*.

**3.** V mapi **Pages** sem shranil vse strani, ki sem jih naložil.

**4.** Dodal sem tudi datoteki *Code.py* in *tags.py*, s katerima sem vse podatke shranil v csv in json datoteke, in datoteko *save.py*, s katero sem naložil in shranil spletne strani v html obliki.

Delovne hipoteze:
* Kateri *žanri* so najbolj popularni?
* Kateri *studii* imajo največ najbolje ocenjenih filmov?
* Ali so anime z več *epizod* bolje ocenjeni?
* Kateri *studii* so izdali največ epizod?
* Ali imajo anime, ki so izšli kasneje več *epizod*?

> Najprej sem v datoteki *anime-planet.csv* zajel tudi opis od anime, ki pa ga ne bom uporabljal in sem ga zato v kodi zakomentiral.
