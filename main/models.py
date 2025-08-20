from django.db import models

class Certificate(models.Model):
    employee_name = models.CharField(max_length=200)
    course_title = models.CharField(max_length=200)
    issue_date = models.DateField()
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)
    pdf_file = models.FileField(upload_to="certificates/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_name} - {self.course_title}"
