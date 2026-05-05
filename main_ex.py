from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit_runner import QuantumManager

# ==========================================
# 1. 실행 환경 셋업 (여기서 모드만 바꾸면 끝납니다)
# ==========================================
# 실제 장비 테스트 시 run_mode='real' 로 변경
# optimization_level을 명시적으로 변경할 수 있습니다. (기본값: simulator=1, real=3)
manager = QuantumManager(run_mode="simulator", optimization_level=2)

# ==========================================
# 2. 양자 회로 및 관측가능량 설계
# ==========================================
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()  # Sampler용 측정 추가

# Estimator용 관측가능량 (예: ZZ 파울리 연산자)
observable = SparsePauliOp(["ZZ"])

# ==========================================
# 3. 구동 및 결과 확인
# ==========================================
print("\n--- Sampler 결과 ---")
counts = manager.run(qc, primitive="sampler", shots=2000)
print(f"측정 결과: {counts}")

# Estimator는 measure_all()이 없는 순수 상태의 회로가 필요하므로 새로 정의
qc_est = QuantumCircuit(2)
qc_est.h(0)
qc_est.cx(0, 1)

print("\n--- Estimator 결과 ---")
expectation_values = manager.run(qc_est, primitive="estimator", observables=[observable], shots=2000)
print(f"기댓값: {expectation_values}")
