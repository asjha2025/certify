from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home_view, name="home_view"),
    path('create/', views.create_certificate, name="create_certificate"),
    path('upload-excel/', views.upload_excel, name="upload_excel"),
    path('certificates/', views.list_certificates, name="list_certificates"),
    path('download/<int:cert_id>/', views.download_certificate, name="download_certificate"),
]