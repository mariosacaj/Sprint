from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("index_try/", views.index_try),
    path("standard_upload/", views.upload_standard, name='standard'),
    path("reference_upload/", views.upload_reference, name='reference'),
    path("standard_select/", views.standard_select, name='standard_select'),
    path("reference_select/", views.reference_select, name='reference_select'),
    path("compare/", views.compare, name='compare'),
    path("download/", views.download, name='download'),
    path("getOntology/", views.get_ontology, name='get_ontology'),
    path('getAssociations/', views.get_associations, name='get_associations'),
    path('getXSD/', views.get_xsd, name='get_xsd'),
]
