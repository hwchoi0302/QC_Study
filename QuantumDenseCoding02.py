# Simulating Quantum Dense Coding

# Importing moduels
from qiskit import QuantumCircuit, execute
from qiskit import IBMQ, transpile  # execute는 사용되지 않으므로 제거
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
import matplotlib.pylab as plt
import IPython.display as display

# Define function


def create_bell_pair():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return qc


def incode_message(qc, msg):
    if len(msg) != 2 or not set(msg).issubset({"0", "1"}):
        raise ValueError(f"message '{msg}' is invaild.")
    if msg[0] == "1":
        qc.x(0)
    if msg[1] == "1":
        qc.z(0)
    return qc


def decode_message(qc):
    qc.cx(0, 1)
    qc.h(0)
    return qc


# Make complete protocol

qc = create_bell_pair()
qc.barrier()

message = "10"
qc = incode_message(qc, message)
qc.barrier()

qc = decode_message(qc)

qc.measure_all()
print(qc.draw())

# Simulate with AerSimulator
sim = AerSimulator()
shots = 1024  # 일관성을 위해 shots 정의
job = sim.run(qc, shots=shots)

result = sim.run(qc).result()
counts = result.get_counts(qc)

print(counts)
plot_histogram(counts)
plt.show()
