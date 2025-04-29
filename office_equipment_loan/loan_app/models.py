from django.db import models

class Equipment(models.Model):
    name = models.CharField(max_length=100, verbose_name='ชื่ออุปกรณ์')
    description = models.TextField(blank=True, null=True, verbose_name='รายละเอียด')
    total_quantity = models.IntegerField(default=0, verbose_name='จำนวนทั้งหมด')
    available_quantity = models.IntegerField(default=0, verbose_name='จำนวนคงเหลือ')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'อุปกรณ์'
        verbose_name_plural = 'อุปกรณ์'

class User(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True) # หรือ PositiveIntegerField

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ผู้ใช้งาน'
        verbose_name_plural = 'ผู้ใช้งาน'

class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ผู้ยืม')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='อุปกรณ์')
    borrow_date = models.DateTimeField(auto_now_add=True, verbose_name='วันที่ยืม')
    return_date = models.DateTimeField(null=True, blank=True, verbose_name='วันที่คืน')
    due_date = models.DateField(null=True, blank=True, verbose_name='กำหนดคืน')
    quantity = models.IntegerField(default=1, verbose_name='จำนวนที่ยืม')

    def __str__(self):
        return f"{self.user.name} - {self.equipment.name} ({self.quantity})"

    class Meta:
        verbose_name = 'รายการยืม'
        verbose_name_plural = 'รายการยืม'

