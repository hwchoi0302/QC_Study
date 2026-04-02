# Deutsch_Jozsa Algorithm in Real Computer

from Deutsch_Jozsa02 import dj_oracle, dj_algorithm
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit import transpile  # transpile for AerSimulator


n = 6
oracle_gate = dj_oracle("constant", n)
# oracle_gate = dj_oracle('constant',n)
dj_circuit = dj_algorithm(oracle_gate, n)

dj_circuit.draw("mpl")
plt.show()

# Simulate with AerSimulator
aer_sim = AerSimulator()
shots = 1024  # Consistent with other examples
t_dj_circuit = transpile(dj_circuit, aer_sim)  # Explicit transpilation for AerSimulator
job = aer_sim.run(t_dj_circuit, shots=shots)
result = job.result()
answer = result.get_counts()

if "1" * n in answer:
    print("function is balanced!")
else:
    print("function is constant!")
plot_histogram(answer)
plt.show()
