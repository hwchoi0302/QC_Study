from qiskit_ibm_runtime import QiskitRuntimeService

try:
    # 1. 저장된 자격 증명을 사용하여 서비스 불러오기 (인자 입력 안 함)
    service = QiskitRuntimeService()
    print("✅ 성공적으로 IBM Cloud 서비스에 연결되었습니다!\n")

    # 2. 학교 CRN을 통해 접근 가능한 백엔드(양자 장치 및 시뮬레이터) 목록 가져오기
    backends = service.backends()
    print(f"사용 가능한 백엔드 총 {len(backends)}개 발견:\n")

    # 3. 백엔드 이름과 큐비트 수 출력
    for backend in backends:
        print(f"- 이름: {backend.name} (큐비트: {backend.num_qubits}개)")

except Exception as e:
    print(
        "❌ 연결에 실패했습니다. 입력한 API 키나 CRN, 혹은 네트워크 상태를 확인해 주세요."
    )
    print(f"에러 상세 내용: {e}")
