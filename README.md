# rush_hour

## Opzet
In requirements.txt staat de benodigde packages die gedownload moeten worden. Dit is te instaleren door:
```
pip install -r requirements.txt
```
## Experiment
In het algoritme run_experiment in rushhour/algoritms kunnen alle algoritmen gerund worden.
\
De gemaakte algoritmen worden op twee manieren vergeleken. Het algoritme random_move (de basislijn), random_with_memory en comparing worden op uitkomst vergeleken. Dit wordt gedaan met behulp van het algoritme save_outputs. De algoritmen verschillen niet in uitkomst, ongeacht of ze in een korte of lange periode worden opgelost, daarom worden ze alleen op uitkomst vergeleken.
\
Het algoritme hillclimber wordt in de tijd met zichzelf vergeleken, aangezien dit verschillende uitkomsten geeft tijdens verschillende runs en verschillende tijden.
\
De algoritmen BFS en Astar hebben slechts één uitkomst. Dit is precies dezelfde uitkomst. Aangezien de uitkomst niet anders is in verschillende tijdsduren, wordt dit niet vergeleken qua tijd. Wel kan de runtijd vergeleken worden. 
\
De verzamelde gegevens bevinden zich in de map solutions.
\
Het algoritme om de grafieken te maken met behulp van de gegevens bevindt zich in rushhour/visualisation/histograms.


