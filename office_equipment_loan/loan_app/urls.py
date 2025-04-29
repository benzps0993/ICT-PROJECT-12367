from django.urls import path
from . import views

urlpatterns = [
    path('', views.equipment_list, name='equipment_list'),
    path('borrow/', views.borrow_equipment, name='borrow_equipment'),
    path('return/<int:loan_id>/', views.return_equipment, name='return_equipment'),
    path('report/borrowed/', views.borrowed_equipment_report, name='borrowed_equipment_report'),
    path('report/equipment/<int:equipment_id>/', views.equipment_loan_history_report, name='equipment_loan_history_report'),
    path('report/user/<int:user_id>/', views.user_loan_history_report, name='user_loan_history_report'),
    path('edit/equipment/<int:equipment_id>/', views.edit_equipment, name='edit_equipment'),
    path('edit/user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('add/equipment/', views.add_equipment, name='add_equipment'),
    path('delete/equipment/<int:equipment_id>/', views.delete_equipment, name='delete_equipment'),
    path('add/user/', views.add_user, name='add_user'),
    path('delete/user/confirm/<int:user_id>/', views.delete_user_confirm, name='delete_user_confirm'), # URL สำหรับหน้ายืนยัน
    path('delete/user/process/<int:user_id>/', views.delete_user_process, name='delete_user_process'), # URL สำหรับการลบจริง
    path('search/', views.search_borrowings, name='search_borrowings'),
    path('search/results/', views.search_results, name='search_results'),
    path('history/', views.borrowing_history, name='borrowing_history'),
    path('delete/borrowing/<int:borrowing_id>/', views.delete_borrowing, name='delete_borrowing'), # เพิ่ม URL สำหรับลบประวัติการยืมคืน
]