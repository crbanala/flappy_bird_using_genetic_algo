The power of a simple neural network as a universal approximator can be demonstrated using this simple game of FlappyBird. 
The neural net here has to decide whether to flap or not at a particular instance using just the following known params:
  1.The distance from the next set of pipes
  2.The vertical height of the bird (or agent) from the ground
  3.The vertical speed it currently has.
  4.The heights of both lower and upper pipes (i.e the height where the gap is).

One can easily solve this problem using simple physics by 
  
  
  
  
  
References:
  Most of the code for pygame graphics and image data was taken from https://github.com/sourabhv/FlappyBirdClone.git.
  
