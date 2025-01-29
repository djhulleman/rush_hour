# rush_hour
Rush hour is een bordspel waarmee als doel om de auto's op het bord op zo'n manier te verschuiven dat de rode auto naar buiten kan. Dit kan op verschillende manieren en volgorden gedaan worden. Door het uit testen van verschillende gemmakte algoritme was het doel van dit project om te kijken welk algoritme het best het bordspel kan oplossen.
## Opzet
In requirements.txt staat de benodigde packages die gedownload moeten worden. De python versie dat is gebruikt is Python 3.10.12. requirements is te instaleren door:
```
pip install -r requirements.txt
```
## Experiment
In het algoritme **run_experiments.py** staan alle functies voor het uitvoeren van de experimenten op algorithmes. Voor ieder algorithme is een aparte functie geschreven die het experiment uitvoerd. Ieder functie heeft een eigen **docstring** waarin de werking van het algorimte/experiment staat uitgelegd. 
\
\
Voor het uitvoeren van een experiment run je de bijbehorende functie van run_experiments.py in main.py. Let goed op welke input argumenten nodig zijn. Zorg ervoor dat UserInterface() is uitgecommend, deze heb je niet nodig voor het uitvoeren van experimenten. Voor het uitvoeren van experimentfuncties is de import "from rushhour.algorithms.run_experiments import \*" nodig. Inplaats van "*" kun je ook de desbetrefende functie importeren. 
\
\
De gemaakte algoritmen worden op twee manieren vergeleken. Het algoritme random_move (baseline), random_with_memory en comparing worden op uitkomst vergeleken. Dit wordt gedaan met behulp van het algoritme save_outputs. De algoritmen verschillen niet in uitkomst, ongeacht of ze in een korte of lange periode worden opgelost, daarom worden ze alleen op uitkomst vergeleken.
\
Het algoritme hillclimber wordt in de tijd met zichzelf vergeleken, aangezien dit verschillende uitkomsten geeft tijdens verschillende runs en verschillende tijden.
\
De algoritmen BFS en Astar hebben slechts één uitkomst. Dit is precies dezelfde uitkomst. Aangezien de uitkomst niet anders is in verschillende tijdsduren, wordt dit niet vergeleken qua tijd. Wel kan de runtijd vergeleken worden. 
\
De verzamelde gegevens bevinden zich in de map solutions.


## Aandachtspunten
1. De auto's worden verschoven op 2 manieren; met gebruik van 1 (links, omhoog) en 2 (rechts, omlaag) en met gebruik van -1 (links, omhoog) en 1 (rechts, omlaag). Dit kan verwarrend overkomen dus let daar goed op. Dit levert geen probleem op bij het runnen van de code.
2. Data kan geexporteerd worden naar verschillende plekken. In de code kan gezien worden waar naartoe en wat de naam is. Als export_moves() opgeroepen wordt zonder argument erin wordt de data geexporteerd als output.csv in dezelfde map als het algortime staat waarin het gerund wordt. Als er wel een naam neem wordt gegeven of pad, zal dat gevolgt worden.

## Structuur
De files en algoritmes zijn ingedeeld volgens dit schema:
- **/rushhour**: bevat alle code van dit project
  - **/rushhour/algorithms**: bevat de code voor algoritmes
  - **/rushhour/classes**: bevat de classes voor deze case
  - **/rushhour/visualisation**: bevat de code voor visualisatie
- **/solutions**: bevat mappen met data dat is verzemeld tijdens de experimeneten

## Code runnen
In de main kan de code geruned worden. Door UserInterface() te runnen kan er gekozen worden welk board en welk algoritme. Vervolgends wordt er een visualisatie gemaakt van de stappen die het algoritme maakt. Ook is er een optie om een al bestaande file te kiezen uit solutions en die stappen te laten zien. Er kan bijvoorbeeld gekozen worden voor de file solutions/random_with_memory/botom_game1.csv. Deze file bevat de preciese stappen van het laagst gevonden aantal stappen.

## De algoritmes kort uitgelegd

Met verschillende soorten algoritmes is geprobeerd het rush hour spel op te lossen. Hieronder staat een korte beschrijving per algoritme. 

### 1. random_move.py
Het random move algoritme creert een baseline voor het vergelijken van de prestaties van andere algoritmes. Het random algoritme heeft geen 'inteligentie' en fungeert dus als basis. Het selecteerd een willekeurige auto en probeert deze in een willkeurige richting te bewegen met één stap per keer. 
Het algoritme gaat door totdat een oplossing is gevonden of een maximaal aantal iteraties is bereikt. 

Dit algoritme maakt geen gebruik van geheugen, waardoor het dezelfde staten opnieuw kan bezoeken en herhalende bewegingen kan maken.

### 2. random_with_memory.py
Het random_with_memory algoritme is een uitbreiding van het random_move algoritme en maakt gebruik van geheugen. Dit geheugen wordt gebruikt om bezochte bord staten op te slaan en te vergelijken. Wanneer een nieuwe zet leidt to een bordstaat die al eens eerder bezocht is, keert het algoritme terug naar deze eerdere staat. Hierdoor voorkom je herhaling.

### 4. comparing.py
Dit algoritme gaat opzoek naar overlappende en gelijke stappen tussen goede oplossingen.
1. Het algoritme genereert meerdere oplossingen doormiddel van een gelijksoortig algoritme van random_with_memory.py.
2. Vervolgens wordt er gezocht naar overlappingen binnen deze reeks oplossingen.
3. De overlappingen zouden een mogelijke eigenschap kunnen zijn van de ideale oplossingen en worden gebruikt om nieuwe, hopelijk kortere oplossingen te vinden.

### 2. BFS.py
Het breadth-first-search (BFS) algoritme zoek systematisch door de statespace van een rush hour spel. 
Breadth-first-search garandeert de korst mogelijke oplossing, maar kan erg geheugen intensief zijn waardoor spellen met een te grote statespace niet opgelost kunnen.

### 3. AStar.py
Het A\* algoritme gebruikt een heuristiek om gericht te zoeken naar de korst mogelijke oplossing. Inplaats van blind door de statespace te zoeken zoals een breadth-first-search, geeft A\* voorkeur aan bepaalde nodes/states die meer waarschijnlijk naar een oplossing leiden. 
Het algoritme maakt gebruik van een "blocking cars" heuristiek. Het algoritme bekijkt het aantal auto's die de rode auto blokkeren van de uitgang. 

Elke bord staat heeft een score f = g + h. g is de kosten die groeit per aantal gemaakte stappen. h is de heuristiek die het aantal auto's die de rode auto blokkeren berekend. Het algoritme geeft prioriteit aan de states met de kleinste waarde voor f. 

### 6. hillclimber.py
Dit algoritme implementeert een hillclimber aanpak. 
1. Het algoritme start met een willkeurige oplossing van het random_with_memory.py algoritme. 
2. Deze oplossing wordt vervolgens iteratief verbeterd
  * Er wordt een willekeurige positie binnen de huidige oplossing reeks gekozen.
  * vanaf dit punt word een nieuwe willkeurige oplossing gezocht met als doel een korter pad te vinden.
3. Als een korter pad wordt gevonden, wordt de beste oplossing bijgewerkt en verder iteratief verbeterd. 

Dit proces gaat door totdat een tijdslimiet wordt bereikt. 

Het algoritme probeert een oplossing lokaal te optimaliseren door een deel van de oplossing opnieuw door te lopen vanaf een willekeurig gekozen positie in de hoop een korter pad te vinden. 

## Auteurs
- Dinand Hulleman
- Bas van Daalen
- Anne Snijder
