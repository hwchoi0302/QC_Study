# Quantum Dense Coding in Real Computer

# Importing moduels
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator  # execute는 사용되지 않으므로 제거
from qiskit.visualization import plot_histogram
import matplotlib.pylab as plt

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
aer_sim = AerSimulator()  # execute는 사용되지 않으므로 제거
shots = 1024
job = aer_sim.run(qc, shots=shots)
result = job.result()
counts = result.get_counts(qc)

print(counts)
plot_histogram(counts)
plt.show()

# IBM Quantum 실제 장치 또는 클라우드 시뮬레이터에서 실행하기 위한 다음 섹션은
# 사용자 요청에 따라 토큰 문제를 피하고 로컬 시뮬레이션에 집중하기 위해 주석 처리됩니다.
# IBM Quantum에서 실행하려면 IBM Quantum 계정이 있는지 확인하고
# 다음 줄들의 주석을 해제하고 구성하십시오.
# from qiskit import IBMQ, transpile
# from qiskit.providers.ibmq import least_busy
# from qiskit_ibm_provider import IBMProvider
# from qiskit.tools.monitor import job_monitor
# provider = IBMProvider()
# backend = provider.get_backend("simulator_statevector") # 또는 실제 장치
# t_qc = transpile(qc, backend, optimization_level=3)
# job = backend.run(t_qc, shots=shots)
# job_monitor(job)
# result_ibmq = job.result()
# plot_histogram(result_ibmq.get_counts(qc))
# plt.show()
