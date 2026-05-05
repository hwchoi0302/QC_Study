# Import
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram, plot_bloch_multivector, array_to_latex
from qiskit import transpile
from qiskit.extensions import Initialize
from qiskit.result import marginal_counts
from qiskit.quantum_info import random_statevector
import matplotlib.pyplot as plt
import numpy as np

# Create random 1-qubit state
psi = random_statevector(2)
init_gate = Initialize(psi)
init_gate.label = "init"

# SETUP


def create_bell_pair(qc, a, b):
    qc.h(a)
    qc.cx(a, b)


def allice_gates(qc, psi, a):
    qc.cx(psi, a)
    qc.h(psi)


def measure_and_send(qc, a, b):
    qc.barrier()
    qc.measure(a, 0)
    qc.measure(b, 1)


def bob_gates(qc, qubit, crz, crx):
    qc.x(qubit).c_if(crx, 1)  # Apply gates if the registers are in the state '1'
    qc.z(qubit).c_if(crz, 1)


# Create Circuit
qr = QuantumRegister(3, name="q")
crz = ClassicalRegister(1, name="crz")
crx = ClassicalRegister(1, name="crx")
teleportation_circuit = QuantumCircuit(qr, crz, crx)
teleportation_circuit.append(init_gate, [0])
teleportation_circuit.barrier()

create_bell_pair(teleportation_circuit, 1, 2)
teleportation_circuit.barrier()
allice_gates(teleportation_circuit, 0, 1)
measure_and_send(teleportation_circuit, 0, 1)
bob_gates(teleportation_circuit, 2, crz, crx)
# print(teleportation_circuit.draw())

# Simulate
inverse_init_gate = init_gate.gates_to_uncompute()
teleportation_circuit.append(inverse_init_gate, [2])

cr_result = ClassicalRegister(1)
teleportation_circuit.add_register(cr_result)
teleportation_circuit.measure(2, 2)
teleportation_circuit.draw("mpl")
plt.show()

sim = AerSimulator()
t_qc = transpile(teleportation_circuit, sim)
t_qc.save_statevector()
counts = sim.run(t_qc).result().get_counts()
# print(counts)
qubit_counts = [marginal_counts(counts, [qubit]) for qubit in range(3)]
plot_histogram(qubit_counts)
plt.show()
