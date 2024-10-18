import pandas as pd
from django.shortcuts import render
from django.core.mail import send_mail
from .forms import UploadFileForm

def handle_uploaded_file(f):
    # Check the file extension to determine the appropriate engine
    if f.name.endswith('.xlsx'):
        df = pd.read_excel(f, engine='openpyxl')
    elif f.name.endswith('.xls'):
        df = pd.read_excel(f, engine='xlrd')
    else:
        raise ValueError("Invalid file format. Please upload an Excel file.")

    # Prepare the summary of the data
    summary = df.groupby('Cust State').agg({'DPD': ['mean', 'max']}).reset_index()
    return summary

def file_upload_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            summary = handle_uploaded_file(request.FILES['file'])
            
            # Send the summary via email
            send_mail(
                'Python Assignment -  maroof shaikh',
                summary.to_string(),  # Send as plain text in email body
                'marufshaikh65515@gmail.com',
                ['tech@themedius.ai'],
                fail_silently=False,
            )
            return render(request, 'fileupload/success.html')
    else:
        form = UploadFileForm()
    return render(request, 'fileupload/upload.html', {'form': form})
