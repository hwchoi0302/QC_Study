# Importing

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np

# Oracle
n = 3
## constant oracle
const_oracle = QuantumCircuit(n + 1)

output = np.random.randint(2)
if output == 1:
    const_oracle.x(n)

# const_oracle.draw("mpl")
# plt.show()

## balanced oracle
balanced_oracle = QuantumCircuit(n + 1)
b_str = "101"

for qubit in range(len(b_str)):
    if b_str[qubit] == "1":
        balanced_oracle.x(qubit)

balanced_oracle.barrier()

for qubit in range(n):
    balanced_oracle.cx(qubit, n)

balanced_oracle.barrier()

for qubit in range(len(b_str)):
    if b_str[qubit] == "1":
        balanced_oracle.x(qubit)

# balanced_oracle.draw("mpl")
# plt.show()

# Deutsch-Jozsa Algorithm
dj_circuit = QuantumCircuit(n + 1, n)
for qubit in range(n):
    dj_circuit.h(qubit)
dj_circuit.x(n)
dj_circuit.h(n)
dj_circuit.barrier()
dj_circuit = dj_circuit.compose(balanced_oracle)  # Add Balanced Oracle
# dj_circuit = dj_circuit.compose(const_oracle) # Add Constant Oracle
dj_circuit.barrier()
for qubit in range(n):
    dj_circuit.h(qubit)

dj_circuit.measure(range(n), range(n))  # 모든 데이터 큐비트를 해당 고전 비트에 측정

dj_circuit.draw("mpl")
plt.show()


# Simulate
aer_sim = AerSimulator()
results = aer_sim.run(dj_circuit).result()
answer = results.get_counts()

if "1" * n in answer:
    print("function is balanced!")
else:
    print("function is constant!")
plot_histogram(answer)
plt.show()
