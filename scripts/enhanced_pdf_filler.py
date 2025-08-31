from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName, PdfObject
import json
import sys
import os
from datetime import datetime
import traceback

class EnhancedPDFFiller:
    def __init__(self):
        print("Initializing Enhanced PDF Filler...")
        # Enhanced field mapping based on your PDF form structure
        self.FIELD_MAP = {
            # Header information
            "client_name": "client",
            "project_name": "reference",
            "transformer_type": "type", 
            "installation_type": "installation",
            "Date": "Date",
            "reference": "reference",
            "revision": "revision",
            
            # Electrical characteristics (Page 1)
            "power_kva": "kVA",
            "frequency_hz": "frequence",
            "primary_voltage": "U1n(V)",
            "secondary_voltage": "U20 (V)",
            "max_temperature_rise": "Variation",
            "primary_coupling": "Couplage",
            "core_material": "ClU(KV)",
            "current_density": "Densite",
            "b_max": "Induction",
            "sheet_type": "ToleMagnetique",
            "winding_material": "NatureBob",
            "cooling_type": "DureeCC",
            "spiresVsp":"spiresVsp",
            
            # Losses and performance
            "core_losses": "PerteVide",
            "no_load_current": "I0Vide",
            "copper_losses": "Pcc", 
            "short_circuit_voltage": "Ucc",
            "total_losses": "PertesTot",
            "temperature_rise": "echauffement",
            
            # Calculated electrical values
            "tensionLignePrim": "tensionLignePrim",
            "tensionLigneSec": "tensionLigneSec",
            "tensionPhasePrim": "tensionPhasePrim", 
            "tensionPhaseSec": "tensionPhaseSec",
            "CourantLignePrim": "CourantLignePrim",
            "CourantLigneSec": "CourantLigneSec",
            "CourantPhasePrim": "CourantPhasePrim",
            "CourantPhaseSec": "CourantPhaseSec",
            "ClasseTensionPrim": "ClasseTensionPrim",
            "ClasseTensionSec": "ClasseTensionSec",
            "ClasseTensionlast": "classeTensionlast",
            
            # Winding step calculations (Page 1)
            "largeurA": "largeurA", "largeurB": "largeurB", "largeurC": "largeurC",
            "largeurD": "largeurD", "largeurE": "largeurE", "largeurF": "largeurF", 
            "largeurG": "largeurG", "largeurH": "largeurH", "largeurI": "largeurI",
            "largeurJ": "largeurJ", "largeurK": "largeurK",
            
            "gradinA": "gradinA", "gradinB": "gradinB", "gradinC": "gradinC",
            "gradinD": "gradinD", "gradinE": "gradinE", "gradinF": "gradinF",
            "gradinG": "gradinG", "gradinH": "gradinH", "gradinI": "gradinI", 
            "gradinJ": "gradinJ", "gradinK": "gradinK",
            
            "EP(mm)A": "EP(mm)A", "EP(mm)B": "EP(mm)B", "EP(mm)C": "EP(mm)C",
            "EP(mm)D": "EP(mm)D", "EP(mm)E": "EP(mm)E", "EP(mm)F": "EP(mm)F",
            "EP(mm)G": "EP(mm)G", "EP(mm)H": "EP(mm)H", "EP(mm)I": "EP(mm)I",
            "EP(mm)J": "EP(mm)J", "EP(mm)K": "EP(mm)K",
            
            "PoidsA": "PoidsA", "PoidsB": "PoidsB", "PoidsC": "PoidsC",
            "PoidsD": "PoidsD", "PoidsE": "PoidsE", "PoidsF": "PoidsF",
            "PoidsG": "PoidsG", "PoidsH": "PoidsH", "PoidsI": "PoidsI",
            "PoidsJ": "PoidsJ", "PoidsK": "PoidsK",
            
            # Core geometry
            "ColonnesSnette": "ColonnesSnette",
            "ColonnesBT": "ColonnesBT", 
            "ColonnesMasse": "ColonnesMasse",
            "4emeColonneSnette": "4emeColonneSnette",
            "4emeColonneMasse": "4emeColonneMasse",
            "CulasseSnette": "CulasseSnette",
            "CulasseBT": "CulasseBT",
            "CulasseMasse": "CulasseMasse",
            "EPCM": "EPCM",
            "MasseCulplusCol": "MasseCulplusCol", 
            "MasseTotale": "MasseTotale",
            
            # Winding parameters (Page 2)
            "ConducteurPrim": "ConducteurPrim",
            "ConducteurSec": "ConducteurSec",
            "BobSectionduConducteurprim1": "BobSectionduConducteurprim1",
            "BobSectionduConducteurSec": "BobSectionduConducteurSec",
            "DensiteCourantPrim": "DensiteCourantPrim",
            "DensiteCourantSec": "DensiteCourantSec",
            "nbCoucherPrim": "nbCoucherPrim",
            "nbCoucherSec": "nbCoucherSec",
            "SpiresCouchePrim": "SpiresCouchePrim",
            "SpiresCoucheSec": "SpiresCoucheSec",
            "NbPapierEpPrim": "NbPapierEpPrim",
            "NbPapierEpSec": "NbPapierEpSec",
            
            # Dimensions and distances
            "CircuitMagnPrim": "CircuitMagnPrim",
            "CircuitMagnSec": "CircuitMagnSec", 
            "DistanceCmagnBT": "DistanceCmagnBT",
            "DimInterBTSec": "DimInterBTSec",
            "EpaisseurBTSec": "EpaisseurBTSec",
            "DimexterBTSec": "DimexterBTSec",
            "Distance MTBT": "Distance MTBT",
            "DimInterMTPrim": "DimInterMTPrim",
            "EpaisseurMTPrim": "EpaisseurMTPrim",
            "DimExterMTPrim": "DimExterMTPrim",
            "HauteurConducteurPrim": "HauteurConducteurPrim",
            "HauteurConducteurSec": "HauteurConducteurSec",
            "LargeurCollierPrim": "LargeurCollierPrim",
            "LargeurCollierSec": "LargeurCollierSec",
            "HauteurBobPrim": "HauteurBobPrim",
            "HauteurBobSec": "HauteurBobSec",
            "PoidsConducteurPrim": "PoidsConducteurPrim",
            "PoidsConducteurSec": "PoidsConducteurSec",
            
            # Short circuit parameters
            "PCC75": "PCC75",
            "addi": "addi",
            "Ucca": "Ucca",
            "Uccr": "Uccr",
            "Ucc75": "Ucc75", 
            "UccCorrigee": "UccCorrigee",
            "ResistanceBT75": "ResistanceBT75",
            "ResistanceMT75": "ResistanceMT75"
        }
        print(f"Field mapping initialized with {len(self.FIELD_MAP)} mappings")

    def validate_pdf_input(self, input_pdf):
        """Validate input PDF file"""
        print(f"\nVALIDATING INPUT PDF: {input_pdf}")
        
        if not os.path.exists(input_pdf):
            print(f"ERROR: PDF file does not exist: {input_pdf}")
            return False
            
        file_size = os.path.getsize(input_pdf)
        print(f"File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        
        if file_size == 0:
            print("ERROR: PDF file is empty")
            return False
            
        try:
            pdf = PdfReader(input_pdf)
            print(f"PDF loaded successfully")
            print(f"Number of pages: {len(pdf.pages)}")
            
            # Check PDF structure
            if pdf.Root:
                print("PDF Root object found")
                if pdf.Root.AcroForm:
                    print("AcroForm found in PDF")
                else:
                    print("WARNING: No AcroForm found in PDF")
            else:
                print("ERROR: No PDF Root object found")
                return False
                
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to read PDF: {str(e)}")
            print(f"Full error: {traceback.format_exc()}")
            return False

    def fill_pdf_comprehensive(self, input_pdf, output_pdf, data):
        """Fill PDF with comprehensive field mapping and detailed logging"""
        
        print(f"\n{'='*60}")
        print(f"STARTING COMPREHENSIVE PDF FILLING")
        print(f"{'='*60}")
        print(f"Input PDF: {input_pdf}")
        print(f"Output PDF: {output_pdf}")
        print(f"Data fields to process: {len(data)}")
        print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Validate input
        if not self.validate_pdf_input(input_pdf):
            print("ABORTING: Input PDF validation failed")
            return None
            
        try:
            print(f"\nLoading PDF with pdfrw...")
            pdf = PdfReader(input_pdf)
            print(f"PDF loaded successfully")
            
            # Configure PDF for form filling
            print(f"\nCONFIGURING PDF FOR FORM FILLING...")
            if pdf.Root and pdf.Root.AcroForm:
                print("Setting NeedAppearances to true...")
                pdf.Root.AcroForm.update(PdfDict(NeedAppearances=PdfObject('true')))
                print("PDF configured for form filling")
            else:
                print("WARNING: No AcroForm found - will try page-level annotations only")
            
            # Show data summary
            print(f"\nDATA SUMMARY:")
            for key, value in list(data.items())[:10]:  # Show first 10 items
                print(f"   {key}: {value}")
            if len(data) > 10:
                print(f"   ... and {len(data) - 10} more fields")
            
            # Fill AcroForm fields
            acroform_count = self._fill_acroform_fields(pdf, data)
            
            # Fill page-level annotations  
            annotation_count = self._fill_page_annotations(pdf, data)
            
            # Write the result
            print(f"\nWRITING OUTPUT PDF...")
            print(f"Output path: {output_pdf}")
            
            try:
                writer = PdfWriter(output_pdf, trailer=pdf)
                writer.write()
                print(f"PDF written successfully")
                
                # Validate output
                if self.validate_output_pdf(output_pdf):
                    print(f"\nSUCCESS: PDF FILLING COMPLETED!")
                    print(f"Summary:")
                    print(f"   - AcroForm fields filled: {acroform_count}")
                    print(f"   - Page annotation fields filled: {annotation_count}")
                    print(f"   - Total fields filled: {acroform_count + annotation_count}")
                    print(f"   - Output file: {output_pdf}")
                    return output_pdf
                else:
                    print(f"ERROR: Output PDF validation failed")
                    return None
                    
            except Exception as write_error:
                print(f"ERROR: Failed to write PDF: {str(write_error)}")
                print(f"Write error details: {traceback.format_exc()}")
                return None
        
        except Exception as e:
            print(f"CRITICAL ERROR during PDF processing: {str(e)}")
            print(f"Full error trace: {traceback.format_exc()}")
            return None

    def _fill_acroform_fields(self, pdf, data):
        """Fill AcroForm fields with detailed logging"""
        
        print(f"\n{'='*40}")
        print(f"FILLING ACROFORM FIELDS")
        print(f"{'='*40}")
        
        if not (pdf.Root and pdf.Root.AcroForm):
            print("No AcroForm found in PDF")
            return 0
        
        acroform = pdf.Root.AcroForm
        fields = acroform.get('/Fields')
        
        if not fields:
            print("No fields found in AcroForm")
            return 0
        
        print(f"Found {len(fields)} AcroForm fields")
        filled_count = 0
        skipped_count = 0
        
        for i, field in enumerate(fields, 1):
            field_name = field.get('/T')
            if not field_name:
                print(f"   {i:3d}. [UNNAMED FIELD] - skipping")
                skipped_count += 1
                continue
                
            # Clean field name
            clean_name = field_name[1:-1] if field_name.startswith('(') else str(field_name)
            
            # Check if we have data for this field
            if clean_name in data:
                value = str(data[clean_name])
                
                try:
                    # Set the field value
                    field.update(PdfDict(V=value))
                    
                    # Handle multi-instance fields
                    kids = field.get('/Kids')
                    if kids:
                        #print(f"   {i:3d}. FILLED '{clean_name}' = '{value}' (multi-instance: {len(kids)} children)")
                        for j, kid in enumerate(kids):
                            kid.update(PdfDict(V=value))
                            kid.update(PdfDict(AP=''))
                            print(f"        Child {j+1} updated")
                    else:
                        print(f"   {i:3d}. FILLED '{clean_name}' = '{value}'")
                        
                    # Force appearance refresh
                    field.update(PdfDict(AP=''))
                    filled_count += 1
                    
                except Exception as field_error:
                    #print(f"   {i:3d}. ERROR '{clean_name}' - {str(field_error)}")
                    skipped_count += 1
            else:
                #print(f"   {i:3d}. SKIPPED '{clean_name}' - no data available")
                skipped_count += 1
        
        print(f"\nAcroForm Summary:")
        print(f"   Fields filled: {filled_count}")
        print(f"   Fields skipped: {skipped_count}")
        print(f"   Total fields: {len(fields)}")
        
        return filled_count

    def _fill_page_annotations(self, pdf, data):
        """Fill page-level form fields with detailed logging"""
        
        print(f"\n{'='*40}")
        print(f"FILLING PAGE ANNOTATIONS")
        print(f"{'='*40}")
        
        total_filled = 0
        total_skipped = 0
        
        for page_num, page in enumerate(pdf.pages, 1):
            print(f"\nProcessing Page {page_num}...")
            
            annotations = page.get('/Annots')
            if not annotations:
                print(f"   No annotations found on page {page_num}")
                continue
            
            page_filled = 0
            page_skipped = 0
            widget_count = 0
            
            for i, annot in enumerate(annotations, 1):
                if annot.get('/Subtype') == PdfName.Widget:
                    widget_count += 1
                    field_name_obj = annot.get('/T')
                    
                    if not field_name_obj:
                        print(f"   {i:3d}. [UNNAMED WIDGET] - skipping")
                        page_skipped += 1
                        continue
                    
                    field_name = field_name_obj[1:-1] if field_name_obj.startswith('(') else str(field_name_obj)
                    
                    if field_name in data:
                        value = str(data[field_name])
                        try:
                            annot.update(PdfDict(V=value))
                            annot.update(PdfDict(AP=''))
                            print(f"   {i:3d}. FILLED '{field_name}' = '{value}'")
                            page_filled += 1
                        except Exception as annot_error:
                            print(f"   {i:3d}. ERROR '{field_name}' - {str(annot_error)}")
                            page_skipped += 1
                    else:
                        print(f"   {i:3d}. SKIPPED '{field_name}' - no data available")
                        page_skipped += 1
            
            #print(f"   Page {page_num} Summary: {widget_count} widgets, {page_filled} filled, {page_skipped} skipped")
            total_filled += page_filled
            total_skipped += page_skipped
        
        print(f"\nPage Annotations Summary:")
        print(f"   Fields filled: {total_filled}")
        print(f"   Fields skipped: {total_skipped}")
        
        return total_filled

    def validate_output_pdf(self, output_pdf):
        """Validate the output PDF"""
        print(f"\nVALIDATING OUTPUT PDF: {output_pdf}")
        
        if not os.path.exists(output_pdf):
            print(f"ERROR: Output PDF was not created: {output_pdf}")
            return False
            
        file_size = os.path.getsize(output_pdf)
        print(f"Output file size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        
        if file_size == 0:
            print("ERROR: Output PDF is empty")
            return False
            
        try:
            pdf = PdfReader(output_pdf)
            print(f"Output PDF can be read successfully")
            print(f"Pages in output: {len(pdf.pages)}")
            return True
            
        except Exception as e:
            print(f"ERROR: Cannot read output PDF: {str(e)}")
            return False

    def generate_field_report(self, input_pdf):
        """Generate a detailed report of all available fields in the PDF"""
        
        print(f"\n{'='*60}")
        print(f"GENERATING PDF FIELD ANALYSIS REPORT")
        print(f"{'='*60}")
        
        if not self.validate_pdf_input(input_pdf):
            return "ERROR: Could not validate input PDF"
            
        pdf = PdfReader(input_pdf)
        report = f"=== PDF FIELD ANALYSIS REPORT ===\n"
        report += f"PDF: {input_pdf}\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"Pages: {len(pdf.pages)}\n\n"
        
        # AcroForm fields
        acroform_count = 0
        if pdf.Root and pdf.Root.AcroForm:
            fields = pdf.Root.AcroForm.get('/Fields')
            if fields:
                acroform_count = len(fields)
                report += f"=== ACROFORM FIELDS ({acroform_count} found) ===\n"
                print(f"Analyzing {acroform_count} AcroForm fields...")
                
                for i, field in enumerate(fields, 1):
                    field_name = field.get('/T')
                    if field_name:
                        clean_name = field_name[1:-1] if field_name.startswith('(') else str(field_name)
                        kids = field.get('/Kids')
                        kid_count = len(kids) if kids else 0
                        
                        report += f"{i:3d}. '{clean_name}'"
                        if kid_count > 0:
                            report += f" (multi-instance: {kid_count} children)"
                        
                        # Check field type
                        field_type = field.get('/FT')
                        if field_type:
                            report += f" [Type: {field_type}]"
                            
                        report += "\n"
                        
                        if i <= 5:  # Show details for first 5 fields
                            print(f"   {i}. '{clean_name}' - Type: {field_type}, Children: {kid_count}")
        
        # Page annotations
        total_annotations = 0
        for page_num, page in enumerate(pdf.pages, 1):
            annotations = page.get('/Annots')
            if annotations:
                page_widgets = [a for a in annotations if a.get('/Subtype') == PdfName.Widget and a.get('/T')]
                if page_widgets:
                    report += f"\n=== PAGE {page_num} ANNOTATIONS ({len(page_widgets)} found) ===\n"
                    print(f"Page {page_num}: Found {len(page_widgets)} widget annotations")
                    
                    for i, annot in enumerate(page_widgets, 1):
                        field_name = annot['/T'][1:-1] if annot['/T'].startswith('(') else str(annot['/T'])
                        field_type = annot.get('/FT', 'Unknown')
                        report += f"{i:3d}. '{field_name}' [Type: {field_type}]\n"
                        total_annotations += 1
        
        report += f"\n=== SUMMARY ===\n"
        report += f"Total AcroForm fields: {acroform_count}\n"
        report += f"Total page annotation fields: {total_annotations}\n"
        report += f"Grand total fields: {acroform_count + total_annotations}\n"
        
        print(f"Field analysis complete:")
        print(f"   AcroForm fields: {acroform_count}")
        print(f"   Page annotation fields: {total_annotations}")
        print(f"   Total fields: {acroform_count + total_annotations}")
        
        return report

def main():
    print("Enhanced PDF Filler - Starting...")
    
    if len(sys.argv) < 3:
        print("ERROR: Insufficient arguments")
        print("Usage: python enhanced_pdf_filler.py <command> <input_pdf> [data_json] [output_pdf]")
        print("Commands:")
        print("  analyze - Generate field analysis report")
        print("  fill - Fill PDF with data")
        sys.exit(1)
    
    command = sys.argv[1]
    input_pdf = sys.argv[2]
    
    print(f"Command: {command}")
    print(f"Input PDF: {input_pdf}")
    
    if not os.path.exists(input_pdf):
        print(f"ERROR: Input PDF not found: {input_pdf}")
        sys.exit(1)
    
    filler = EnhancedPDFFiller()
    
    if command == "analyze":
        print("Starting PDF field analysis...")
        # Generate field analysis report
        report = filler.generate_field_report(input_pdf)
        
        report_file = f"pdf_field_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\nFULL REPORT:")
        print("=" * 60)
        print(report)
        print("=" * 60)
        print(f"Report saved to: {report_file}")
        
    elif command == "fill":
        if len(sys.argv) < 4:
            print("ERROR: Data JSON file required for fill command")
            sys.exit(1)
        
        data_json = sys.argv[3]
        output_pdf = sys.argv[4] if len(sys.argv) > 4 else f"filled_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        print(f"Data JSON: {data_json}")
        print(f"Output PDF: {output_pdf}")
        
        if not os.path.exists(data_json):
            print(f"ERROR: Data JSON file not found: {data_json}")
            sys.exit(1)
        
        # Load data
        print(f"Loading data from JSON...")
        try:
            with open(data_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"Data loaded: {len(data)} fields")
        except Exception as e:
            print(f"ERROR: Failed to load JSON data: {str(e)}")
            sys.exit(1)
        
        # Add current date
        data["Date"] = datetime.now().strftime("%d/%m/%Y")
        print(f"Added current date: {data['Date']}")
        data["Variation"]="± 2x2.5"
        data["DureeCC"]= 2
        
        # Fill PDF
        result = filler.fill_pdf_comprehensive(input_pdf, output_pdf, data)
        
        if result:
            print(f"\nSUCCESS! PDF filled and saved as: {result}")
        else:
            print(f"\nFAILED! PDF filling was not successful")
            sys.exit(1)
        
    else:
        print(f"ERROR: Unknown command '{command}'")
        print("Available commands: analyze, fill")
        sys.exit(1)

if __name__ == "__main__":
    main()
