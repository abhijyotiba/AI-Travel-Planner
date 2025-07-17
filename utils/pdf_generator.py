from fpdf import FPDF
import io
import datetime

def remove_non_latin1(text: str) -> str:
    return text.encode("latin-1", "ignore").decode("latin-1")

class CustomFPDF(FPDF):
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

def generate_pdf_from_text(text: str) -> io.BytesIO:
    pdf = CustomFPDF() # Use the custom FPDF class
    pdf.alias_nb_pages() # Required for {nb} alias in footer
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Set Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, remove_non_latin1("AI-Generated Travel Plan"), ln=True, align='C')
    
    # Subheading with date
    pdf.set_font("Arial", "", 10)
    generated_date = remove_non_latin1(datetime.datetime.now().strftime('%Y-%m-%d at %H:%M'))
    pdf.cell(0, 10, f"Generated on: {generated_date}", ln=True, align='C')
    
    pdf.ln(10)  # Add space

    # Travel Plan Content
    pdf.set_font("Arial", size=12)

    for line in text.split('\n'):
        line = remove_non_latin1(line.strip())

        if line.startswith("###"):  # H3
            pdf.set_font("Arial", "B", 13)
            pdf.cell(0, 10, line.replace("###", "").strip(), ln=True)
        elif line.startswith("####"):  # H4
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, line.replace("####", "").strip(), ln=True)
        elif line.startswith("-"):  # Bullet point
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 8, f"- {line[1:].strip()}")
        elif line.startswith("**") and line.endswith("**"):  # Bold line
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, line.replace("**", "").strip(), ln=True)
        elif line.strip() == "":
            pdf.ln(3)
        else:
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 8, line.strip())

    # Footer
    pdf.ln(10)
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 8, remove_non_latin1("*This travel plan was generated using AI. Please verify key details before finalizing bookings.*"))

    # Output to BytesIO for download
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return io.BytesIO(pdf_bytes)