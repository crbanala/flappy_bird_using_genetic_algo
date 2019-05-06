from numpy import exp, array, random, dot
import numpy as np

class NeuronLayer():
    def __init__(self, number_of_neurons=0, number_of_inputs_per_neuron=0, weights=None):
        if weights is None:
            self.synaptic_weights = 2 * random.random((number_of_inputs_per_neuron, number_of_neurons)) - 1
        else:
            self.synaptic_weights = weights

    def copy_weights(self, weights):
        self.synaptic_weights = weights


class NeuralNetwork():
    def __init__(self, input_nodes=None, hidden_nodes=None, output_nodes=None, layer1=None, layer2=None):
        if layer1 is None:
            self.layer1 = NeuronLayer(hidden_nodes, input_nodes)
            self.layer2 = NeuronLayer(output_nodes, hidden_nodes)
        else:
            self.layer1 = layer1
            self.layer2 = layer2

    def __sigmoid(self, x):
        return 1 / (1 + exp(-x))

    def __sigmoid_derivative(self, x):
        return x * (1 - x)



    def think(self, inputs):
        output_from_layer1 = self.__sigmoid(dot(inputs, self.layer1.synaptic_weights))
        output_from_layer2 = self.__sigmoid(dot(output_from_layer1, self.layer2.synaptic_weights))
        return output_from_layer1, output_from_layer2

    def print_weights(self):
        print("    Layer 1 (4 neurons, each with 3 inputs): ")
        print(self.layer1.synaptic_weights)
        print("    Layer 2 (1 neuron, with 4 inputs):")
        print(self.layer2.synaptic_weights)

    # functions needed for genetic algorithms
    def mutate(self, rate):
        def mutate(val):
            if (random.random(1)[0] < rate):
                return 2 * random.random(1)[0] - 1
            else:
                return val

        vfunc = np.vectorize(mutate)
        new_layer1 = NeuronLayer(weights=vfunc(self.layer1.synaptic_weights))
        new_layer2 = NeuronLayer(weights=vfunc(self.layer2.synaptic_weights))
        return NeuralNetwork(layer1=new_layer1, layer2=new_layer2)

    def copy(self):
        new_layer1 = NeuronLayer(weights=(self.layer1.synaptic_weights))
        new_layer2 = NeuronLayer(weights=(self.layer2.synaptic_weights))
        return NeuralNetwork(layer1=new_layer1, layer2=new_layer2)



    def train(self, training_set_inputs, training_set_outputs, number_of_training_iterations):
        for iteration in range(number_of_training_iterations):
            # Pass the training set through our neural network
            output_from_layer_1, output_from_layer_2 = self.think(training_set_inputs)
            layer2_error = training_set_outputs - output_from_layer_2
            layer2_delta = layer2_error * self.__sigmoid_derivative(output_from_layer_2)
            layer1_error = layer2_delta.dot(self.layer2.synaptic_weights.T)
            layer1_delta = layer1_error * self.__sigmoid_derivative(output_from_layer_1)
            layer1_adjustment = training_set_inputs.T.dot(layer1_delta)
            layer2_adjustment = output_from_layer_1.T.dot(layer2_delta)
            self.layer1.synaptic_weights += layer1_adjustment
            self.layer2.synaptic_weights += layer2_adjustment

if __name__ == "__main__":
    random.seed(1)

    neural_network = NeuralNetwork(input_nodes=3, hidden_nodes=4, output_nodes=1)
    print("Stage 1) Random starting synaptic weights: ")
    neural_network.print_weights()
    training_set_inputs = array([[0, 0, 1], [0, 1, 1], [1, 0, 1], [0, 1, 0], [1, 0, 0], [1, 1, 1], [0, 0, 0]])
    training_set_outputs = array([[0, 1, 1, 1, 1, 0, 0]]).T
    neural_network.train(training_set_inputs, training_set_outputs, 60000)

    print("Stage 2) New synaptic weights after training: ")
    neural_network.print_weights()
    print("Stage 3) Considering a new situation [1, 1, 0] -> ?: ")
    hidden_state, output = neural_network.think(array([1, 1, 0]))
    print(output)

    mutated = neural_network.mutate(0.8)
    mutated.print_weights()
    copied = neural_network.copy()
    copied.print_weights()
