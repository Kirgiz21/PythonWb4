from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^doctors/$', views.DoctorListView.as_view(), name='doctors'),
    re_path(r'^doctors/(?P<pk>\d+)$', views.DoctorDetailView.as_view(), name='doctor-detail'),

    re_path(r'^doctors/create/$', views.create_doctor, name='create_doctor'),
    re_path(r'^doctors/(?P<pk>\d+)/renew/$', views.update_doctor, name='update_doctor'),
    re_path(r'^doctors/(?P<pk>\d+)/delete/$', views.delete_doctor, name='delete_doctor'),

    re_path(r'^procedure_types/$', views.ProcedureTypeListView.as_view(), name='procedure_types'),
    re_path(r'^procedure_types/create/$', views.create_procedure_type, name='create_procedure_type'),
    re_path(r'^procedure_types/(?P<pk>\d+)/renew/$', views.update_procedure_type, name='update_procedure_type'),
    re_path(r'^procedure_types/(?P<pk>\d+)/delete/$', views.delete_procedure_type, name='delete_procedure_type'),


    re_path(r'^my_procedures/$', views.LoanedProceduresByUserListView.as_view(), name='my_procedures'),
    re_path(r'^all_procedures/$', views.ProceduresListView.as_view(), name='all_procedures'),

    re_path(r'^all_procedures/create_procedure/$', views.create_procedure_admin, name='create_procedure_admin'),
    re_path(r'^all_procedures/(?P<pk>\d+)/renew/$', views.update_procedure, name='update_procedure'),
    re_path(r'^all_procedures/(?P<pk>\d+)/delete/$', views.delete_procedure, name='delete_procedure'),
    re_path(r'^create_procedure/$', views.create_procedure_user, name='create_procedure'),
]
