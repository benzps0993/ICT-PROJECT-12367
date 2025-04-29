from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Equipment, User, Loan  # เพิ่ม Loan ใน import
from .forms import LoanForm, ReturnForm, EquipmentForm, UserForm, AddEquipmentForm, AddUserForm

def equipment_list(request):
    equipments = Equipment.objects.all()
    users = User.objects.all()
    for equipment in equipments:
        equipment.has_borrowed = equipment.loan_set.filter(return_date__isnull=True).exists()
        equipment.current_loans = equipment.loan_set.filter(return_date__isnull=True).select_related('user')
    context = {'equipments': equipments, 'users': users}
    return render(request, 'loan_app/equipment_list.html', context)

def borrow_equipment(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            equipment = Equipment.objects.get(pk=loan.equipment.id)
            if equipment.available_quantity >= loan.quantity:
                loan.save()
                equipment.available_quantity -= loan.quantity
                equipment.save()
                return redirect('equipment_list')
            else:
                form.add_error(None, f'จำนวนอุปกรณ์ {equipment.name} ที่มีไม่เพียงพอ (มี {equipment.available_quantity} ชิ้น)')
    else:
        form = LoanForm()
    context = {'form': form}
    return render(request, 'loan_app/borrow_equipment.html', context)

def return_equipment(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id, return_date__isnull=True) # ดึงเฉพาะรายการที่ยังไม่คืน
    if request.method == 'POST':
        form = ReturnForm(request.POST, instance=loan)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.return_date = form.cleaned_data['return_date'] or timezone.now() # บันทึกวันที่คืน
            equipment = Equipment.objects.get(pk=loan.equipment.id)
            equipment.available_quantity += loan.quantity
            equipment.save()
            loan.save()
            return redirect('equipment_list')
    else:
        form = ReturnForm(instance=loan)
    context = {'form': form, 'loan': loan}
    return render(request, 'loan_app/return_equipment.html', context)

def borrowed_equipment_report(request):
    borrowed_loans = Loan.objects.filter(return_date__isnull=True).select_related('equipment', 'user')
    context = {'borrowed_loans': borrowed_loans}
    return render(request, 'loan_app/borrowed_equipment_report.html', context)

def equipment_loan_history_report(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    loan_history = Loan.objects.filter(equipment=equipment).order_by('-borrow_date')
    context = {'equipment': equipment, 'loan_history': loan_history}
    return render(request, 'loan_app/equipment_loan_history_report.html', context)

def user_loan_history_report(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    loan_history = Loan.objects.filter(user=user).order_by('-borrow_date')
    context = {'user': user, 'loan_history': loan_history}
    return render(request, 'loan_app/user_loan_history_report.html', context)

def edit_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
    else:
        form = EquipmentForm(instance=equipment)
    context = {'form': form, 'equipment': equipment}
    return render(request, 'loan_app/edit_equipment.html', context)

def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
    else:
        form = UserForm(instance=user)
    context = {'form': form, 'user': user}
    return render(request, 'loan_app/edit_user.html', context)

def add_equipment(request):
    if request.method == 'POST':
        form = AddEquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save()
            return redirect('equipment_list')
    else:
        form = AddEquipmentForm()
    context = {'form': form}
    return render(request, 'loan_app/add_equipment.html', context)

def delete_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    if request.method == 'POST':
        equipment.delete()
        return redirect('equipment_list')
    context = {'equipment': equipment}
    return render(request, 'loan_app/delete_equipment_confirm.html', context)

def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('equipment_list')
    else:
        form = AddUserForm()
    context = {'form': form}
    return render(request, 'loan_app/add_user.html', context)

def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('equipment_list')
    context = {'user': user}
    return render(request, 'loan_app/delete_user_confirm.html', context)

def search_borrowings(request):
    return render(request, 'loan_app/search_borrowings.html')

def search_results(request):
    query = request.GET.get('q')
    search_by = request.GET.get('by')
    results = []

    if query and search_by:
        if search_by == 'borrower_name':
            results = Loan.objects.filter(user__name__icontains=query)  # ค้นหาในชื่อผู้ใช้
        elif search_by == 'item_name':
            results = Loan.objects.filter(equipment__name__icontains=query)  # ค้นหาในชื่ออุปกรณ์
        elif search_by == 'status':
            if query.lower() == 'ยังไม่คืน':
                results = Loan.objects.filter(return_date__isnull=True)
            elif query.lower() == 'คืนแล้ว':
                results = Loan.objects.filter(return_date__isnull=False)

    return render(request, 'loan_app/search_borrowings.html', {'results': results})

def borrowing_history(request):
    borrowing_list = Loan.objects.all().select_related('equipment', 'user').order_by('-borrow_date')
    return render(request, 'loan_app/borrowing_history.html', {'borrowing_list': borrowing_list})

def delete_user_confirm(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {'user': user}
    return render(request, 'loan_app/delete_user_confirm.html', context)


def delete_user_process(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('equipment_list')
    else:
        # ป้องกันการเข้าถึงโดยตรงด้วย GET
        return redirect('equipment_list')

def delete_borrowing(request, borrowing_id):
    borrowing = get_object_or_404(Loan, pk=borrowing_id)
    if request.method == 'POST':
        borrowing.delete()
        return redirect('borrowing_history')
    # ถ้าไม่ใช่ POST request (เช่น เข้ามาด้วย GET โดยตรง) อาจจะ redirect หรือแสดงหน้ายืนยัน
    return redirect('borrowing_history')