# flappy_bird_using_genetic_algo
Implementation of a self learning flappy bird using Genetic Algorithm.

The flappy bird game is the easiest game that could be automated.
<br>
The Game :
<br>
(i)The bird has to escape touching the never ending stream of vertical pipes (top and bottom) by flying through the gap between the two pipes.
<br>
(ii)The user control to the bird is that he could instruct the bird to flap by pressing the space key (generally).
<br>
(iii)whenever user presses the key the bird flaps and moves upward by a constant velocity ( which is unknown and the user has to percieve it through playing multiple times).
<br>
(iv)Another constarint here is the gravity. If we know the speed with which the bird flies up , we could work out the physics of the game and make it flap exactly whenever needed to and win the game.
<br>
(v)But , what if we used another way of playing the game instead of solving those cumbersome physics equations with some unknowns that are to be calculated using some experiments.
<br>
(vi)What if we use a neural network that decides whether to flap or not.
<br>
