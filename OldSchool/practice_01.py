"""
# 1. 데코레이터 정의 (포장지)
def circuit_alert(func):
    def wrapper():
        print("⚠️ 알림: 양자 회로 작업을 시작합니다.")
        func()  # 원래 함수 실행
        print("✅ 알림: 작업이 무사히 완료되었습니다!")

    return wrapper


# 2. 데코레이터 적용 (@ 사용)
@circuit_alert
def my_quantum_task():
    print("  -> 큐비트를 조작하는 중...")


# 3. 함수 실행
my_quantum_task()
"""

"""
# 회로 생성
from qiskit import QuantumCircuit

# 2개의 큐비트를 가진 회로 객체 생성
qc = QuantumCircuit(2)
"""

# from qiskit import QuantumCircuit
# from qiskit.primitives import StatevectorSampler  # sampler and estimater
# from qiskit.visualization import plot_histogram
# import matplotlib.pyplot as plt

# # 1. 회로 조립하기
# qc = QuantumCircuit(2)
# qc.h(0)
# qc.cx(0, 1)
# qc.measure_all()  # 회로의 모든 큐비트를 측정하여 고전 비트에 저장

# # 2. 시뮬레이터로 회로 실행하기
# sampler = StatevectorSampler()
# job = sampler.run(qc)
# result = job.result()

# # 3. 측정된 확률 데이터 가져오기
# prob_dist = result.quasi_dists[0].binary_probabilities()

# # 4. 히스토그램으로 시각화하기
# plot_histogram(prob_dist)
# plt.show()

from qiskit import __version__

print(__version__)
