from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.http import FileResponse
from .models import Certificate
from .forms import CertificateForm, UploadExcelForm
from .utils import generate_certificate
import pandas as pd




def home_view(request: HttpRequest):

     return render(request, "main/index.html")




def create_certificate(request):
    if request.method == "POST":
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            cert = form.save()
            pdf_path = generate_certificate(cert)
            cert.pdf_file.name = pdf_path.replace("media/", "")
            cert.save()
            return redirect("main:list_certificates")
    else:
        form = CertificateForm()
    return render(request, "main/create_certificate.html", {"form": form})

def upload_excel(request):
    if request.method == "POST":
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            # اقرأ ملف الإكسل
            df = pd.read_excel(request.FILES['file'])

            # تحويل عمود التاريخ إلى كائنات تاريخ
            # to_datetime ستقوم بتحويل الصيغ المختلفة إلى كائن تاريخ موحد
            df['issue_date'] = pd.to_datetime(df['issue_date']).dt.date

            for _, row in df.iterrows():
                cert = Certificate.objects.create(
                    employee_name=row['employee_name'],
                    course_title=row['course_title'],
                    issue_date=row['issue_date']  # الآن هذا كائن تاريخ
                )
                pdf_path = generate_certificate(cert)
                cert.pdf_file.name = pdf_path.replace("media/", "")
                cert.save()
            return redirect("main:list_certificates")
    else:
        form = UploadExcelForm()
    return render(request, "main/upload_excel.html", {"form": form})

def list_certificates(request):
    query = request.GET.get("q", "")
    certs = Certificate.objects.all()
    if query:
        certs = certs.filter(employee_name__icontains=query)
    return render(request, "main/list_certificates.html", {"certs": certs})

def download_certificate(request, cert_id):
    cert = Certificate.objects.get(id=cert_id)
    return FileResponse(open(cert.pdf_file.path, "rb"), as_attachment=True)

