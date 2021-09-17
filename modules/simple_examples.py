from gluon import current


def hello3():
    return dict(message="Hello")

def histogram():
    import numpy as np
    import matplotlib.pyplot as plt

    x = [12,-8,56,7,1]
    y = [2,8,5,6,7]

    plt.plot(x, y)
    plt.show()
    plt.savefig("test.svg")
    return

def plot_sympy():
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    import io
    from sympy import symbols
    from sympy.plotting import plot
    x = symbols('x')
    p1 = plot(x*x)
    p2 = plot(x)
    p1.append(p2[0])
    s = io.BytesIO()
    p1.save(s)
    fig=Figure()
    canvas=FigureCanvas(fig)
    canvas.print_tif(s)
    return s.getvalue()
    
def myplot4():
    response = current.response
    response.headers['Content-Type']='image/png'
    return plot_sympy()

