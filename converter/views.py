from django.shortcuts import render
from django.http import HttpResponse
from fpdf import FPDF
from PIL import Image as PILImage
import io
import tempfile
import os

def base(request):
    return render(request, 'form.html')

def convert_single_image_to_pdf(request):
    if request.method == 'POST':
        image_file = request.FILES['single_image']
        try:
            image = PILImage.open(io.BytesIO(image_file.read()))
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                image.save(tmp_file, format='JPEG')
                tmp_file.close()

                pdf = FPDF()
                pdf.add_page()

                # Get image dimensions in pixels
                img_width, img_height = image.size
                aspect_ratio = img_width / img_height

                # PDF dimensions in mm (A4 size)
                pdf_width = 210  # mm
                pdf_height = 297  # mm

                # Scale image to fit within the PDF dimensions
                if img_width / pdf_width > img_height / pdf_height:
                    new_width = pdf_width
                    new_height = new_width / aspect_ratio
                else:
                    new_height = pdf_height
                    new_width = new_height * aspect_ratio

                # Center the image on the PDF page
                x = (pdf_width - new_width) / 2
                y = (pdf_height - new_height) / 2

                pdf.image(tmp_file.name, x, y, new_width, new_height)

                os.remove(tmp_file.name)
            response = HttpResponse(pdf.output(dest='S').encode('latin-1'), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="single_image.pdf"'
            return response
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")

def convert_multiple_images_to_pdf(request):
    if request.method == 'POST':
        images = request.FILES.getlist('multiple_images')
        pdf = FPDF()
        try:
            for image_file in images:
                image = PILImage.open(io.BytesIO(image_file.read()))
                if image.mode == 'RGBA':
                    image = image.convert('RGB')
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                    image.save(tmp_file, format='JPEG')
                    tmp_file.close()

                    pdf.add_page()

                    # Get image dimensions in pixels
                    img_width, img_height = image.size
                    aspect_ratio = img_width / img_height

                    # PDF dimensions in mm (A4 size)
                    pdf_width = 210  # mm
                    pdf_height = 297  # mm

                    # Scale image to fit within the PDF dimensions
                    if img_width / pdf_width > img_height / pdf_height:
                        new_width = pdf_width
                        new_height = new_width / aspect_ratio
                    else:
                        new_height = pdf_height
                        new_width = new_height * aspect_ratio

                    # Center the image on the PDF page
                    x = (pdf_width - new_width) / 2
                    y = (pdf_height - new_height) / 2

                    pdf.image(tmp_file.name, x, y, new_width, new_height)

                    os.remove(tmp_file.name)
            response = HttpResponse(pdf.output(dest='S').encode('latin-1'), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="multiple_images.pdf"'
            return response
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
