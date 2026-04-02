from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np


def qft_circuit(n_qubits):
    """
    주어진 큐비트 수에 대한 양자 푸리에 변환(QFT) 회로를 생성합니다.

    Args:
        n_qubits (int): QFT를 적용할 큐비트의 수.

    Returns:
        QuantumCircuit: QFT 연산을 수행하는 QuantumCircuit 객체.
    """
    qc = QuantumCircuit(n_qubits)

    # QFT 게이트 적용
    for i in range(n_qubits):
        qc.h(i)  # 각 큐비트에 Hadamard 게이트 적용
        for j in range(i + 1, n_qubits):
            # 제어 위상 회전(Controlled-Phase Rotation) 적용
            # cp(theta, control_qubit, target_qubit)
            # 각도는 pi / 2^(j - i)
            qc.cp(np.pi / (2 ** (j - i)), j, i)

    # 큐비트 순서를 뒤집기 위한 스왑 게이트 적용 (QFT 출력은 역순으로 나옴)
    for i in range(n_qubits // 2):
        qc.swap(i, n_qubits - 1 - i)

    return qc


if __name__ == "__main__":
    # QFT를 적용할 큐비트 수 설정
    num_qubits = 3

    # 큐비트 수와 동일한 수의 고전 비트를 가진 양자 회로 생성
    full_qc = QuantumCircuit(num_qubits, num_qubits)

    # 초기 상태 준비 (예: |001> 상태를 만들기 위해 첫 번째 큐비트에 X 게이트 적용)
    # Qiskit에서 q[0]은 측정 결과 문자열의 가장 오른쪽 비트(LSB)에 해당합니다.
    full_qc.x(0)
    # 다른 초기 상태를 원하면 이 부분을 수정하세요.
    # 예: 모든 큐비트를 중첩 상태로 만들려면:
    # for i in range(num_qubits):
    #     full_qc.h(i)

    full_qc.barrier()

    # QFT 회로를 생성하고 전체 회로에 추가
    qft_op = qft_circuit(num_qubits)
    full_qc.append(qft_op, range(num_qubits))

    full_qc.barrier()

    # 모든 큐비트 측정
    full_qc.measure(range(num_qubits), range(num_qubits))

    # 회로 그리기 및 출력
    print("--- QFT Circuit ---")
    # 텍스트 출력은 복잡할 수 있으므로, 시각적인 'mpl' 출력을 사용합니다.
    full_qc.draw("mpl")
    plt.show()

    # AerSimulator를 사용하여 시뮬레이션 실행 전에 회로를 트랜스파일합니다.
    aer_sim = AerSimulator()
    shots = 1024  # 시뮬레이션 샷 수
    t_full_qc = transpile(full_qc, aer_sim)  # AerSimulator에 맞게 회로 트랜스파일
    job = aer_sim.run(t_full_qc, shots=shots)  # 트랜스파일된 회로 실행
    result = job.result()
    counts = result.get_counts(full_qc)

    # 측정 결과 출력
    print(f"\n--- Measurement counts for {num_qubits}-qubit QFT ---")
    print(counts)

    # 측정 결과 히스토그램 그리기
    plot_histogram(counts)
    plt.show()
