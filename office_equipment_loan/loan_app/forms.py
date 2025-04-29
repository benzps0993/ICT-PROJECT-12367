from django import forms
from django.utils import timezone
from .models import Loan, Equipment, User

class LoanForm(forms.ModelForm):
    equipment = forms.ModelChoiceField(queryset=Equipment.objects.all(), label='อุปกรณ์')
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='กำหนดคืน (ไม่บังคับ)', required=False)

    class Meta:
        model = Loan
        fields = ['user', 'equipment', 'quantity', 'due_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].label = 'ผู้ยืม'
        self.fields['quantity'].label = 'จำนวนที่ยืม'

class ReturnForm(forms.ModelForm):
    return_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), initial=timezone.now)

    class Meta:
        model = Loan
        fields = ['return_date']


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'description', 'total_quantity', 'available_quantity'] # เพิ่ม 'available_quantity'

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'age'] # เปลี่ยน 'department' เป็น 'age'
        labels = {
            'name': 'ชื่อผู้ใช้งาน:',
            'age': 'อายุ:',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AddEquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'description', 'total_quantity']

class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'age'] # เปลี่ยน 'department' เป็น 'age'
        labels = {
            'name': 'ชื่อผู้ใช้งาน:',
            'age': 'อายุ:',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }