import matplotlib.pyplot as plt
import base64
from io import BytesIO


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_plot(x, y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 5))
    plt.title("Incomes per day")

    x_labels = [d.strftime('%Y-%m-%d') for d in x]

    plt.plot(x, y, marker='o', linestyle='-', color='steelblue')
    plt.xlabel('date')
    plt.ylabel('price')
    plt.xticks(rotation=45)
    plt.tight_layout()
    graph = get_graph()
    return graph