# obdelava-podatkov---programiranje-1
# Avtor 
Matej Novoselec

# IGRALCI LIGE NBA
Analiziral bom statistiko/podatke o igralcih iz ameriške lige NBA, v sezonah, ko je dostop do podatkov mogoč (1996/97-2020/21). Te podatke, ki ji bom po letih dobil na povezavi: https://www.nba.com/stats/players/traditional/?SeasonType=Regular%20Season&sort=PTS&dir=-1&Season=2020-21, bom nato še dopolnil s podatki, ki jih bom dobil iz širše baze, ki jo prav tako vodi NBA in je na povezavi: https://www.nba.com/players, če omogočimo "show historic"

# OPOMBA
Po posvetu z asistentom, sem se odlocil spletno stran iz katere bom zajemal podatke spremeniti (zajem je bil prek prejsne strani pretezek - potrebno bi bilo znanje zajemanja s pomocjo JavaScripta). Glavni podatki, ki sem jih imel namen zajeti so na novo izbrani strani se prekrivajo, zato ne bo potrebno spremeniti vseh hipotez. <br>
Url nove strani: od let https://www.basketball-reference.com/leagues/NBA_1980_per_game.html do https://www.basketball-reference.com/leagues/NBA_2020_per_game.html<br>


# Za vsakega igralca bom zajel:
-ime, priimek<br>
-pozicijo <br>
-povprečje metov<br>
-povprečni odstotek meta za 2 in 3, povprečni odstotek prostih metov<br>
-povprečje točk<br>
-povprečno število asistenc<br>
-povprečno število skokov

# Delovne hipoteze:
-Obstaja povezava med povprečnim odstotkom meta za 2 in 3, ter povprečnim odstotkom prostih metov<br>
-Igralci pozicij G (guards) dosežejo povprečno več točk na tekmo kot igralci pozicij F (forwards)<br>
-igralci pozicije C (center), dosežejo povprečno več skokov, kot igralci pozicij F (forwards) in G (guards) skupaj<br>
-Igralci pozicij g (guards) imajo največji odstotek meta (povsod), sledijo jih igralci pozicij F (forwards) in nato igralci pozicije C (center)
