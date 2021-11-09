
import requests
import re
import os
import csv

file_directory = 'C:/Users/matej/OneDrive/Namizje/obdelava podatkov/obdelava-podatkov---programiranje-1'
frontpage_filename = 'index_players.html'
csv_filename = 'players.csv'

def download_url_to_string(url):
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print("Napaka pri povezovanju do:", url)
        return None
    if r.status_code == requests.codes.ok:
        return r.text
    else:
        print("Napaka pri prenosu strani:", url)
        return None

#vec sezon, zato bomo podartke morali pobrati iz vseh sezon (razlicni linki)
#funkcija vrze linke po sezonah v obliki seznama
def all_seasons_url_dict(start, finish):
    dictionary_url = {}
    for year in range(start,finish + 1):
        #dodajanje na seznam leto:url_za_leto
        dictionary_url.update({year : f'https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html'})
    return dictionary_url

#funkcija sprejme seznam elementov oblike {leto :url} in vrne tekst za posamezno leto (njegov url)
def text_from_url_dictionary(dictionary_url):
    dictionary_year_text = {}
    for url_year in dictionary_url.keys():
        dictionary_year_text.update({url_year : download_url_to_string(dictionary_url[url_year])})
    return dictionary_year_text

#shrani slovar v file 
def save_string_to_file(directory, filename, dictionary):
    text_dictionary = f'{text_from_url_dictionary(dictionary)}'
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text_dictionary)
    return None

# funkcija shrani podatke, ki jih bomo obdelovali 
def save_frontpage(directory, filename):
    save_string_to_file(directory, filename, all_seasons_url_dict(1980,2020))
    #od 1980 naprej, saj so od tam naprej navedeni vsi potrebni podatki
    return None

####
##PRIDOBLJENI PODATKI V OBLIKI SLOVARJA {leto: html za leto} 
####
##OBEDALAVA PODATKOV
####

#prebere file v obliki niza
def read_file_to_string(directory, filename):
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        return file_in.read()

#string (ki bo kot slovar razvrscen po letih - ni pomembno, le za vecjo preglednost), bo spodnja funkcija razbila na posamezne igralce
#funkcija pripravi tudi vse potrebne podatke za igralce

def page_to_players(page_content):
    rx = re.compile(r'<a href="/players(?P<url_name>/\w/\w+?\d\d).html">(?P<name>.{1,30})</a></td>.+?'
                    r'data-stat="pos" >(?P<position>.*?)</td>.+?'
                    r'data-stat="fg_pct" >(?P<fg_pct>.*?)</td>.+?'
                    r'data-stat="fg3_pct" >(?P<fg3_pct>.*?)</td>.+?'
                    r'data-stat="fg2_pct" >(?P<fg2_pct>.*?)</td>.+?'
                    r'data-stat="ft_pct" >(?P<ft_pct>.*?)</td>.+?'
                    r'data-stat="trb_per_g" >(?P<rebounds>.*?)</td>.+?'
                    r'data-stat="ast_per_g" >(?P<asists>.*?)</td>.+?'
                    r'data-stat="pts_per_g" >(?P<points>.*?)</td>',
                    re.DOTALL)
#VZOREC ZA IGRALCA
#                    <a href="/players/y/youngth01.html">Thaddeus Young</a></td>
#                    <td class="center " data-stat="pos" >PF</td
#                    <td class="right " data-stat="fg_pct" >.448</td
#                    <td class="right " data-stat="fg3_pct" >.356</td
#                    <td class="right " data-stat="fg2_pct" >.501</td
#                    <td class="right non_qual" data-stat="ft_pct" >.583</td
#                    <td class="right " data-stat="trb_per_g" >4.9</td>
#                    <td class="right " data-stat="ast_per_g" >1.8</td
#                    <td class="right " data-stat="pts_per_g" >10.3</td>
    all_players = re.findall(rx, page_content)
    return all_players

#nabor za igralce iz razlicnih sezon(igralec se lahko veckrat ponovi), ustrezno obdela in vrne slovar s povprecji za igralca    
def final_data_players_from_seasons(all_players):
    dictionary_players = {}
    for player in all_players:
        final_data_player = {}
        fg_pct = 0
        fg3_pct = 0
        fg2_pct = 0
        ft_pct = 0
        rebounds = 0
        asists = 0
        points_per_game = 0 
        list_data_player = []
        for player_search in all_players:
            if player[0] == player_search[0]:
                list_data_player.append(player_search)

        for i in range(len(list_data_player)):
            if list_data_player[i][3] != '': 
                fg_pct += float(list_data_player[i][3])
            else:
                pass
            if list_data_player[i][4] != '': 
                fg3_pct += float(list_data_player[i][4])
            else:
                pass
            if list_data_player[i][5] != '': 
                fg2_pct += float(list_data_player[i][5])
            else:
                pass
            if list_data_player[i][6] != '':
                ft_pct += float(list_data_player[i][6])
            else:
                pass
            if list_data_player[i][7] != '': 
                rebounds += float(list_data_player[i][7])
            else:
                pass
            if list_data_player[i][8] != '':
                asists += float(list_data_player[i][8])
            else:
                pass
            if list_data_player[i][9] != '':
                points_per_game += float(list_data_player[i][9])
            else:
                pass
        #sestejemo vse podatke za igralca po kategorijah po sezonah 
        fg_pct = round(ft_pct/len(list_data_player),2)
        fg3_pct = round(fg3_pct/len(list_data_player),2)
        fg2_pct = round(fg2_pct/len(list_data_player),2)
        ft_pct = round(ft_pct/len(list_data_player),2) 
        rebounds = round(rebounds/len(list_data_player),2)
        asists = round(asists/len(list_data_player),2)
        points_per_game = round(points_per_game/len(list_data_player),2)
        #delimo podatke s stevilom sezon da dobimo povprecje
        final_data_player = {list_data_player[0][1]:
            {'position': list_data_player[0][2],
            'fg_pct': fg_pct,
            'fg3_pct': fg3_pct,
            'fg2_pct': fg2_pct,
            'ft_pct': ft_pct,
            'rebounds': rebounds,
            'asists': asists,
            'points_per_game' : points_per_game,
            }
        }
        #sestavimo podatke/povprecje za posameznega igralca in podatke preusmerimo v slovar
        dictionary_players.update(final_data_player)
    return dictionary_players

def players_from_file(filename, directory):
    text_all = read_file_to_string(filename, directory)
    all_players = page_to_players(text_all)
    players_data = final_data_players_from_seasons(all_players)
    return players_data

##PODATKE SHRANIMO V PRIPRAVLJENO DATOTEKO 
#save_frontpage(file_directory, frontpage_filename)

##PODATKE O IGRALCIH DOBIMO V OBLIKI SLOVARJA
def players():
    return players_from_file(file_directory, frontpage_filename)


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