from django.contrib import admin
from .models import Doctor, Procedure, ProcedureType

admin.site.register(Doctor)
admin.site.register(Procedure)
admin.site.register(ProcedureType)
