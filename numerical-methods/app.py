from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)


def bisection_method(func_str, a, b, tol=1e-6, max_iter=100):
    """
    Bisection method implementation.
    Returns steps list and final result.
    """
    allowed = {
        'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
        'exp': math.exp, 'log': math.log, 'sqrt': math.sqrt,
        'pi': math.pi, 'e': math.e, 'abs': abs,
        'log10': math.log10, 'log2': math.log2,
        'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
    }

    def f(x):
        try:
            return eval(func_str.replace('^', '**'), {"__builtins__": {}}, {**allowed, 'x': x})
        except Exception:
            raise ValueError(f"Cannot evaluate function at x = {x}")

    fa = f(a)
    fb = f(b)

    if fa * fb > 0:
        return None, "f(a) and f(b) must have opposite signs (f(a)·f(b) < 0)."

    steps = []
    root = None

    for i in range(1, max_iter + 1):
        c = (a + b) / 2.0
        fc = f(c)

        error = (b - a) / 2.0

        steps.append({
            'iteration': i,
            'a': round(a, 8),
            'b': round(b, 8),
            'c': round(c, 8),
            'fa': round(f(a), 8),
            'fb': round(f(b), 8),
            'fc': round(fc, 8),
            'error': round(error, 8),
        })

        if abs(fc) < 1e-14 or error < tol:
            root = c
            break

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

        root = c

    return steps, root


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bisection')
def bisection():
    return render_template('bisection.html')


@app.route('/api/bisection', methods=['POST'])
def api_bisection():
    data = request.get_json()
    func_str = data.get('func', '')
    try:
        a = float(data.get('a', 0))
        b = float(data.get('b', 1))
        tol = float(data.get('tol', 1e-6))
        max_iter = int(data.get('max_iter', 100))
    except ValueError:
        return jsonify({'error': 'Invalid numeric input.'}), 400

    if not func_str:
        return jsonify({'error': 'Function is required.'}), 400

    try:
        steps, result = bisection_method(func_str, a, b, tol, max_iter)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Computation error: {str(e)}'}), 400

    if steps is None:
        return jsonify({'error': result}), 400

    return jsonify({
        'steps': steps,
        'root': round(result, 10),
        'iterations': len(steps),
    })


if __name__ == '__main__':
    app.run(debug=True)
