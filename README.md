# rush_hour


## Experiment
The alogorithms created are compared in two ways. The algorithm random_move (the baseline), random_with_memory and comparing are compared in outcome. This is done using the algorithm save_outputs. These algorithms do not differ in outcome wether they are solved in a short of long period of time, that is why these are compared only by outcome. Save_output can be called in the main. 
\
The algorithm hillclimber will be compared to itself in time, this is done to run the algorithm a few hours and collect the data by calling the algorithm in main and timing the running time using start_time = time.time(), end_time = time.time() and execution_time = end_time - start_time.
The algorithms BFS and Astar only have one outcome.
\
The collected data is in the map solutions. 
\ 
The algorithm to create the plots using the data is in histograms within the map visulization.
