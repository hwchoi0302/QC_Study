from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator  # AerSimulator 임포트 추가
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt


def Simon_Oracle(b):
    n = len(b)
    c = b[::-1]
    b_j = 0
    qc = QuantumCircuit(n * 2)
    # Make |x>|x>
    for qubit in range(n):
        qc.cx(qubit, qubit + n)
    # Find least b_j
    for i in range(n):
        if c[i] == "1":
            b_j = i
            break
    # Make |x>|x+b>
    for qubit in range(n):
        if c[qubit] == "1":
            qc.cx(b_j, qubit + n)
    return qc


# qc = Simon_Oracle('1101010')
# qc.draw('mpl')
# plt.show()


def Simon_Algorithm(b):
    n = len(b)
    qc = QuantumCircuit(n * 2, n)
    # for qubit in range(n):
    #     qc.h(qubit)
    qc.h(range(n))
    qc.barrier()
    qc = qc.compose(Simon_Oracle(b))
    qc.barrier()
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc


# qc = Simon_Algorithm('110')
# qc.draw('mpl')
# plt.show()

b = "110"
shots = 1024  # 일관성을 위해 shots 정의
simon_circuit = Simon_Algorithm(b)

# AerSimulator로 시뮬레이션
aer_sim = AerSimulator()
job = aer_sim.run(simon_circuit, shots=shots)
results = job.result()
counts = results.get_counts()

print(counts)
plot_histogram(counts)  # plot_histogram 주석 해제
plt.show()  # plt.show() 추가

# # Calculate the dot product of the results
# def bdotz(b, z):
#     accum = 0
#     for i in range(len(b)):
#         accum += int(b[i]) * int(z[i])
#     return (accum % 2)

# for z in device_counts:
#     print( '{}.{} = {} (mod 2)'.format(b, z, bdotz(b,z)) )
