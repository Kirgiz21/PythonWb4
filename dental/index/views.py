from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views import generic
from .models import Doctor, ProcedureType, Procedure
from .forms import CreateUpdateDoctorForm, ConfirmDeleteForm, CreateUpdateProcedureFormForAdmins, \
    CreateProcedureFormForUsers, CreateUpdateProcedureTypeForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404


def index(request):
    group = Group.objects.get(name='patients')
    users_in_group = group.user_set.all()

    num_doctors = Doctor.objects.all().count()
    num_procedure_type = ProcedureType.objects.all().count()
    num_patient = users_in_group.count()
    data = {
        'num_doctors': num_doctors, 'num_procedure_type': num_procedure_type, 'num_patient': num_patient
    }
    return render(request, 'index.html', context=data)


@permission_required('index.can_add_procedure')
def create_procedure_user(request):
    group = str(list(request.user.groups.all())[0])
    if request.method == 'POST':
        form = CreateProcedureFormForUsers(request.POST)
        if form.is_valid():

            if group == 'patients':
                patient = request.user
                status = 'p'
            else:
                patient = form.cleaned_data['patient']
                status = form.cleaned_data['status']

            procedure = Procedure(
                date_time=form.cleaned_data['date_time'],
                patient=patient,
                doctor=form.cleaned_data['doctor'],
                status=status,
                details=form.cleaned_data['details']
            )
            procedure.save()
            procedure.procedure_type.set(form.cleaned_data['procedure_type'])
            procedure.save()

            return HttpResponseRedirect(reverse('index'))
    else:
        form = CreateProcedureFormForUsers()
    return render(request, 'create_update.html', {'form': form, 'title': 'Створити процедуру'})


@permission_required('index.can_add_procedure_type')
def create_procedure_type(request):
    if request.method == 'POST':
        form = CreateUpdateProcedureTypeForm(request.POST)
        if form.is_valid():
            procedure_type = ProcedureType(
                name=form.cleaned_data['name'],
                price=form.cleaned_data['price'],
                details=form.cleaned_data['details']
            )
            procedure_type.save()
            return HttpResponseRedirect(reverse('procedure_types'))
    else:
        form = CreateUpdateProcedureTypeForm()
    return render(request, 'create_update.html', {'form': form, 'title': 'Створити послугу'})


@permission_required('index.can_edit_procedure_type')
def update_procedure_type(request, pk):
    procedure_type = get_object_or_404(ProcedureType, pk=pk)
    if request.method == 'POST':
        form = CreateUpdateProcedureTypeForm(request.POST)
        if form.is_valid():
            procedure_type.name = form.cleaned_data['name']
            procedure_type.price = form.cleaned_data['price']
            procedure_type.details = form.cleaned_data['details']
            procedure_type.save()
            return HttpResponseRedirect(reverse('procedure_types'))
    else:
        form = CreateUpdateProcedureTypeForm(initial={
            'name': procedure_type.name,
            'price': procedure_type.price,
            'details': procedure_type.details
        })
    return render(request, 'create_update.html', {'form': form, 'title': 'Оновити послугу'})


@permission_required('index.can_delete_procedure_type')
def delete_procedure_type(request, pk):
    procedure_type = get_object_or_404(ProcedureType, pk=pk)

    if request.method == 'POST':
        form = ConfirmDeleteForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm']:
            procedure_type.delete()
            messages.success(request, 'Послуга видалена.')
            return HttpResponseRedirect(reverse('procedure_types'))
    else:
        form = ConfirmDeleteForm()
    return render(request, 'delete.html',
                  {'form': form, 'model': procedure_type, 'back': 'procedure_types', 'title': 'Видалити послугу'})


@permission_required('index.can_add_procedure')
def create_procedure_admin(request):
    if request.method == 'POST':
        form = CreateUpdateProcedureFormForAdmins(request.POST)
        if form.is_valid():
            procedure = Procedure(
                date_time=form.cleaned_data['date_time'],
                patient=form.cleaned_data['patient'],
                doctor=form.cleaned_data['doctor'],
                status=form.cleaned_data['status'],
                details=form.cleaned_data['details']
            )
            procedure.save()
            procedure.procedure_type.set(form.cleaned_data['procedure_type'])
            procedure.save()
            return HttpResponseRedirect(reverse('all_procedures'))
    else:
        form = CreateUpdateProcedureFormForAdmins()
    return render(request, 'create_update.html', {'form': form, 'title': 'Створити процедуру'})


@permission_required('index.can_edit_procedure')
def update_procedure(request, pk):
    procedure = get_object_or_404(Procedure, pk=pk)
    disabled_fields = ['date_time']
    if request.method == 'POST':
        form = CreateUpdateProcedureFormForAdmins(request.POST, disabled_fields=disabled_fields)
        if form.is_valid():
            procedure.patient = form.cleaned_data['patient']
            procedure.doctor = form.cleaned_data['doctor']
            procedure.status = form.cleaned_data['status']
            procedure.details = form.cleaned_data['details']
            procedure.save()
            procedure.procedure_type.set(form.cleaned_data['procedure_type'])
            procedure.save()
            return HttpResponseRedirect(reverse('all_procedures'))
    else:
        form = CreateUpdateProcedureFormForAdmins(initial={
            'date_time': procedure.date_time,
            'patient': procedure.patient,
            'doctor': procedure.doctor,
            'procedure_type': procedure.procedure_type.all(),
            'status': procedure.status,
            'details': procedure.details
        }, disabled_fields=disabled_fields)
    return render(request, 'create_update.html', {'form': form, 'title': 'Оновити процедуру'})


@permission_required('index.can_delete_procedure')
def delete_procedure(request, pk):
    procedure = get_object_or_404(Procedure, pk=pk)

    if request.method == 'POST':
        form = ConfirmDeleteForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm']:
            procedure.delete()
            messages.success(request, 'Процедура видалена.')
            return HttpResponseRedirect(reverse('all_procedures'))
    else:
        form = ConfirmDeleteForm()
    return render(request, 'delete.html',
                  {'form': form, 'model': procedure, 'back': 'all_procedures', 'title': 'Видалити процедуру'})


@permission_required('index.can_add_doctor')
def create_doctor(request):
    if request.method == 'POST':
        form = CreateUpdateDoctorForm(request.POST, request.FILES)
        if form.is_valid():
            doctor = Doctor(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                middle_name=form.cleaned_data['middle_name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                specialization=form.cleaned_data['specialization'],
                photo=form.cleaned_data['photo']
            )
            doctor.save()
            return HttpResponseRedirect(reverse('doctors'))
    else:
        form = CreateUpdateDoctorForm()
    return render(request, 'create_update.html', {'form': form, 'title': 'Створити доктора'})


@permission_required('index.can_edit_doctor')
def update_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = CreateUpdateDoctorForm(request.POST, request.FILES)
        if form.is_valid():
            doctor.first_name = form.cleaned_data['first_name']
            doctor.last_name = form.cleaned_data['last_name']
            doctor.middle_name = form.cleaned_data['middle_name']
            doctor.phone = form.cleaned_data['phone']
            doctor.email = form.cleaned_data['email']
            doctor.specialization = form.cleaned_data['specialization']
            if 'photo' in request.FILES:
                doctor.photo = request.FILES['photo']
            doctor.save()
            return HttpResponseRedirect(reverse('doctors'))
    else:
        form = CreateUpdateDoctorForm(initial={
            'first_name': doctor.first_name,
            'last_name': doctor.last_name,
            'middle_name': doctor.middle_name,
            'phone': doctor.phone,
            'email': doctor.email,
            'specialization': doctor.specialization,
        })
    return render(request, 'create_update.html', {'form': form, 'title': 'Оновити доктора'})


@permission_required('index.can_delete_doctor')
def delete_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)

    if request.method == 'POST':
        form = ConfirmDeleteForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm']:
            doctor.delete()
            messages.success(request, 'Доктор видалений.')
            return HttpResponseRedirect(reverse('doctors'))
    else:
        form = ConfirmDeleteForm()
    return render(request, 'delete.html',
                  {'form': form, 'model': doctor, 'back': 'doctors', 'title': 'Видалити лікаря'})


class ProceduresListView(generic.ListView):
    permission_required = ('index.can_add_procedure', 'index.can_edit_procedure')
    model = Procedure
    context_object_name = 'procedures'
    template_name = 'all_procedures.html'
    paginate_by = 10


class DoctorListView(generic.ListView):
    model = Doctor
    context_object_name = 'doctors'
    template_name = 'doctors.html'
    paginate_by = 6


class ProcedureTypeListView(generic.ListView):
    model = ProcedureType
    context_object_name = 'procedure_types'
    template_name = 'procedure_types.html'
    paginate_by = 5


class DoctorDetailView(generic.DetailView):
    model = Doctor


class LoanedProceduresByUserListView(LoginRequiredMixin, generic.ListView):
    model = Procedure
    template_name = 'my_procedures.html'
    paginate_by = 10

    def get_queryset(self):
        return Procedure.objects.filter(patient=self.request.user).order_by('date_time')
