from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("index_try", views.index_try),
    path("standard_upload", views.upload_standard, name='standard'),
    path("reference_upload", views.upload_reference),
    path("standard_select", views.standard_select),
    path("reference_select", views.reference_select),
    path("compare", views.compare),
    path("download", views.download),
    path("retrieve_json", views.load_json),
    path("retrieve_xsd", views.load_xsd)
]
