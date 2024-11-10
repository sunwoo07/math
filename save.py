import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

# 변수와 함수 정의
x = sp.symbols('x')
f = (x - 5) * (x + 5) * (x + 3)

# SymPy로 함수의 1계, 2계 도함수 계산
f_prime = sp.diff(f, x)
f_double_prime = sp.diff(f_prime, x)

# y=0과의 교점 찾기
roots_f = sp.solve(f, x)
roots_f_prime = sp.solve(f_prime, x)
roots_f_double_prime = sp.solve(f_double_prime, x)

# 함수와 미분함수를 넘파이용 함수로 변환
f_lambdified = sp.lambdify(x, f, 'numpy')
f_prime_lambdified = sp.lambdify(x, f_prime, 'numpy')
f_double_prime_lambdified = sp.lambdify(x, f_double_prime, 'numpy')

# x값 범위 설정
x_vals = np.linspace(-10, 10, 400)
y_vals = f_lambdified(x_vals)
y_prime_vals = f_prime_lambdified(x_vals)
y_double_prime_vals = f_double_prime_lambdified(x_vals)

# y=0 교점 좌표 계산
roots_f_vals = [float(r.evalf()) for r in roots_f]
roots_f_prime_vals = [float(r.evalf()) for r in roots_f_prime]
roots_f_double_prime_vals = [float(r.evalf()) for r in roots_f_double_prime]

#변곡점 찾기
inflection_points = sp.solve(f_double_prime, x)

# 그래프 그리기
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(1,1,1)
plt.subplots_adjust(left=0.25)  # 여백 조정

# 함수와 도함수 그래프
line_f, = ax.plot(x_vals, y_vals, label='Original function', color='blue')
line_f_prime, = ax.plot(x_vals, y_prime_vals, label='First Derivative', color='red', linestyle='--')
line_f_double_prime, = ax.plot(x_vals, y_double_prime_vals, label='Second Derivative', color='green', linestyle='-.')

# y=0 교점 표시 (f, f', f'')
scatter_f = ax.scatter(roots_f_vals, [0]*len(roots_f_vals), color='blue', s=40, label='Roots of f(x)')
scatter_f_prime = ax.scatter(roots_f_prime_vals, [0]*len(roots_f_prime_vals), color='red', s=40, label="Roots of f'(x)")
scatter_f_double_prime = ax.scatter(roots_f_double_prime_vals, [0]*len(roots_f_double_prime_vals), color='green', s=40, label="Roots of f''(x)")

# 교점 주석 설정
annotations_f = [ax.annotate(f'({rx:.2f}, 0)', (rx, 0), textcoords="offset points", xytext=(0,10), ha='center', color='black', visible=True) for rx in roots_f_vals]
annotations_f_prime = [ax.annotate(f'({rx:.2f}, 0)', (rx, 0), textcoords="offset points", xytext=(0,10), ha='center', color='black', visible=True) for rx in roots_f_prime_vals]
annotations_f_double_prime = [ax.annotate(f'({rx:.2f}, 0)', (rx, 0), textcoords="offset points", xytext=(0,10), ha='center', color='black', visible=True) for rx in roots_f_double_prime_vals]


# 변곡점 좌표 계산
inflection_points_vals = [float(p.evalf()) for p in inflection_points]
inflection_y_vals = [f_lambdified(p) for p in inflection_points_vals]

#변곡점 표시
scatter_inflection = plt.scatter(inflection_points_vals, inflection_y_vals, color='purple', s=40, label='Inflection Points')
annotations_inflection = [ax.annotate(f'({ix:.2f}, {iy:.2f})', (ix, iy), textcoords="offset points", xytext=(0,10), ha='center', color='black', visible=True) for ix, iy in zip(inflection_points_vals, inflection_y_vals)]

# 설정 및 표시
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title(f'Graph of f(x)={str(f)}')
ax.grid(True)
ax.legend()
ax.set_ylim([-400, 400])
ax.set_xlim([-10, 10])

# CheckButtons 생성
check_ax = plt.axes([0.02, 0.4, 0.15, 0.15])  # 버튼 위치
check = CheckButtons(
    check_ax,
    ["f(x)", "f'(x)", "f''(x)", "Roots of f(x)", "Roots of f'(x)", "Roots of f''(x)", "Inflection point"],
    [True, True, True, True, True, True, True]
    )

# CheckButtons 이벤트 함수
def toggle_visibility(label):
    if label == "f(x)":
        line_f.set_visible(not line_f.get_visible())
    elif label == "f'(x)":
        line_f_prime.set_visible(not line_f_prime.get_visible())
    elif label == "f''(x)":
        line_f_double_prime.set_visible(not line_f_double_prime.get_visible())
    elif label == "Roots of f(x)":
        visible = not scatter_f.get_visible()
        scatter_f.set_visible(visible)
        for ann in annotations_f:
            ann.set_visible(visible)
    elif label == "Roots of f'(x)":
        visible = not scatter_f_prime.get_visible()
        scatter_f_prime.set_visible(visible)
        for ann in annotations_f_prime:
            ann.set_visible(visible)
    elif label == "Roots of f''(x)":
        visible = not scatter_f_double_prime.get_visible()
        scatter_f_double_prime.set_visible(visible)
        for ann in annotations_f_double_prime:
            ann.set_visible(visible)
    elif label == "Inflection point":
        visible = not scatter_inflection.get_visible()
        scatter_inflection.set_visible(visible)
        for ann in annotations_inflection:
            ann.set_visible(visible)
    plt.draw()

# CheckButtons와 이벤트 연결
check.on_clicked(toggle_visibility)

plt.show()