from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, EstimatorV2
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import (
    SamplerV2 as RuntimeSampler,
    EstimatorV2 as RuntimeEstimator,
)
from qiskit.primitives import BackendSamplerV2, BackendEstimatorV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


class QuantumManager:
    """
    시뮬레이터와 실제 양자 컴퓨터 간의 전환을 관리하고,
    Sampler와 Estimator 실행을 전담하는 통합 매니저 클래스입니다.
    """

    def __init__(
        self, run_mode="simulator", backend_name=None, optimization_level=None
    ):
        self.run_mode = run_mode

        # 1. 백엔드 초기화 (객체 생성 시 1회만 수행)
        if self.run_mode == "simulator":
            self.backend = AerSimulator()
            if optimization_level is None:
                optimization_level = (
                    1  # 시뮬레이터는 최적화 레벨을 낮춰 클래식 연산 자원 절약
                )
            self._sampler_class = BackendSamplerV2
            self._estimator_class = BackendEstimatorV2
        elif self.run_mode == "real":
            self.service = QiskitRuntimeService()
            if backend_name:
                self.backend = self.service.backend(backend_name)
            else:
                self.backend = self.service.least_busy(
                    operational=True, simulator=False
                )
            if optimization_level is None:
                optimization_level = (
                    3  # 실제 장비는 노이즈 최소화를 위해 최고 수준의 최적화 적용
                )
            self._sampler_class = RuntimeSampler
            self._estimator_class = RuntimeEstimator
        else:
            raise ValueError("run_mode는 'simulator' 또는 'real' 이어야 합니다.")

        print(
            f"[{self.run_mode.upper()} MODE] 연결된 백엔드: {self.backend.name} (Opt Level: {optimization_level})"
        )

        # 2. Pass Manager 초기화 (ISA 변환용)
        self.pm = generate_preset_pass_manager(
            backend=self.backend, optimization_level=optimization_level
        )

    def run(self, qc, primitive="sampler", observables=None, shots=1024):
        """
        선택된 primitive(Sampler 또는 Estimator)를 사용하여 회로를 실행합니다.

        Args:
            qc: 실행할 양자 회로
            primitive: 'sampler' 또는 'estimator' (기본값: 'sampler')
            observables: Estimator 실행 시 필요한 관측가능량 (primitive='estimator'일 때 필수)
            shots: 실행 샷 수 (기본값: 1024)
        """
        # 하드웨어 토폴로지에 맞게 회로 변환 (ISA 변환)
        isa_qc = self.pm.run(qc)

        if primitive == "sampler":
            if self.run_mode == "real":
                sampler = self._sampler_class(mode=self.backend)
            else:
                sampler = self._sampler_class(backend=self.backend)

            sampler.options.default_shots = shots
            # SamplerV2는 run 시 튜플 리스트 형태를 받습니다.
            job = sampler.run([(isa_qc,)])
            result = job.result()[0]
            # 고전적인 딕셔너리 형태의 결과(Counts) 반환
            return result.data.meas.get_counts()

        elif primitive == "estimator":
            if observables is None:
                raise ValueError(
                    "estimator를 사용할 경우 observables를 제공해야 합니다."
                )

            # 관측가능량(Observables)도 회로의 물리적 큐비트 레이아웃에 맞게 변환해야 함
            isa_observables = [obs.apply_layout(isa_qc.layout) for obs in observables]

            if self.run_mode == "real":
                estimator = self._estimator_class(mode=self.backend)
            else:
                estimator = self._estimator_class(backend=self.backend)

            estimator.options.default_shots = shots
            job = estimator.run([(isa_qc, isa_observables)])
            result = job.result()[0]
            # 기댓값 데이터 반환
            return result.data.evs

        else:
            raise ValueError(
                f"지원하지 않는 primitive 입니다: {primitive}. 'sampler' 또는 'estimator'를 사용하세요."
            )
