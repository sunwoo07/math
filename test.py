import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, TextBox

# 초기 함수 정의
x = sp.symbols('x')
f = (x - 5) * (x + 5) * (x + 3)

# 함수 업데이트를 위한 함수 정의
def update_function(expression):
    global f, f_prime, f_double_prime
    try:
        # 입력 받은 수식을 SymPy의 표현식으로 변환
        f = sp.sympify(expression)
        
        # 함수와 도함수 다시 계산
        f_prime = sp.diff(f, x)
        f_double_prime = sp.diff(f_prime, x)
        
        # y=0 교점 및 변곡점 재계산
        roots_f = sp.solve(f, x)
        roots_f_prime = sp.solve(f_prime, x)
        roots_f_double_prime = sp.solve(f_double_prime, x)
        inflection_points = sp.solve(f_double_prime, x)
        
        # 함수와 도함수를 넘파이용 함수로 변환
        f_lambdified = sp.lambdify(x, f, 'numpy')
        f_prime_lambdified = sp.lambdify(x, f_prime, 'numpy')
        f_double_prime_lambdified = sp.lambdify(x, f_double_prime, 'numpy')
        
        # 그래프 업데이트
        x_vals = np.linspace(-10, 10, 400)
        y_vals = f_lambdified(x_vals)
        y_prime_vals = f_prime_lambdified(x_vals)
        y_double_prime_vals = f_double_prime_lambdified(x_vals)
        
        # y=0 교점 업데이트
        roots_f_vals = [float(r.evalf()) for r in roots_f]
        roots_f_prime_vals = [float(r.evalf()) for r in roots_f_prime]
        roots_f_double_prime_vals = [float(r.evalf()) for r in roots_f_double_prime]
        
        # 변곡점 업데이트
        inflection_points_vals = [float(p.evalf()) for p in inflection_points]
        inflection_y_vals = [f_lambdified(p) for p in inflection_points_vals]

        # 그래프에 적용
        line_f.set_ydata(y_vals)
        line_f_prime.set_ydata(y_prime_vals)
        line_f_double_prime.set_ydata(y_double_prime_vals)

        # 교점 및 변곡점 업데이트
        scatter_f.set_offsets(np.c_[roots_f_vals, [0] * len(roots_f_vals)])
        scatter_f_prime.set_offsets(np.c_[roots_f_prime_vals, [0] * len(roots_f_prime_vals)])
        scatter_f_double_prime.set_offsets(np.c_[roots_f_double_prime_vals, [0] * len(roots_f_double_prime_vals)])
        scatter_inflection.set_offsets(np.c_[inflection_points_vals, inflection_y_vals])

        # 주석 업데이트
        for ann in annotations_f + annotations_f_prime + annotations_f_double_prime + annotations_inflection:
            ann.remove()  # 기존 주석 삭제
        annotations_f[:] = [ax.annotate(f'({rx:.2f}, 0)', (rx, 0), textcoords="offset points", xytext=(0,10), ha='center', color='black', visible=True) for rx in roots_f_vals]
        annotations_f_prime[:] = [ax.annotate(f'({rx:.2f}, 0)', (rx, 0), textcoords="offset points", xytext=(0,10), ha='center', color='black', visible=True) for rx in roots_f_prime_vals]
        annotations_f_double_prime[:] = [ax.annotate(f'({rx:.2f}, 0)', (rx, 0), textcoords="offset points", xytext=(0,10), ha='center', color='black', visible=True) for rx in roots_f_double_prime_vals]
        annotations_inflection[:] = [ax.annotate(f'({ix:.2f}, {iy:.2f})', (ix, iy), textcoords="offset points", xytext=(0,10), ha='center', color='black', visible=True) for ix, iy in zip(inflection_points_vals, inflection_y_vals)]

        # 그래프 제목 업데이트
        ax.set_title(f'Graph of f(x)={str(f)}')
        plt.draw()

    except Exception as e:
        print("Invalid input:", e)

# 초기 그래프 설정
f_prime = sp.diff(f, x)
f_double_prime = sp.diff(f_prime, x)

# 초기 y=0 교점 및 변곡점
roots_f = sp.solve(f, x)
roots_f_prime = sp.solve(f_prime, x)
roots_f_double_prime = sp.solve(f_double_prime, x)
inflection_points = sp.solve(f_double_prime, x)

# 함수와 미분함수 넘파이 변환
f_lambdified = sp.lambdify(x, f, 'numpy')
f_prime_lambdified = sp.lambdify(x, f_prime, 'numpy')
f_double_prime_lambdified = sp.lambdify(x, f_double_prime, 'numpy')

x_vals = np.linspace(-10, 10, 400)
y_vals = f_lambdified(x_vals)
y_prime_vals = f_prime_lambdified(x_vals)
y_double_prime_vals = f_double_prime_lambdified(x_vals)

roots_f_vals = [float(r.evalf()) for r in roots_f]
roots_f_prime_vals = [float(r.evalf()) for r in roots_f_prime]
roots_f_double_prime_vals = [float(r.evalf()) for r in roots_f_double_prime]
inflection_points_vals = [float(p.evalf()) for p in inflection_points]
inflection_y_vals = [f_lambdified(p) for p in inflection_points_vals]

fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(left=0.3)

line_f, = ax.plot(x_vals, y_vals, label='Original function', color='blue')
line_f_prime, = ax.plot(x_vals, y_prime_vals, label='First Derivative', color='red', linestyle='--')
line_f_double_prime, = ax.plot(x_vals, y_double_prime_vals, label='Second Derivative', color='green', linestyle='-.')
scatter_f = ax.scatter(roots_f_vals, [0] * len(roots_f_vals), color='blue', s=40, label='Roots of f(x)')
scatter_f_prime = ax.scatter(roots_f_prime_vals, [0] * len(roots_f_prime_vals), color='red', s=40, label="Roots of f'(x)")
scatter_f_double_prime = ax.scatter(roots_f_double_prime_vals, [0] * len(roots_f_double_prime_vals), color='green', s=40, label="Roots of f''(x)")
scatter_inflection = plt.scatter(inflection_points_vals, inflection_y_vals, color='purple', s=40, label='Inflection Points')

annotations_f = [ax.annotate(f'({rx:.2f}, 0)', (rx, 0), textcoords="offset points", xytext=(0,10), ha='center', color='black', visible=True) for rx in roots_f_vals]
annotations_f_prime = [ax.annotate(f'({rx:.2f}, 0)', (rx, 0), textcoords="offset points", xytext=(0,10), ha='center', color='black', visible=True) for rx in roots_f_prime_vals]
annotations_f_double_prime = [ax.annotate(f'({rx:.2f}, 0)', (rx, 0), textcoords="offset points", xytext=(0,10), ha='center', color='black', visible=True) for rx in roots_f_double_prime_vals]
annotations_inflection = [ax.annotate(f'({ix:.2f}, {iy:.2f})', (ix, iy), textcoords="offset points", xytext=(0,10), ha='center', color='black', visible=True) for ix, iy in zip(inflection_points_vals, inflection_y_vals)]

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title(f'Graph of f(x)={str(f)}')
ax.grid(True)
ax.legend()
ax.set_ylim([-400, 400])
ax.set_xlim([-10, 10])

# CheckButtons
check_ax = plt.axes([0.05, 0.4, 0.15, 0.2])
check = CheckButtons(check_ax, ["f(x)", "f'(x)", "f''(x)", "Roots of f(x)", "Roots of f'(x)", "Roots of f''(x)", "Inflection point"], [True, True, True, True, True, True, True])

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

check.on_clicked(toggle_visibility)

# TextBox
text_box_ax = plt.axes([0.05, 0.7, 0.2, 0.05])
text_box = TextBox(text_box_ax, "f(x)", initial=str(f))
text_box.on_submit(update_function)

plt.show()
