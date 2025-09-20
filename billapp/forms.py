from django import forms
from .models import Tailoring

class TailoringForm(forms.ModelForm):
    email = forms.EmailField(required=True, help_text="Enter your email to receive the invoice.",
    initial='starfashion4646@gmail.com',  # default email value
    disabled=True )
    description = forms.CharField(
    required=False,
    widget=forms.Textarea(attrs={'placeholder': 'Describe your order', 'rows': 3}),
    help_text="Optional: Add any additional details for this tailoring order."
)


    class Meta:
        model = Tailoring
        fields = [
            'clothing_type', 'name', 'phone_number', 'bill', 'email',
            'shirt_length', 'shirt_shoulder', 'shirt_full_chest', 'shirt_full_stomach', 'shirt_full_hip',
            'shirt_hands', 'shirt_full_arms', 'shirt_cuff', 'shirt_collor',
            'paint_length', 'paint_waist', 'paint_hip', 'paint_full_thighs', 'paint_full_knees',
            'paint_leg_bottom', 'paint_full_seat', 'kurta_length', 'kurta_shoulder', 'kurta_full_chest',
            'kurta_full_stomach', 'kurta_full_hip', 'kurta_hands', 'kurta_full_arms', 'kurta_cuff',
            'kurta_collor', 'pajama_length', 'pajama_leg_bottom', 'pajama_waist',
            'puna_pant_length', 'puna_pant_waist', 'puna_pant_hip', 'puna_pant_full_thighs', 'puna_pant_full_knees',
            'puna_pant_leg_bottom', 'puna_pant_full_seat', 'amount','advance_amount','description', 
        ]
        # exclude = ['bill_number']

        widgets = {
            'clothing_type': forms.Select(),
            'bill_number': forms.NumberInput(),
            'name': forms.TextInput(),
            'age': forms.NumberInput(),
            'phone_number': forms.TextInput(),
            'bill': forms.TextInput(),
            'shirt_length': forms.TextInput(),
            'shirt_shoulder': forms.TextInput(),
            'shirt_full_chest': forms.TextInput(),
            'shirt_full_stomach': forms.TextInput(),
            'shirt_full_hip': forms.TextInput(),
            'shirt_hands': forms.TextInput(),
            'shirt_full_arms': forms.TextInput(),
            'shirt_cuff': forms.TextInput(),
            'shirt_collor': forms.TextInput(),
            'paint_length': forms.TextInput(),
            'paint_waist': forms.TextInput(),
            'paint_hip': forms.TextInput(),
            'paint_full_thighs': forms.TextInput(),
            'paint_full_knees': forms.TextInput(),
            'paint_leg_bottom': forms.TextInput(),
            'paint_full_seat': forms.TextInput(),
            'kurta_length': forms.TextInput(),
            'kurta_shoulder': forms.TextInput(),
            'kurta_full_chest': forms.TextInput(),
            'kurta_full_stomach': forms.TextInput(),
            'kurta_full_hip': forms.TextInput(),
            'kurta_hands': forms.TextInput(),
            'kurta_full_arms': forms.TextInput(),
            'kurta_cuff': forms.TextInput(),
            'kurta_collor': forms.TextInput(),
            'pajama_length': forms.TextInput(),
            'pajama_leg_bottom': forms.TextInput(),
            'pajama_waist': forms.TextInput(),
            'puna_pant_length': forms.TextInput(),
            'puna_pant_waist': forms.TextInput(),
            'puna_pant_hip': forms.TextInput(),
            'puna_pant_full_thighs': forms.TextInput(),
            'puna_pant_full_knees': forms.TextInput(),
            'puna_pant_leg_bottom': forms.TextInput(),
            'puna_pant_full_seat': forms.TextInput(),
            'advance_amount': forms.NumberInput(attrs={'placeholder': 'Enter the advance amount'}), 
            'amount': forms.NumberInput(attrs={'placeholder': 'Enter the amount'})
        }
