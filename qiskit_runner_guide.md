# Qiskit Runner 사용 가이드 (`qiskit_runner.py`)

`qiskit_runner.py`는 Qiskit V2 Primitives(SamplerV2, EstimatorV2)를 기반으로 양자 회로를 시뮬레이터 또는 실제 양자 하드웨어에서 쉽게 구동할 수 있도록 도와주는 `QuantumManager` 클래스를 제공합니다.

---

## 1. 초기화 (설정)

`QuantumManager`를 초기화할 때 실행 모드와 최적화 레벨을 선택할 수 있습니다.

```python
from qiskit_runner import QuantumManager

# 1. 시뮬레이터 모드 (기본값)
# 로컬 시뮬레이터를 사용하며 기본 최적화 레벨(optimization_level)은 1입니다.
manager_sim = QuantumManager(run_mode="simulator")

# 2. 실제 양자 컴퓨터 모드
# IBM Quantum 실제 하드웨어를 사용하며 기본 최적화 레벨은 3입니다.
# (사전에 IBM Quantum 계정 인증이 필요합니다.)
manager_real = QuantumManager(run_mode="real")

# 3. 최적화 레벨 수동 지정
# 사용자가 명시적으로 최적화 레벨(0~3)을 설정할 수 있습니다.
manager_custom = QuantumManager(run_mode="simulator", optimization_level=2)
```

> **참고**: `run_mode="real"` 사용 시 IBM Quantum 계정이 로컬 환경에 저장되어 있어야 합니다. (에러 발생 시 `QiskitRuntimeService.save_account(token="YOUR_TOKEN")`를 통해 인증을 진행해주세요.)

---

## 2. 회로 구동 (run 메서드)

새롭게 통합된 `run()` 메서드를 통해 Sampler(확률 분포 측정)와 Estimator(기댓값 측정)를 모두 실행할 수 있습니다.

```python
def run(self, qc, primitive="sampler", observables=None, shots=1024):
```

- `qc`: 실행할 양자 회로 (`QuantumCircuit` 객체)
- `primitive`: 구동할 방식 (`"sampler"` 또는 `"estimator"`)
- `observables`: Estimator 사용 시 필수인 관측가능량 리스트 (예: `SparsePauliOp`)
- `shots`: 구동할 샷(Shot) 수 (기본값: 1024)

---

## 3. 사용 예시

### 예시 A: Sampler 사용하기 (확률 분포 얻기)
Sampler는 회로의 측정 결과를 기반으로 상태의 확률 분포(Counts)를 반환합니다. 회로 끝에 반드시 측정(`measure`)이 포함되어 있어야 합니다.

```python
from qiskit import QuantumCircuit
from qiskit_runner import QuantumManager

# 1. 환경 설정
manager = QuantumManager(run_mode="simulator", optimization_level=1)

# 2. 양자 회로 생성 (측정 포함)
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all() # Sampler는 측정 구문이 반드시 필요함

# 3. Sampler 구동 및 결과 확인 (샷 수 지정 가능)
counts = manager.run(qc, primitive="sampler", shots=2000)
print(f"측정 결과 (Counts): {counts}")
# 출력 예시: {'00': 1015, '11': 985}
```

### 예시 B: Estimator 사용하기 (기댓값 얻기)
Estimator는 특정 관측가능량(Observable)에 대한 기댓값을 계산합니다. 회로에 측정 구문이 포함되지 않은 순수 상태(State)의 회로를 전달해야 합니다.

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit_runner import QuantumManager

# 1. 환경 설정
manager = QuantumManager(run_mode="simulator", optimization_level=2)

# 2. 양자 회로 생성 (측정 미포함)
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

# 3. 관측가능량(Observable) 정의
# 예: 2큐비트 시스템의 ZZ 파울리 연산자
observable = SparsePauliOp(["ZZ"])

# 4. Estimator 구동 및 결과 확인
expectation_values = manager.run(qc, primitive="estimator", observables=[observable], shots=2000)
print(f"기댓값 (Expectation Value): {expectation_values}")
# 출력 예시: [1.0]
```

---

## 4. 요약 및 주의사항

- **`primitive` 인자 주의**: `manager.run(qc, primitive="real")`과 같이 잘못된 이름을 넣으면 에러가 발생합니다. 반드시 `"sampler"` 또는 `"estimator"`를 사용하세요.
- **ISA 회로 자동 변환**: 매니저 내부에서 하드웨어 구조에 맞게 `pass_manager`를 통해 자동으로 회로 변환(Transpilation)을 수행해 주므로, 사용자는 추상적인 논리 회로만 넘겨주면 됩니다.
- **Estimator Observable 자동 레이아웃 적용**: `run()` 내부에서 회로 변환 시 변경된 큐비트 레이아웃에 맞춰 Observable 역시 자동으로 `apply_layout` 처리가 이루어집니다.
