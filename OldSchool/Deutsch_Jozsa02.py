# Generalised Circuits

from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np


def dj_oracle(case, n):
    from qiskit_aer import (
        AerSimulator,
    )  # Moved import here to avoid circular dependency if Deutsch_Jozsa03 imports this

    oracle_qc = QuantumCircuit(n + 1)
    if case == "constant":
        output = np.random.randint(2)
        if output == 1:
            oracle_qc.x(n)

    if case == "balanced":
        b = np.random.randint(0, 2**n)
        b_str = format(b, "0" + str(n) + "b")
        for qubit in range(n):
            if b_str[qubit] == "1":
                oracle_qc.x(qubit)
        for qubit in range(n):
            oracle_qc.cx(qubit, n)
        for qubit in range(n):
            if b_str[qubit] == "1":
                oracle_qc.x(qubit)

    oracle_gate = oracle_qc.to_gate()
    oracle_qc.name = "Oracle"
    return oracle_gate


def dj_algorithm(oracle, n):
    dj_circuit = QuantumCircuit(n + 1, n)
    for qubit in range(n):
        dj_circuit.h(qubit)
    dj_circuit.x(n)
    dj_circuit.h(n)
    dj_circuit.append(oracle, range(n + 1))
    for qubit in range(n):
        dj_circuit.h(qubit)

    dj_circuit.measure(range(n), range(n))  # 모든 데이터 큐비트를 해당 고전 비트에 측정

    return dj_circuit


def main():
    n = 4
    from qiskit_aer import AerSimulator  # Moved import here for main function

    oracle_gate = dj_oracle("balanced", n)
    # oracle_gate = dj_oracle('constant',n)
    dj_circuit = dj_algorithm(oracle_gate, n)
    dj_circuit.draw("mpl")
    plt.show()

    # Simulation
    aer_sim = AerSimulator()
    t_dj_circuit = transpile(dj_circuit, aer_sim)
    results = aer_sim.run(t_dj_circuit).result()
    answer = results.get_counts()

    if "1" * n in answer:
        print("function is balanced!")
    else:
        print("function is constant!")


if __name__ == "__main__":
    main()
