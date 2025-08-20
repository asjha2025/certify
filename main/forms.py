from django import forms
from .models import Certificate

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['employee_name', 'course_title', 'issue_date', 'logo']

class UploadExcelForm(forms.Form):
    file = forms.FileField()
