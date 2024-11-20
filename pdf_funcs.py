import PyPDF2

def resize_pdf_to_uniform_width(input_pdf_path, output_pdf_path):
    # Open the input PDF
    with open(input_pdf_path, 'rb') as input_pdf:
        reader = PyPDF2.PdfReader(input_pdf)
        writer = PyPDF2.PdfWriter()

        # Determine the largest width in the PDF
        max_width = max(page.mediabox.width for page in reader.pages)

        for page in reader.pages:
            # Get the original dimensions of the page
            original_width = page.mediabox.width
            original_height = page.mediabox.height

            # Calculate the new height while maintaining the aspect ratio
            scale_factor = max_width / original_width
            new_height = original_height * scale_factor

            # Set the new dimensions for the page
            page.mediabox.lower_right = (max_width, new_height)
            writer.add_page(page)

        # Save the modified PDF
        with open(output_pdf_path, 'wb') as output_pdf:
            writer.write(output_pdf)

# Example usage
input_pdf = "main.pdf"  # Replace with your input PDF file path
output_pdf = "main2.pdf"  # Replace with the desired output PDF file path
resize_pdf_to_uniform_width(input_pdf, output_pdf)