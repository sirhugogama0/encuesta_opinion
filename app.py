from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import os
import json

app = Flask(__name__)

# Ruta del archivo JSON para almacenar los resultados
RESULTS_FILE = "results.json"
GRAPH_FILE = "static/graph.png"

# Cargar resultados iniciales desde el archivo JSON o inicializar en 0
def load_results():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r") as file:
            return json.load(file)
    return {"Buena": 0, "Regular": 0, "Mala": 0}

# Guardar resultados en el archivo JSON
def save_results(results):
    with open(RESULTS_FILE, "w") as file:
        json.dump(results, file)

# Crear gráfica con porcentajes y guardarla como archivo
def create_graph(results):
    total_votes = sum(results.values())
    labels = list(results.keys())

    # Calcular porcentajes
    if total_votes > 0:
        percentages = [(votes / total_votes) * 100 for votes in results.values()]
    else:
        percentages = [0] * len(results)  # Si no hay votos, mostrar 0%

    # Crear la gráfica
    plt.bar(labels, percentages, color=["green", "orange", "red"])
    plt.xlabel("Opiniones")
    plt.ylabel("Porcentaje (%)")
    plt.title("Resultados de la Encuesta")
    plt.ylim(0, 100)  # Escala de 0 a 100%

    # Guardar la gráfica en un archivo
    plt.savefig(GRAPH_FILE)
    plt.close()

# Inicializar resultados
opinions = load_results()

@app.route("/", methods=["GET", "POST"])
def index():
    show_graph = False  # Por defecto, la gráfica está oculta

    if request.method == "POST":
        opinion = request.form.get("opinion")
        if opinion in opinions:
            opinions[opinion] += 1
            save_results(opinions)  # Guardar resultados actualizados

        # Crear la gráfica después de recibir una opinión
        create_graph(opinions)
        show_graph = True  # Mostrar la gráfica después de votar

    # Verificar si el archivo de gráfica existe
    graph_url = GRAPH_FILE if os.path.exists(GRAPH_FILE) else None
    return render_template("index.html", graph_url=graph_url, show_graph=show_graph)

if __name__ == "__main__":
    # Eliminar el gráfico inicial si existe
    if os.path.exists(GRAPH_FILE):
        os.remove(GRAPH_FILE)
    app.run(debug=True)
