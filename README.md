## Power Of a Neural Net

The power of a simple neural network as a <b>universal approximator</b> can be demonstrated using this simple game of FlappyBird.


The neural net here has to decide whether to flap or not at a particular instance using just the following known params:



  1. The horizantal distance from the next set of pipes


  2. The vertical height of the bird (or agent) from the ground


  3. The vertical speed it currently has.


  4. The heights of both lower and upper pipes (i.e the height where the gap is).



One can easily solve this problem using simple physics by taking into the consideration of all the constraints posed by the game (like gravity in this case etc..)


But can a neural net learn this equation using the weights ??


(or better)


Can the neural net capture the functional mapping of input of 4 params to boolean using just  4 * 3 + 3* 1 = 15   weights ??




The solution of the optimal weights is found using a special search paradigm called <b>Genetic Algorithms</b>.


  More on it : <href>https://towardsdatascience.com/introduction-to-genetic-algorithms-including-example-code-e396e98d8bf3</href>


# Training Process:

<video width="640" height="360" src="flappy_training.mkv"> </video>



# References:
 Most of the code and image data for pygame graphics including code for controls is taken from :
 
 
 <href>https://github.com/sourabhv/FlappyBirdClone.git</href>.But most of it is restructured for better understanding.
