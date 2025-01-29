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
Voor het uitvoeren van een experiment run je de bijbehorende functie van run_experiments.py in main.py. Let goed op welke input argumenten nodig zijn. Zorg ervoor dat UserInterface() is uitgecommend, deze heb je niet nodig voor het uitvoeren van experimenten.
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
In de main kan de code geruned worden. Door UserInterface() te runnen kan er gekozen worden welk board en welk algoritme. Vervolgends wordt er een visualisatie gemaakt van de stappen die het algoritme maakt. Ook is er een optie om een al bestaande file te kiezen uit solutions en die stappen te laten zien. Er kan bijvoorbeeld gekozen worden voor de file solutions/random_with_memory/botom_game1.csv. Deze file bevat de preciese stappen van de laagst gevonden aantal stappen.

## Auteurs
- Dinand Hulleman
- Bas van Daalen
- Anne Snijder
