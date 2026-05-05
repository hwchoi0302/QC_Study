# Importing
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt


def Bernstein_vazirani_Circuit(secret_string):
    n = len(secret_string)

    qc = QuantumCircuit(n + 1, n)
    qc.h(range(n))  # 모든 데이터 큐비트에 H 게이트 적용
    qc.x(n)
    qc.h(n)
    qc.barrier()
    # Make oracle
    reverse_string = secret_string[::-1]
    for qubit in range(n):
        if reverse_string[qubit] == "1":
            qc.cx(qubit, n)

    qc.barrier()
    qc.h(range(n))  # 모든 데이터 큐비트에 H 게이트 적용

    qc.measure(range(n), range(n))  # 모든 데이터 큐비트를 해당 고전 비트에 측정
    return qc


# Aer sim
secret_string = "110"
qc = Bernstein_vazirani_Circuit(secret_string)
# You can uncomment the following two lines to draw the circuit
# qc.draw("mpl")
# plt.show()

# Run the simulation
aer_sim = AerSimulator()
shots = 1024
job = aer_sim.run(qc, shots=shots)
results = job.result()
answer = results.get_counts()

print(f"Counts for secret string {secret_string}: {answer}")


# 두 번째 시뮬레이션 (Load_simulator 대신 AerSimulator 사용)
print("\n--- Second Simulation with AerSimulator ---")
secret_string_aer = "1010"
qc_aer = Bernstein_vazirani_Circuit(secret_string_aer)

# AerSimulator를 사용하여 시뮬레이션 실행
aer_sim_second = AerSimulator()
job_aer = aer_sim_second.run(qc_aer, shots=shots)
results_aer = job_aer.result()
answer_aer = results_aer.get_counts()

print(f"Counts for secret string {secret_string_aer}: {answer_aer}")
most_frequent_string_aer = max(answer_aer, key=answer_aer.get)
print(
    f"Hidden binary string from AerSimulator for '{secret_string_aer}': {most_frequent_string_aer}"
)
