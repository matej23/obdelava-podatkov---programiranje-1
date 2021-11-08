
import requests
import re
import os
import csv

###############################################################################
# Najprej definirajmo nekaj pomožnih orodij za pridobivanje podatkov s spleta.
###############################################################################

# definirajte URL glavne strani bolhe za oglase z mačkami
#cats_frontpage_url = 'https://www.basketball-reference.com/leagues/NBA_2020_per_game.html'
# mapa, v katero bomo shranili podatke
file_directory = 'C:/Users/matej/OneDrive/Namizje/obdelava podatkov/obdelava-podatkov---programiranje-1'
# ime datoteke v katero bomo shranili glavno stran
frontpage_filename = 'index_players.html'
# ime CSV datoteke v katero bomo shranili podatke
csv_filename = 'players.csv'


def download_url_to_string(url):
    """Funkcija kot argument sprejme niz in poskusi vrniti vsebino te spletne
    strani kot niz. V primeru, da med izvajanje pride do napake vrne None.
    """
    try:
        # del kode, ki morda sproži napako
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        # koda, ki se izvede pri napaki
        # dovolj je če izpišemo opozorilo in prekinemo izvajanje funkcije
        print("Napaka pri povezovanju do:", url)
        return None
    # nadaljujemo s kodo če ni prišlo do napake
    if r.status_code == requests.codes.ok:
        return r.text
    else:
        print("Napaka pri prenosu strani:", url)
        return None

#vec sezon, zato bomo shranili v file vsako posebej
#funkcija vrze linke po sezonah v obliki seznama
def all_seasons_url_dict(start, finish):
    dictionary_url = {}
    #prazen seznam urljev
    for year in range(start,finish + 1):
        #dodajanje na seznam leto:url_za_leto
        dictionary_url.update({year : f'https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html'})
    return dictionary_url
#ta je okej

def text_from_url_list(dictionary_url):
    dictionary_year_text = {}
    for url_year in dictionary_url.keys():
        dictionary_year_text.update({url_year : download_url_to_string(dictionary_url[url_year])})
    return dictionary_year_text
#ta je okej

def save_string_to_file(directory, filename, dictionary):
    """Funkcija zapiše vrednost parametra "text" v novo ustvarjeno datoteko
    locirano v "directory"/"filename", ali povozi obstoječo. V primeru, da je
    niz "directory" prazen datoteko ustvari v trenutni mapi.
    """
    text_dictionary = f'{text_from_url_list(dictionary)}'
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text_dictionary)
    return None

# Definirajte funkcijo, ki prenese glavno stran in jo shrani v datoteko.
def save_frontpage(directory, filename):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz"""
    save_string_to_file(directory, filename, all_seasons_url_dict(1950, 2020))
    return None
save_frontpage(file_directory,frontpage_filename)

####
##PRIDOBLJENI PODATKI V OBLIKI SLOVARJA {leto: html za leto} 
####

################################################################################
## Po pridobitvi podatkov jih želimo obdelati.
################################################################################
#
#
#def read_file_to_string(directory, filename):
#    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz"""
#    path = os.path.join(directory, filename)
#    with open(path, 'r', encoding='utf-8') as file_in:
#        return file_in.read()
#
## Definirajte funkcijo, ki sprejme niz, ki predstavlja vsebino spletne strani,
# in ga razdeli na dele, kjer vsak del predstavlja en oglas. To storite s
# pomočjo regularnih izrazov, ki označujejo začetek in konec posameznega
# oglasa. Funkcija naj vrne seznam nizov.


#def page_to_ads(page_content):
#    """Funkcija poišče posamezne oglase, ki se nahajajo v spletni strani in
#    vrne njih seznam"""
#    rx = re.compile(r'<li class="EntityList-item EntityList-item--Regular'
#                    r'(.*?)</article>',
#                    re.DOTALL)
#    ads = re.findall(rx, page_content)
#    return ads
#
## Definirajte funkcijo, ki sprejme niz, ki predstavlja oglas, in izlušči
## podatke o imenu, lokaciji, datumu objave in ceni v oglasu.
#
#
#def get_dict_from_ad_block(block):
#    """Funkcija iz niza za posamezen oglasni blok izlušči podatke o imenu,
#    lokaciji, datumu objave in ceni ter vrne slovar, ki vsebuje ustrezne
#    podatke"""
#    rx = re.compile(r'<h3.*>(?P<name>.*?)</a></h3>'
#                    r'.*?"pubdate">(?P<time>.*?)</time>'
#                    r'.*?<strong class="price price--hrk">\s*?(?P<price>\d*)&',
#                    re.DOTALL)
#    data = re.search(rx, block)
#    ad_dict = data.groupdict()
#
#    # Ker nimajo vsi oglasi podatka o lokaciji, to rešimo z dodatnim vzorcem
#    rloc = re.compile(r'Lokacija: </span>(?P<location>.*?)<br />')
#    locdata = re.search(rloc, block)
#    if locdata is not None:
#        ad_dict['location'] = locdata.group('location')
#    else:
#        ad_dict['location'] = 'Unknown'
#
#    return ad_dict
#
## Definirajte funkcijo, ki sprejme ime in lokacijo datoteke, ki vsebuje
## besedilo spletne strani, in vrne seznam slovarjev, ki vsebujejo podatke o
## vseh oglasih strani.
#
#
#def ads_from_file(filename, directory):
#    """Funkcija prebere podatke v datoteki "directory"/"filename" in jih
#   pretvori (razčleni) v pripadajoč seznam slovarjev za vsak oglas posebej."""
#    page = read_file_to_string(filename, directory)
#    blocks = page_to_ads(page)
#    ads = [get_dict_from_ad_block(block) for block in blocks]
#    return ads
#
#
#def ads_frontpage():
#    return ads_from_file(file_directory, frontpage_filename)
#
################################################################################
## Obdelane podatke želimo sedaj shraniti.
################################################################################
#
#
#def write_csv(fieldnames, rows, directory, filename):
#    """
#    Funkcija v csv datoteko podano s parametroma "directory"/"filename" zapiše
#    vrednosti v parametru "rows" pripadajoče ključem podanim v "fieldnames"
#    """
#    os.makedirs(directory, exist_ok=True)
#    path = os.path.join(directory, filename)
#    with open(path, 'w', encoding='utf-8') as csv_file:
#        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#        writer.writeheader()
#        for row in rows:
#            writer.writerow(row)
#    return None
#
## Definirajte funkcijo, ki sprejme neprazen seznam slovarjev, ki predstavljajo
## podatke iz oglasa mačke, in zapiše vse podatke v csv datoteko. Imena za
## stolpce [fieldnames] pridobite iz slovarjev.
#
#
#def write_cat_ads_to_csv(ads, directory, filename):
#    """Funkcija vse podatke iz parametra "ads" zapiše v csv datoteko podano s
#    parametroma "directory"/"filename". Funkcija predpostavi, da so ključi vseh
#    slovarjev parametra ads enaki in je seznam ads neprazen."""
#    # Stavek assert preveri da zahteva velja
#    # Če drži se program normalno izvaja, drugače pa sproži napako
#    # Prednost je v tem, da ga lahko pod določenimi pogoji izklopimo v
#    # produkcijskem okolju
#    assert ads and (all(j.keys() == ads[0].keys() for j in ads))
#    write_csv(ads[0].keys(), ads, directory, filename)
#
#
## Celoten program poženemo v glavni funkciji
#
#def main(redownload=True, reparse=True):
#    """Funkcija izvede celoten del pridobivanja podatkov:
#    1. Oglase prenese iz bolhe
#    2. Lokalno html datoteko pretvori v lepšo predstavitev podatkov
#    3. Podatke shrani v csv datoteko
#    """
#    # Najprej v lokalno datoteko shranimo glavno stran
#    save_frontpage(file_directory, frontpage_filename)
#
#    # Iz lokalne (html) datoteke preberemo podatke
#    ads = page_to_ads(read_file_to_string(file_directory, frontpage_filename))
#    # Podatke preberemo v lepšo obliko (seznam slovarjev)
#    ads_nice = [get_dict_from_ad_block(ad) for ad in ads]
#    # Podatke shranimo v csv datoteko
#    write_cat_ads_to_csv(ads_nice, file_directory, csv_filename)
#
#    # Dodatno: S pomočjo parametrov funkcije main omogoči nadzor, ali se
#    # celotna spletna stran ob vsakem zagon prenese (četudi že obstaja)
#    # in enako za pretvorbo
#
#
#if __name__ == '__main__':
#    main()