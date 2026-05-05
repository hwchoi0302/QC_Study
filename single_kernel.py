## Import data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Two mock data points, including category labels, as in training
small_data = [
    [-0.194, 0.114, -0.006, 0.301, -0.359, -0.088, -0.156, 0.342, -0.016, 0.143, 1],
    [-0.1, 0.002, 0.244, 0.127, -0.064, -0.086, 0.072, 0.043, -0.053, 0.02, -1],
]

# Data points with labels removed, for inner product
train_data = [small_data[0][:-1], small_data[1][:-1]]

## encode Z-feature map
# from qiskit.circuit.library import zz_feature_map
# fm = zz_feature_map(feature_dimension=np.shape(train_data)[1], entanglement='linear', reps=1)

from qiskit.circuit.library import z_feature_map

fm = z_feature_map(feature_dimension=np.shape(train_data)[1])

unitary1 = fm.assign_parameters(train_data[0])
unitary2 = fm.assign_parameters(train_data[1])

## Overlap circuit
from qiskit.circuit.library import unitary_overlap

overlap_circ = unitary_overlap(unitary1, unitary2)
overlap_circ.measure_all()

print("circuit depth = ", overlap_circ.decompose().depth())

# 터미널이나 서버 환경에서는 창이 뜨지 않을 수 있으므로 파일로 저장합니다.
fig_circ = overlap_circ.decompose().draw("mpl", scale=0.6, style="iqp")
fig_circ.savefig("circuit_draw.png")
print("-> 회로 도면이 'circuit_draw.png'로 저장되었습니다.")


# =====================================================================
# 1. 기존 시뮬레이션 및 IBM Runtime 코드 주석 처리 (Line 36 ~ 86)
# =====================================================================
'''
## Optimize circuit
# Import needed packages
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService

# Get the least busy backend
service = QiskitRuntimeService()
backend = service.least_busy(
    operational=True, simulator=False, min_num_qubits=fm.num_qubits
)
print(backend)

# Apply level 3 optimization to our overlap circuit
pm = generate_preset_pass_manager(optimization_level=3, backend=backend)
overlap_ibm = pm.run(overlap_circ)

print("circuit depth = ", overlap_ibm.decompose().depth())
overlap_ibm.decompose().depth(lambda instr: len(instr.qubits) > 1)

#Run this for a simulator
from qiskit.primitives import StatevectorSampler
from qiskit_ibm_runtime import Options, Session, Sampler

num_shots = 10000


#Evaluate the problem using state vector-based primitives from Qiskit
sampler = StatevectorSampler()
results = sampler.run([overlap_circ], shots=num_shots).result()
# .get_counts() returns counts associated with a state labeled by bit results such as |001101...01>.
counts_bit = results[0].data.meas.get_counts()
# .get_int_counts returns the same counts, but labeled by integer equivalent of the above bit string.
counts = results[0].data.meas.get_int_counts()

# Benchmarked on an Eagle processor, 7-11-24, took 4 sec.
# Import our runtime primitive
from qiskit_ibm_runtime import Session, SamplerV2 as Sampler

num_shots = 10000

# Use sampler and get the counts

sampler = Sampler(mode=backend)
results = sampler.run([overlap_ibm], shots=num_shots).result()
# .get_counts() returns counts associated with a state labeled by bit results such as |001101...01>.
counts_bit = results[0].data.meas.get_counts()
# .get_int_counts returns the same counts, but labeled by integer equivalent of the above bit string.
counts = results[0].data.meas.get_int_counts()
'''

# =====================================================================
# qiskit_runner.py를 이용한 구동
# =====================================================================
from qiskit_runner import QuantumManager

print("\n--- qiskit_runner 구동 시작 ---")
num_shots = 10000
# simulator 모드로 구동하며, 원하시는 경우 'real'로 변경 가능합니다.
manager = QuantumManager(run_mode="simulator", optimization_level=3)

# Sampler를 이용하여 counts 가져오기 (문자열 형태의 counts_bit 반환)
counts_bit = manager.run(overlap_circ, primitive="sampler", shots=num_shots)

# 시각화를 위해 정수형 키(int)를 가지는 counts 딕셔너리로 변환
counts = {int(k, 2): v for k, v in counts_bit.items()}
print("--- 구동 완료 ---\n")


# =====================================================================
# 2. Visualization (Line 89, 92, 110)
# =====================================================================

# [Line 89 대응] 단순히 연산만 하면 출력이 안되므로 print문 사용
prob_zero = counts.get(0, 0.0) / num_shots
print(f"상태 |0...0> 의 확률: {prob_zero:.4f}")

from qiskit.visualization import plot_distribution

# [Line 92 대응] plot_distribution 결과를 파일로 저장
fig_dist = plot_distribution(counts_bit)
fig_dist.savefig("plot_distribution.png")
print("-> 확률 분포 막대 그래프가 'plot_distribution.png'로 저장되었습니다.")

def visualize_counts(probs, num_qubits):
    """Visualize the outputs from the Qiskit Sampler primitive."""
    zero_prob = probs.get(0, 0.0)
    top_10 = dict(sorted(probs.items(), key=lambda item: item[1], reverse=True)[:10])
    top_10.update({0: zero_prob})
    by_key = dict(sorted(top_10.items(), key=lambda item: item[0]))
    xvals, yvals = list(zip(*by_key.items()))
    xvals = [bin(xval)[2:].zfill(num_qubits) for xval in xvals]
    
    plt.figure() # 새로운 그림판 생성
    plt.bar(xvals, yvals)
    plt.xticks(rotation=75)
    plt.title("Results of sampling")
    plt.xlabel("Measured bitstring")
    plt.ylabel("Counts")
    plt.tight_layout() # 라벨 짤림 방지
    
    # [Line 110 대응] 터미널 출력 환경을 위해 이미지 저장 방식으로 우회
    plt.savefig("visualize_counts.png")
    print("-> Top 10 시각화 결과가 'visualize_counts.png'로 저장되었습니다.")
    plt.show() # 원하신다면 주석 해제하여 사용할 수 있습니다.

visualize_counts(counts, overlap_circ.num_qubits)

