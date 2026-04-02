# # Import
# from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
# from qiskit.visualization import plot_histogram, plot_bloch_multivector, array_to_latex
# from qiskit.circuit.library import Initialize
# from qiskit.result import marginal_counts
# from qiskit.quantum_info import random_statevector
# import matplotlib.pyplot as plt
# import numpy as np

# # Create random 1-qubit state
# psi = random_statevector(2)
# init_gate = Initialize(psi)
# init_gate.label = "init"
# inverse_init_gate = init_gate.gates_to_uncompute()

# # SETUP

# def create_bell_pair(qc, a, b):
#     qc.h(a)
#     qc.cx(a,b)

# def allice_gates(qc, psi, a):
#     qc.cx(psi,a)
#     qc.h(psi)

# def measure_and_send(qc, a, b):
#     qc.barrier()
#     qc.measure(a,0)
#     qc.measure(b,1)

# def bob_gates(qc, qubit, crz, crx):
#     qc.x(qubit).c_if(crx, 1) # Apply gates if the registers are in the state '1'
#     qc.z(qubit).c_if(crz, 1)

# def new_bob_gates(qc, psi, a, b):
#     qc.cx(a,b)
#     qc.cz(psi,b)


# # Create Circuit
# qc = QuantumCircuit(3, 1)
# qc.append(init_gate,[0])
# qc.barrier()
# create_bell_pair(qc,1,2)
# qc.barrier()
# allice_gates(qc,0,1)
# qc.barrier()
# new_bob_gates(qc, 0, 1, 2)
# qc.append(inverse_init_gate, [2])
# qc.measure(2,0)
# qc.draw('mpl')
# # plt.show()

# from Load_simulator import load_simulator
# exp_result = load_simulator(qc)

# exp_counts = exp_result.get_counts(qc)
# print(exp_counts)
# plot_histogram(exp_counts)
# plt.show()

## Simulator에서 실행시키는 QT
# Import
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.visualization import plot_histogram, plot_bloch_multivector, array_to_latex
from qiskit.circuit.library import Initialize
from qiskit.result import marginal_counts
from qiskit.quantum_info import random_statevector
import matplotlib.pyplot as plt
import numpy as np

# Create random 1-qubit state
# psi = random_statevector(2)
# init_gate = Initialize(psi)
# init_gate.label = "init"
# inverse_init_gate = init_gate.gates_to_uncompute()


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


def new_bob_gates(qc, psi, a, b):
    qc.cx(a, b)
    qc.cz(psi, b)


# Create Circuit
psi = random_statevector(2)  # 임의의 초기 상태 생성
init_gate = Initialize(psi)
init_gate.label = "init"
inverse_init_gate = init_gate.gates_to_uncompute()

qc = QuantumCircuit(3, 1)  # 3 큐비트, 1 고전 비트
qc.append(init_gate, [0])  # 텔레포트할 초기 상태를 0번 큐비트에 적용
qc.barrier()
create_bell_pair(qc, 1, 2)
qc.barrier()
allice_gates(qc, 0, 1)
qc.barrier()
new_bob_gates(qc, 0, 1, 2)
qc.append(
    inverse_init_gate, [2]
)  # 텔레포트된 상태가 올바른지 확인하기 위해 역변환 적용
qc.measure(2, 0)
qc.draw("mpl")
# plt.show()

# AerSimulator로 시뮬레이션
from qiskit_aer import AerSimulator

aer_sim = AerSimulator()
shots = 1024
t_qc = transpile(qc, aer_sim)
job = aer_sim.run(t_qc, shots=shots)
exp_result = job.result()

exp_counts = exp_result.get_counts(t_qc)
print(exp_counts)
plot_histogram(exp_counts)
plt.show()
