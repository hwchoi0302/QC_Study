import numpy as np

ket0 = np.array([[1], [0]])
ket1 = np.array([[0], [1]])

print(ket0 / 2 + ket1 / 2)

M1 = np.array([[1, 1], [0, 0]])
M2 = np.array([[1, 0], [0, 1]])
M = M1 / 2 + M2 / 2
print(M)


print(np.matmul(M1, ket1))
print(np.matmul(M1, M2))
print(np.matmul(M, M))

from qiskit.quantum_info import Statevector
from numpy import sqrt

u = Statevector([1 / sqrt(2), 1 / sqrt(2)])
v = Statevector([(1 + 2.0j) / 3, -2 / 3])
w = Statevector([1 / 3, 2 / 3])

# display(u.draw("text"))
# display(u.draw("latex"))
print(u.draw("latex_source"))

outcome, state = v.measure()
print(f"Measured: {outcome}\nPost-measurement state:")
# display(state.draw("latex"))

from qiskit.visualization import plot_histogram

statistics = v.sample_counts(1000)
plot_histogram(statistics)

import matplotlib.pyplot as plt  # matplotlib.pyplot을 직접 임포트하는 것이 일반적입니다.

plt.show()  # plot_histogram이 생성한 그래프를 화면에 표시합니다.


zero = Statevector.from_label("0")
one = Statevector.from_label("1")
psi = zero.tensor(one)  # Tensor product
# display(psi.draw("latex"))
