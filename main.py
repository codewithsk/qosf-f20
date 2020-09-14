import pennylane as qml
from pennylane import numpy as np

NUM_LAYERS = 2
NUM_QUBITS = 4
NUM_STEPS = 100

qpu = qml.device("default.qubit", wires=4)

psi = np.random.rand(2**NUM_QUBITS)
while sum(psi) !=1:
    psi = np.random.rand(2**NUM_QUBITS)
    psi = np.exp(psi) / sum(np.exp(psi))

@qml.qnode(qpu)
def circuit(params, num_layers=NUM_LAYERS, num_qubits=NUM_QUBITS):

    for layer in range(num_layers):
        for wire in range(num_qubits):
            qml.RZ(params[layer * num_qubits + wire], wires=wire)

            
        for control in range(num_qubits-1):
            for target in range(control+1, num_qubits):
                qml.CZ(wires=[control,target]) 
        
        for wire in range(num_qubits):
            qml.RX(params[layer * num_qubits + wire], wires=wire)

    return qml.probs(np.arange(num_qubits))

def cost(x):
    return np.sum(np.square(circuit(x) - psi))


if __name__ == "__main__":
    weights = np.random.rand(NUM_QUBITS * NUM_LAYERS)
    print(circuit(weights))
    print(circuit.draw())

    print(cost(weights))

    opt = qml.GradientDescentOptimizer(stepsize=0.4)
    steps = NUM_STEPS
    params = weights


    for i in range(steps):
        params = opt.step(cost, params)

        if (i+1) % 5 == 0:
            print("Cost after step {:5d}: {: .7f}".format(i + 1, cost(params)))

    print("Optimized rotation angles: {}".format(params))
    print("Optimal cost: {}".format(cost(params)))
