import os
import subprocess
import tempfile

from PyPDF2 import PdfMerger
from bs4 import BeautifulSoup
from weasyprint import HTML


def convert_chm_to_pdf(chm_path, output_pdf):
    # Temporäres Verzeichnis erstellen
    with tempfile.TemporaryDirectory() as temp_dir:
        # CHM-Datei mit 7-Zip entpacken
        try:
            subprocess.run(
                ["7z", "x", chm_path, f"-o{temp_dir}"], check=True, capture_output=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Fehler beim Entpacken der CHM-Datei: {e.stderr.decode()}"
            )
        except FileNotFoundError:
            raise RuntimeError(
                "7-Zip nicht gefunden. Bitte installieren und in PATH aufnehmen."
            )

        # .hhc-Datei (Inhaltsverzeichnis) finden
        hhc_files = []
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.lower().endswith(".hhc"):
                    hhc_files.append(os.path.join(root, file))
        if not hhc_files:
            raise RuntimeError("Keine .hhc-Datei im CHM-Inhalt gefunden.")
        hhc_path = hhc_files[0]  # Erstes gefundenes .hhc verwenden

        # HTML-Dateien aus .hhc parsen
        html_files = parse_hhc(hhc_path, temp_dir)

        # HTML zu PDF konvertieren und zusammenführen
        merger = PdfMerger()
        for html_file in html_files:
            full_html_path = os.path.join(temp_dir, html_file)
            if not os.path.exists(full_html_path):
                print(f"Warnung: {html_file} nicht gefunden, überspringe.")
                continue
            pdf_path = os.path.join(temp_dir, os.path.basename(html_file) + ".pdf")
            try:
                HTML(
                    full_html_path, base_url=os.path.dirname(full_html_path)
                ).write_pdf(pdf_path)
                merger.append(pdf_path)
            except Exception as e:
                print(f"Fehler beim Konvertieren von {html_file}: {str(e)}")

        # Gesamtes PDF speichern
        merger.write(output_pdf)
        merger.close()


def parse_hhc(hhc_path, base_dir):
    # Extrahiert die Reihenfolge der HTML-Dateien aus der .hhc
    html_files = []
    with open(hhc_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    soup = BeautifulSoup(content, "html.parser")
    for obj in soup.find_all("object", type="text/sitemap"):
        local_param = obj.find("param", {"name": lambda x: x and x.lower() == "local"})
        if local_param and local_param.get("value"):
            html_path = local_param["value"]
            # Pfad relativ zum CHM-Stammverzeichnis
            full_path = os.path.normpath(os.path.join(base_dir, html_path))
            # Sicherstellen, dass die Datei existiert
            if os.path.isfile(full_path):
                html_files.append(html_path)
    return html_files


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CHM zu PDF Konverter")
    parser.add_argument("input_chm", help="Pfad zur Eingabe-CHM-Datei")
    parser.add_argument("output_pdf", help="Pfad zur Ausgabe-PDF-Datei")
    args = parser.parse_args()

    convert_chm_to_pdf(args.input_chm, args.output_pdf)
    print(f"Konvertierung abgeschlossen: {args.output_pdf}")
