from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName, PdfObject
import json
import sys
import os
from datetime import datetime

# Map your JSON keys to the PDF's field names
FIELD_MAP = {
    "client_name": "client",
    "project_name": "reference",  # This exists in AcroForm!
    "transformer_type": "type",
    "installation_type": "installation",
    "Date": "Date",  # This exists in AcroForm!
    "frequency_hz": "frequence",
    "power_kva": "kVA",
    "primary_voltage": "U1n(V)",
    "secondary_voltage": "U20 (V)",
    # Add more mappings as needed
}

def fill_acroform_fields(pdf, champs):
    """Fill AcroForm fields including multi-instance fields"""
    
    if not (pdf.Root and pdf.Root.AcroForm):
        print("No AcroForm found in PDF")
        return
    
    acroform = pdf.Root.AcroForm
    fields = acroform.get('/Fields')
    
    if not fields:
        print("No fields found in AcroForm")
        return
    
    print("=== FILLING ACROFORM FIELDS ===")
    
    for field in fields:
        field_name = field.get('/T')
        if not field_name:
            continue
            
        # Clean field name (remove parentheses)
        clean_name = field_name[1:-1] if field_name.startswith('(') else str(field_name)
        
        # Find if this field should be filled
        matching_json_keys = [
            json_key for json_key, mapped_field in FIELD_MAP.items()
            if mapped_field == clean_name
        ]
        
        if matching_json_keys:
            json_key = matching_json_keys[0]
            
            if json_key in champs:
                value = str(champs[json_key])
                
                # Set the field value
                field.update(PdfDict(V=value))
                
                # If field has children (multi-instance), fill them too
                kids = field.get('/Kids')
                if kids:
                    print(f"Filled multi-instance field '{clean_name}' with '{value}' ({len(kids)} instances)")
                    for kid in kids:
                        kid.update(PdfDict(V=value))
                        kid.update(PdfDict(AP=''))  # Force appearance refresh
                else:
                    print(f"Filled field '{clean_name}' with '{value}'")
                    
                # Force appearance refresh
                field.update(PdfDict(AP=''))
            else:
                print(f"Field '{clean_name}' found but no data provided")
        else:
            # Check if it's one of our target fields with different case
            if clean_name.lower() in ['reference', 'date', 'revision']:
                print(f"! Found target field '{clean_name}' but no mapping defined")

def fill_page_annotations(pdf, champs):
    """Fill regular page-level form fields"""
    
    print("\n=== FILLING PAGE ANNOTATIONS ===")
    filled_count = 0
    
    for page_num, page in enumerate(pdf.pages, 1):
        annotations = page.get('/Annots')
        if not annotations:
            continue
            
        for annot in annotations:
            if annot['/Subtype'] == PdfName.Widget and annot.get('/T'):
                field_name = annot['/T'][1:-1]
                
                # Find if this field should be filled
                matching_json_keys = [
                    json_key for json_key, mapped_field in FIELD_MAP.items()
                    if mapped_field == field_name
                ]
                
                if matching_json_keys:
                    json_key = matching_json_keys[0]
                    
                    if json_key in champs:
                        value = str(champs[json_key])
                        annot.update(PdfDict(V=value))
                        annot.update(PdfDict(AP=''))
                        print(f"Page {page_num}: Filled '{field_name}' with '{value}'")
                        filled_count += 1
    
    print(f"Total page fields filled: {filled_count}")

def remplir_formulaire_complet(input_pdf, output_pdf, champs):
    """Fill both AcroForm and page-level fields"""
    
    pdf = PdfReader(input_pdf)
    
    # Ensure fields display after filling
    if pdf.Root and pdf.Root.AcroForm:
        pdf.Root.AcroForm.update(PdfDict(NeedAppearances=PdfObject('true')))
    
    print(f"=== FORM DATA TO FILL ===")
    for key, value in champs.items():
        print(f"'{key}' = '{value}'")
    
    # Fill AcroForm fields (including multi-instance header fields)
    fill_acroform_fields(pdf, champs)
    
    # Fill page-level annotations
    fill_page_annotations(pdf, champs)
    
    # Write the result
    PdfWriter(output_pdf, trailer=pdf).write()
    print(f"SUCCESS: {output_pdf}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python acroform_filler.py <form_data_json> <input_pdf>")
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
    
    # Add current date
    champs_pdf["Date"] = datetime.now().strftime("%d/%m/%Y")
    
    output_pdf = f"filled_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    remplir_formulaire_complet(input_pdf, output_pdf, champs_pdf)