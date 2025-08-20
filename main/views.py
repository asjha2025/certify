from django.shortcuts import render
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
            df = pd.read_excel(request.FILES['file'])
            for _, row in df.iterrows():
                cert = Certificate.objects.create(
                    employee_name=row['employee_name'],
                    course_title=row['course_title'],
                    issue_date=row['issue_date']
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


def edit_certificate(request, cert_id):
    """
    تعديل شهادة موجودة
    """
    try:
        cert = Certificate.objects.get(id=cert_id)
    except Certificate.DoesNotExist:
        return redirect("main:list_certificates")
    
    if request.method == "POST":
        form = CertificateForm(request.POST, request.FILES, instance=cert)
        if form.is_valid():
            cert = form.save()
            # إعادة توليد ملف PDF بالبيانات الجديدة
            pdf_path = generate_certificate(cert)
            cert.pdf_file.name = pdf_path.replace("media/", "")
            cert.save()
            return redirect("main:list_certificates")
    else:
        form = CertificateForm(instance=cert)
    
    return render(request, "main/edit_certificate.html", {"form": form, "cert": cert})

def delete_certificate(request, cert_id):
    """
    حذف شهادة
    """
    try:
        cert = Certificate.objects.get(id=cert_id)
        # حذف ملف PDF من النظام
        import os
        if cert.pdf_file and os.path.exists(cert.pdf_file.path):
            os.remove(cert.pdf_file.path)
        # حذف الشهادة من قاعدة البيانات
        cert.delete()
    except Certificate.DoesNotExist:
        pass
    
    return redirect("main:list_certificates")
