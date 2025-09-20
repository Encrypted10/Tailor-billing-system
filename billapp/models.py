from django.db import models
from django.db import models, transaction
import uuid
from django.db.models import F
from django.db.utils import IntegrityError
# from .models import BillNumberSequence

class Tailoring(models.Model):
    bill_number = models.PositiveIntegerField(unique=True, editable=False)
    CLOTHING_TYPE_CHOICES = [
        ('shirt', 'Shirt'),
        ('paint', 'Pant'),
        ('kurta', 'Kurta'),
        ('puna_pant', 'Puna Pant'),
        ('pajama', 'Pajama'),
        ('shirt_pant', 'Shirt and Pant'),
        ('kurta_pajama', 'Kurta Pajama'),
        ('kurta_puna_pant', 'Kurta Puna Pant'),
    ]

    bill_number = models.IntegerField()
    clothing_type = models.CharField(max_length=100, choices=CLOTHING_TYPE_CHOICES, default='shirt', verbose_name='Clothing Type')

    # Personal Info
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    bill = models.CharField(max_length=15, default='unpaid')
    # bill = models.CharField(max_length=10, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')])
    email = models.EmailField(default='Null')
    # bill_number = models.CharField(max_length=5, unique=True, editable=False)

    # Shirt Measurements
    shirt_length = models.FloatField(null=True, blank=True, verbose_name='Shirt Length')
    shirt_shoulder = models.FloatField(null=True, blank=True, verbose_name='Shirt Shoulder')
    shirt_full_chest = models.FloatField(null=True, blank=True, verbose_name='Shirt Full Chest')
    shirt_full_stomach = models.FloatField(null=True, blank=True, verbose_name='Shirt Full Stomach')
    shirt_full_hip = models.FloatField(null=True, blank=True, verbose_name='Shirt Full Hip')
    shirt_hands = models.FloatField(null=True, blank=True, verbose_name='Shirt Hands')
    shirt_full_arms = models.FloatField(null=True, blank=True, verbose_name='Shirt Full Arms')
    shirt_cuff = models.FloatField(null=True, blank=True, verbose_name='Shirt Cuff')
    shirt_collor = models.FloatField(null=True, blank=True, verbose_name='Shirt Collar')

    # Pant Measurements
    paint_length = models.FloatField(null=True, blank=True, verbose_name='Pant Length')
    paint_waist = models.FloatField(null=True, blank=True, verbose_name='Pant Waist')
    paint_hip = models.FloatField(null=True, blank=True, verbose_name='Pant Hip')
    paint_full_thighs = models.FloatField(null=True, blank=True, verbose_name='Pant Full Thighs')
    paint_full_knees = models.FloatField(null=True, blank=True, verbose_name='Pant Full Knees')
    paint_leg_bottom = models.FloatField(null=True, blank=True, verbose_name='Pant Leg Bottom')
    paint_full_seat = models.FloatField(null=True, blank=True, verbose_name='Pant Full Seat')

    # Kurta Measurements
    kurta_length = models.FloatField(null=True, blank=True, verbose_name='Kurta Length')
    kurta_shoulder = models.FloatField(null=True, blank=True, verbose_name='Kurta Shoulder')
    kurta_full_chest = models.FloatField(null=True, blank=True, verbose_name='Kurta Full Chest')
    kurta_full_stomach = models.FloatField(null=True, blank=True, verbose_name='Kurta Full Stomach')
    kurta_full_hip = models.FloatField(null=True, blank=True, verbose_name='Kurta Full Hip')
    kurta_hands = models.FloatField(null=True, blank=True, verbose_name='Kurta Hands')
    kurta_full_arms = models.FloatField(null=True, blank=True, verbose_name='Kurta Full Arms')
    kurta_cuff = models.FloatField(null=True, blank=True, verbose_name='Kurta Cuff')
    kurta_collor = models.FloatField(null=True, blank=True, verbose_name='Kurta Collar')

    # Pajama Measurements
    pajama_length = models.FloatField(null=True, blank=True, verbose_name='Pajama Length')
    pajama_leg_bottom = models.FloatField(null=True, blank=True, verbose_name='Pajama Leg Bottom')
    pajama_waist = models.FloatField(null=True, blank=True, verbose_name='Pajama Waist')

    # Puna Pant Measurements (added specifically for Kurta Puna Pant and Puna Pant)
    puna_pant_length = models.FloatField(null=True, blank=True, verbose_name='Puna Pant Length')
    puna_pant_waist = models.FloatField(null=True, blank=True, verbose_name='Puna Pant Waist')
    puna_pant_hip = models.FloatField(null=True, blank=True, verbose_name='Puna Pant Hip')
    puna_pant_full_thighs = models.FloatField(null=True, blank=True, verbose_name='Puna Pant Full Thighs')
    puna_pant_full_knees = models.FloatField(null=True, blank=True, verbose_name='Puna Pant Full Knees')
    puna_pant_leg_bottom = models.FloatField(null=True, blank=True, verbose_name='Puna Pant Leg Bottom')
    puna_pant_full_seat = models.FloatField(null=True, blank=True, verbose_name='Puna Pant Full Seat')


    # Other Details
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Date and Time
    order_date = models.DateField(auto_now_add=True, verbose_name='Order Date')
    order_time = models.TimeField(auto_now_add=True, verbose_name='Order Time')
    description = models.TextField(blank=True, null=True)


    # def __str__(self):
    #     return f"{self.name} - {self.clothing_type}"

    def save(self, *args, **kwargs):
        if self.pk is None:  # Check if this is a new instance
            # Get the next bill number from the sequence
            bill_number_sequence = BillNumberSequence.objects.first()
            if bill_number_sequence is None:
                # Create the sequence if it doesn't exist
                bill_number_sequence = BillNumberSequence.objects.create(next_number=1)
            self.bill_number = bill_number_sequence.get_next_number()
        super().save(*args, **kwargs)



class BillNumberSequence(models.Model):
    """Model to keep track of the next available bill number."""
    next_number = models.PositiveIntegerField(default=1, unique=True)

    def get_next_number(self):
        """Get the next bill number and increment the sequence."""
        with transaction.atomic():
            self.refresh_from_db()
            current_number = self.next_number
            self.next_number += 1
            self.save()
            return current_number

    class Meta:
        verbose_name = "Bill Number Sequence"
        verbose_name_plural = "Bill Number Sequences"

def __str__(self):
        return f"{self.name} - {self.clothing_type}"