# Load provider
def load_simulator(qc):
    print("start load simulator")
    from qiskit import transpile  # transpile은 여전히 유용합니다.
    from qiskit_aer import AerSimulator  # 로컬 시뮬레이션을 위해 AerSimulator 사용

    # Save account credentails.
    # IBM 토큰이 만료되었으므로, 로컬 시뮬레이션을 위해 AerSimulator를 사용합니다.
    # IBMProvider와 관련된 다음 줄들은 주석 처리됩니다.
    # from qiskit_ibm_provider import IBMProvider
    # from qiskit.tools.monitor import job_monitor
    # provider = IBMProvider()
    # backend = provider.get_backend("ibmq_qasm_simulator")

    aer_sim = AerSimulator()  # 로컬 시뮬레이션을 위한 AerSimulator 초기화
    # Transpile the circuit
    t_qc = transpile(
        qc, aer_sim, optimization_level=3
    )  # AerSimulator를 위한 트랜스파일
    # Submit a job.
    shots = 1024
    job = aer_sim.run(t_qc, shots=shots)  # AerSimulator에서 실행
    # Get results.
    print("complete load simulator(return job.result())")
    # Return results.
    return job.result()
