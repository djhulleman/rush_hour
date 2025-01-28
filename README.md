# rush_hour

## Opzet
In requirements.txt staat de benodigde packages die gedownload moeten worden. Dit is te instaleren door:
```
pip install -r requirements.txt
```
## Experiment
In het algoritme **run_experiments.py** staan alle functies voor het uitvoeren van de experimenten op algorithmes. Voor ieder algorithme is een aparte functie geschreven die het experiment uitvoerd. Ieder functie heeft een eigen **docstring** waarin de werking van het algorimte/experiment staat uitgelegd. 
\
\
Voor het uitvoeren van een experiment run je de bijbehorende functie van run_experiments.py in main.py. Let goed op welke input argumenten nodig zijn. Zorg ervoor dat visualize_and_solve(board, memory) is uitgecommend, deze heb je niet nodig voor het uitvoeren van experimenten.
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
1. De auto's worden verschoven op 2 manieren; met gebruik van 1 (links, omhoog) en 2 (rechts, omlaag) en met gebruik van -1 (links, omhoog) en 1 (rechts, omlaag). Dit kan verwarrend overkomen maar door een misverstand in het er zo uitgekomen. Dit levert geen probleem op bij het runnen van de code.
2. Data kan geexporteerd worden naar verschillende plekken. In de code kan gezien worden waar naartoe en wat de naam is. Als export_moves() opgeroepen wordt zonder argument erin wordt de data geexporteerd als output.csv in dezelfde map als het algortime staat waarin het gerund wordt. Als er wel een naam neem wordt gegeven of pad, zal dat gevolgt worden.


