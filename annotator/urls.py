from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("standard_upload/", views.upload_standard, name='standard'),
    path("reference_upload/", views.upload_reference, name='reference'),
    path("standard_select/", views.standard_select, name='standard_select'),
    path("reference_select/", views.reference_select, name='reference_select'),
    path("compare/", views.compare, name='compare'),
    path("download/", views.download, name='download'),
    path("getOntology/", views.get_ontology, name='get_ontology'),
    path('getAssociations/', views.get_associations, name='get_associations'),
    path('getXSD/', views.get_xsd, name='get_xsd'),
    path("redirect/", views.redirect_view, name='redirect'),
    # path("get_std_type/", views.return_standard_type, name='get_std_type'),
    # path("get_ref_type/", views.return_reference_type, name='get_ref_type'),
    # path("get_valid_standards/", views.get_valid_standards),
    # path("get_valid_references/", views.get_valid_references)
    path("is_valid/", views.is_valid_view, name='is_valid')

]
