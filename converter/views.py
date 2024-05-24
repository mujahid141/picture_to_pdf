

from django.shortcuts import render, redirect
from .forms import ImageForm
from .models import Image
from fpdf import FPDF
from django.http import HttpResponse
from PIL import Image

def convert_image_to_pdf(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            # Convert the image to JPEG
            img = Image.open(image.image.path)
            img = img.convert('RGB')
            img.save('temp.jpg')
            # Generate the PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.image('temp.jpg', 0, 0, 210, 297)
            pdf_file = pdf.output(dest='S').encode('latin-1')
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="image.pdf"'
            return response 
        
    else:
        form = ImageForm()
    return render(request, 'converter/form.html', {'form': form})