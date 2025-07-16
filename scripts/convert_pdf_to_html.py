import os
from pathlib import Path
from pdf2image import convert_from_path

# Définition des chemins de base
BASE_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = BASE_DIR / "plaquettes"
HTML_OUTPUT_DIR = BASE_DIR / "html_plaquettes"

# Création du dossier de sortie s'il n'existe pas
HTML_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Configuration de la résolution pour la conversion PDF en image
DPI = 150

def convert_pdf_to_html(pdf_path: Path):
    product_name = pdf_path.stem

    # Chemins des fichiers générés
    output_image_path = HTML_OUTPUT_DIR / f"{product_name}.png"
    output_html_path = HTML_OUTPUT_DIR / f"{product_name}.html"

    try:
        # Conversion du PDF en image PNG (première page uniquement)
        image = convert_from_path(str(pdf_path), dpi=DPI)[0]
        image.save(output_image_path, "PNG")
    except Exception as e:
        print(f"❌ Échec de la conversion pour {pdf_path.name}: {e}")
        return

    # Contenu HTML généré dynamiquement
    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>{product_name}</title>
  <style>
    body {{
      margin: 0;
      padding: 2rem;
      background-color: #f4f4f9;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
    }}
    .card {{
      background: #ffffff;
      border-radius: 12px;
      padding: 1rem;
      box-shadow: 0 6px 12px rgba(0,0,0,0.1);
      max-width: 900px;
      width: 90%;
    }}
    .card img {{
      width: 100%;
      border-radius: 8px;
      display: block;
    }}
  </style>
</head>
<body>
  <div class="card">
    <img src="{product_name}.png" alt="Plaquette produit : {product_name}">
  </div>
</body>
</html>"""

    # Sauvegarde du fichier HTML
    with open(output_html_path, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"✅ Fichier HTML généré : {product_name}.html")

# Conversion de tous les fichiers PDF présents dans le dossier "plaquettes"
for pdf_file in PDF_DIR.glob("*.pdf"):
    convert_pdf_to_html(pdf_file)