from flask import Flask, request, render_template
import pdfplumber
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def pdf_a_excel(pdf_path, excel_path):
    all_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                all_data.extend(table)
    df = pd.DataFrame(all_data)
    df.columns = df.iloc[2]  # Usa encabezados reales (fila 3)
    df = df[3:]              # Elimina encabezados
    df.to_excel(excel_path, index=False)
    return df  # Devolver el DataFrame ya procesado

@app.route("/", methods=["GET", "POST"])  # Se debe especificar el método POST
def index():
    conteo_html = None
    if request.method == "POST":
        opcion = request.form.get("opcion")
        pdf = request.files["pdf"]
        pdf_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
        excel_path = pdf_path.replace(".pdf", ".xlsx")
        pdf.save(pdf_path)
        df = pdf_a_excel(pdf_path, excel_path)

        try:
            if opcion == "ph":
                # Verifica si la columna 'TX' existe
                if 'TX' in df.columns:
                    # Limpiar los datos de la columna 'TX' (eliminamos espacios y normalizamos)
                    df['TX'] = df['TX'].str.strip().str.lower()  # Eliminar espacios y convertir a minúsculas
                    
                    # Conteo de PHs de la columna TX
                    conteo = df['TX'].value_counts().reset_index()
                    conteo.columns = ['Tipo de PH', 'Cantidad']
                else:
                    conteo = pd.DataFrame()
                    conteo_html = "<p><strong>Error:</strong> La columna 'TX' no existe en el archivo.</p>"

            elif opcion == "cliente":
                if "Cliente" in df.columns and "TX" in df.columns:
                    grouped = df.groupby(["Cliente", "TX"]).size().reset_index(name="Cantidad")
                    resumen = grouped.groupby("Cliente").apply(
                        lambda x: ", ".join(f"{row['TX']}: {row['Cantidad']}" for _, row in x.iterrows())
                    ).reset_index(name="PH que tiene")

                    total = df["Cliente"].value_counts().reset_index()
                    total.columns = ["Cliente", "Cantidad"]

                    conteo = pd.merge(total, resumen, on="Cliente")
                else:
                    conteo = pd.DataFrame()
            else:
                conteo = pd.DataFrame()

            # Convertir el conteo a HTML
            conteo_html = conteo.to_html(index=False)
        except Exception as e:
            conteo_html = f"<p><strong>Error al procesar:</strong> {e}</p>"

    return render_template("index.html", resultado=conteo_html)  # Pasamos conteo_html a la plantilla

if __name__ == "__main__":
    print("🚀 Iniciando aplicación Flask...")
    app.run(debug=True)
    