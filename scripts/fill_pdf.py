from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName, PdfObject
import json
import sys
import os
from datetime import datetime

# Map your JSON keys (from UI) to the PDF's field names
FIELD_MAP = {
    "client_name": "client",
    "project_name": "reference",
    "transformer_type": "type",
    "installation_type": "installation",
    "Date":"Date",
    # Add more if needed...
}

def remplir_formulaire(input_pdf, output_pdf, champs):
    pdf = PdfReader(input_pdf)

    # Ensure fields display after filling
    if pdf.Root and pdf.Root.AcroForm:
        pdf.Root.AcroForm.update(PdfDict(NeedAppearances=PdfObject('true')))

    for page in pdf.pages:
        annotations = page.get('/Annots')
        if not annotations:
            continue

        for annot in annotations:
            if annot['/Subtype'] == PdfName.Widget and annot.get('/T'):
                # Get the PDF field name from annotation (remove parentheses)
                pdf_field_name = annot['/T'][1:-1]

                # Find if this PDF field name matches any value in FIELD_MAP
                matching_json_keys = [
                    json_key for json_key, mapped_pdf_field in FIELD_MAP.items()
                    if mapped_pdf_field == pdf_field_name
                ]

                if matching_json_keys:
                    json_key = matching_json_keys[0]  # Take the first match

                    if json_key in champs:
                        value = champs[json_key]
                        annot.update(PdfDict(V=str(value)))
                        annot.update(PdfDict(AP=''))  # Force appearance refresh
                        print(f"Filled '{pdf_field_name}' with '{value}' from JSON key '{json_key}'")

    PdfWriter(output_pdf, trailer=pdf).write()
    print(f"SUCCESS: {output_pdf}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python fill_pdf.py <form_data_json> <input_pdf>")
        sys.exit(1)

    form_data_file = sys.argv[1]
    input_pdf = sys.argv[2]

    if not os.path.exists(form_data_file):
        print(f"ERROR: JSON file not found: {form_data_file}")
        sys.exit(1)

    if not os.path.exists(input_pdf):
        print(f"ERROR: Input PDF not found: {input_pdf}")
        sys.exit(1)

    with open(form_data_file, 'r', encoding='utf-8') as f:
        champs_pdf = json.load(f)

    champs_pdf["Date"] = datetime.now().strftime("%d/%m/%Y")

    output_pdf = f"filled_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    remplir_formulaire(input_pdf, output_pdf, champs_pdf)
