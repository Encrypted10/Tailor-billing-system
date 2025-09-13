from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from billapp.forms import TailoringForm
from billapp.models import Tailoring
from django.contrib.auth import login , authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
# import weasyprint
from .models import Tailoring
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login
from django.conf import settings
from .forms import TailoringForm
from django.db.models import Sum, F, Value,DecimalField
from django.db.models.functions import Coalesce
from django.contrib.auth import authenticate, login as auth_login
from django.core.mail import send_mail
from django.db.models import F, Value, Sum
from django.db.models.functions import Coalesce
from decimal import Decimal


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html',{'form':form})
   



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)  # Log the user in
            # Check if the user is an admin
            if user.is_superuser:
                return redirect('details')  # Admin page URL pattern name
            else:
                return redirect('tailoring_form_view')  # Regular user page URL pattern name
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')


from decimal import Decimal

def successpage(request):
    billapp_tailoring = request.session.get('billapp_tailoring', {})
    
    # Convert amount back to Decimal if needed
    if 'amount' in billapp_tailoring:
        billapp_tailoring['amount'] = Decimal(billapp_tailoring['amount'])
    
    return render(request, 'success.html', {'billapp_tailoring': billapp_tailoring})





# views.py
# views.py
from django.shortcuts import render, redirect
from .forms import TailoringForm

# Example of saving data to session after form submission
def tailoring_form_view(request):
    if request.method == 'POST':
        form = TailoringForm(request.POST)
        if form.is_valid():
            form.save()
            tailoring_instance = form.save() 
            # Store form data in session
            request.session['billapp_tailoring'] = {
                'clothing_type': form.cleaned_data['clothing_type'],
                'name': form.cleaned_data['name'], 
                'phone_number': form.cleaned_data['phone_number'],
                'bill': form.cleaned_data['bill'],
                'email': form.cleaned_data['email'],
                'bill_number': tailoring_instance.bill_number,


                

                'order_date': tailoring_instance.order_date.strftime('%Y-%m-%d'),  # Format date for session
                'order_time': tailoring_instance.order_time.strftime('%H:%M:%S'),
                
                
                # shirt measurments
                'shirt_length': form.cleaned_data['shirt_length'],
                'shirt_shoulder': form.cleaned_data['shirt_shoulder'],
                'shirt_full_chest': form.cleaned_data['shirt_full_chest'],
                'shirt_full_stomach': form.cleaned_data['shirt_full_stomach'],
                'shirt_full_hip': form.cleaned_data['shirt_full_hip'],
                'shirt_hands': form.cleaned_data['shirt_hands'],
                'shirt_full_arms': form.cleaned_data['shirt_full_arms'],
                'shirt_cuff': form.cleaned_data['shirt_cuff'],
                'shirt_collor': form.cleaned_data['shirt_collor'],


                # paint measurments

                'paint_length': form.cleaned_data['paint_length'],
                'paint_waist': form.cleaned_data['paint_waist'],
                'paint_hip': form.cleaned_data['paint_hip'],
                'paint_full_thighs': form.cleaned_data['paint_full_thighs'],
                'paint_full_knees': form.cleaned_data['paint_full_knees'],
                'paint_leg_bottom': form.cleaned_data['paint_leg_bottom'],
                'paint_full_seat': form.cleaned_data['paint_full_seat'],

                # kurta measurmnets

                'kurta_length': form.cleaned_data['kurta_length'],
                'kurta_shoulder': form.cleaned_data['kurta_shoulder'],
                'kurta_full_chest': form.cleaned_data['kurta_full_chest'],
                'kurta_full_stomach': form.cleaned_data['kurta_full_stomach'],
                'kurta_full_hip': form.cleaned_data['kurta_full_hip'],
                'kurta_hands': form.cleaned_data['kurta_hands'],
                'kurta_full_arms': form.cleaned_data['kurta_full_arms'],
                'kurta_cuff': form.cleaned_data['kurta_cuff'],
                'kurta_collor': form.cleaned_data['kurta_collor'],

                #pajama measurments


                'pajama_length': form.cleaned_data['pajama_length'],
                'pajama_leg_bottom': form.cleaned_data['pajama_leg_bottom'],
                'kurta_collor': form.cleaned_data['kurta_collor'],


                'advance_amount':float(form.cleaned_data['advance_amount']),
                'amount': float(form.cleaned_data['amount']),  # Ensure it's JSON serializable
            }
            # customer_email = form.cleaned_data['email']
            # email_subject = "Star Fashion Invoice"
            # email_body = "Thank you for your order. Please find your invoice attached."
            # from_email = 'your_email@gmail.com'
            # to_email = customer_email

            # # Create email message with attachment
            # email = EmailMessage(
            #     email_subject,
            #     email_body,
            #     from_email,
            #     [to_email]
            # )
            # email.attach('invoice.pdf', pdf_stream.getvalue(), 'application/pdf')

            # # Send email
            # email.send(fail_silently=False)

            # return HttpResponse('Your form was submitted successfully and the invoice has been sent to your email.')
            return redirect('success')  # Redirect to success page
    else:
        form = TailoringForm()

    return render(request, 'tailoring_form.html', {'form': form})



from django.db.models import Sum,Q # Ensure this is your model
from datetime import datetime

from django.shortcuts import render
from django.db.models import Q, F, Value, Sum, DecimalField
from django.db.models.functions import Coalesce
from decimal import Decimal
from .models import Tailoring

def details(request):
    # Base queryset
    billdata = Tailoring.objects.all()

    # Get filters from the request
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')

    # Apply filters only if they are not empty
    if year:
        try:
            year = int(year)
            billdata = billdata.filter(order_date__year=year)
        except ValueError:
            pass

    if month:
        try:
            month = int(month)
            billdata = billdata.filter(order_date__month=month)
        except ValueError:
            pass

    if day:
        try:
            day = int(day)
            billdata = billdata.filter(order_date__day=day)
        except ValueError:
            pass

    # Search functionality
    search_term = request.GET.get('search')
    if search_term:
        try:
            search_term_int = int(search_term)
            billdata = billdata.filter(
                Q(name__icontains=search_term) | Q(bill_number=search_term_int)
            )
        except ValueError:
            billdata = billdata.filter(Q(name__icontains=search_term))

    # -------------------------------
    # Calculate totals properly
    # -------------------------------

    # Sum of full amounts for fully paid bills
    paid_full = billdata.filter(bill='paid').aggregate(
        total=Sum(F('amount'), output_field=DecimalField())
    )['total'] or Decimal('0')

    # Sum of advance payments for unpaid bills
    advance_paid = billdata.filter(bill='unpaid').aggregate(
        total=Sum(Coalesce(F('advance_amount'), Value(0), output_field=DecimalField()))
    )['total'] or Decimal('0')

    # Total paid = full paid + advances
    total_paid_amount = paid_full + advance_paid

    # Total due = remaining amount for unpaid bills
    total_due_amount = billdata.filter(bill='unpaid').aggregate(
        total=Sum(F('amount') - Coalesce(F('advance_amount'), Value(0), output_field=DecimalField()),
                  output_field=DecimalField())
    )['total'] or Decimal('0')

    # -------------------------------
    # Get unique years and months for filters
    # -------------------------------
    years = Tailoring.objects.dates('order_date', 'year').distinct()
    months = Tailoring.objects.dates('order_date', 'month').distinct()

    # Extract unique days if year and month are selected
    if year and month:
        days = Tailoring.objects.filter(order_date__year=year, order_date__month=month)\
            .values_list('order_date__day', flat=True).distinct()
        days = sorted(days)
    else:
        days = []

    # -------------------------------
    # Pass data to template
    # -------------------------------
    context = {
        'billdata': billdata,
        'total_paid_amount': total_paid_amount,
        'total_due_amount': total_due_amount,
        'years': years,
        'months': months,
        'days': days,
        'selected_year': year,
        'selected_month': month,
        'selected_day': day,
    }

    return render(request, 'details.html', context)





# list and details
from django.shortcuts import render, get_object_or_404
from .models import Tailoring

def tailoring_list(request):
    tailoring_records = Tailoring.objects.all()
    if request.method == "GET":
        search_term = request.GET.get('search')
        if search_term:
            # Try converting the search term to an integer for numeric searches
            try:
                search_term_int = int(search_term)
                tailoring_records = Tailoring.objects.filter(
                    Q(name__icontains=search_term) | Q(bill_number=search_term_int)
                )
            except ValueError:
                # If conversion fails, treat the search term as a string for non-numeric fields
                tailoring_records = Tailoring.objects.filter(
                    Q(name__icontains=search_term)
                )
    return render(request, 'tailoring_list.html', {'tailoring_records': tailoring_records})

def tailoring_detail(request, pk):
    tailoring_record = get_object_or_404(Tailoring, pk=pk)
    return render(request, 'tailoring_details.html', {'tailoring_record': tailoring_record})






# pdf
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
# import weasyprint
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io

# def render_to_pdf(template_src, context_dict):
#     """
#     Converts HTML to PDF using xhtml2pdf
#     """
#     template = render_to_string(template_src, context_dict)
#     result = io.BytesIO()
#     pdf = pisa.pisaDocument(io.BytesIO(template.encode("UTF-8")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None

# def generate_pdf_view(request):
#     billapp_tailoring = request.session.get('billapp_tailoring', {})
    
#     # Pass the bill details to the PDF generation function
#     context = {'billapp_tailoring': billapp_tailoring, 
#         #        'order_date': billapp_tailoring.order_date,
#         # 'order_time': billapp_tailoring.order_time,
#         }
#     pdf = render_to_pdf('pdf_template.html', context)
    
#     if pdf:
#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="Bill Recipt.pdf"'
#         return response
#     else:
#         return HttpResponse("Error generating PDF")




# sharing pdf 


from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa

def generate_pdf(tailoring_data):
    template_path = 'pdf_template.html'  # Path to your PDF template
    context = {'billapp_tailoring': tailoring_data}
    
    # Create an in-memory file object
    response = BytesIO()
    html = render_to_string(template_path, context)
    
    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Check for PDF generation errors
    if pisa_status.err:
        return None
    
    # Seek to the beginning of the BytesIO stream
    response.seek(0)
    
    
    return response



import os
from django.conf import settings

def generate_pdf_view(request):
    billapp_tailoring = request.session.get('billapp_tailoring', {})
    pdf_stream = generate_pdf(billapp_tailoring)  # Assume returns BytesIO or similar
    
    # Save PDF to disk
    pdf_dir = os.path.join(settings.MEDIA_ROOT, 'pdfs')
    os.makedirs(pdf_dir, exist_ok=True)
    filename = f"order_{billapp_tailoring.get('name', 'client').replace(' ', '_').lower()}.pdf"
    file_path = os.path.join(pdf_dir, filename)
    
    with open(file_path, 'wb') as f:
        pdf_stream.seek(0)
        f.write(pdf_stream.read())
    
    # Prepare email
    customer_email = billapp_tailoring.get('email', 'default@example.com')
    email = EmailMessage(
        "Star Fashion Invoice",
        "Thank you for your order. Please find your invoice attached.",
        'ch41019@gmail.com',
        [customer_email]
    )
    
    # Attach the saved PDF
    with open(file_path, 'rb') as f:
        email.attach(filename, f.read(), 'application/pdf')

    email.send(fail_silently=False)
    
    client_name = billapp_tailoring.get('name', 'Client')
    client_email = billapp_tailoring.get('email', 'Client')
    return HttpResponse(f'Successfully, your invoice has been saved and sent to {client_name} ({client_email}).')

#     # except Exception as e:
    #         # return JsonResponse({'error': f'Error sending email: {str(e)}'}, status=500)
    #         HttpResponse('Fild to sent inovice')
    # else:
    #     return JsonResponse({'error': 'Invalid request method.'}, status=405)
# 

# test 








from django.shortcuts import render, redirect
from .models import Tailoring

def update_status(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('status_'):
                record_id = key.split('_')[1]
                status = value
                Tailoring.objects.filter(id=record_id).update(bill=status)
        return redirect('details')  # Redirect to the view displaying the records

# edit_tailoring


def edit_tailoring(request, pk):
    tailoring_record = get_object_or_404(Tailoring, pk=pk)
    
    if request.method == 'POST':
        form = TailoringForm(request.POST, instance=tailoring_record)
        if form.is_valid():
            form.save()
            return redirect('tailoring_detail', pk=tailoring_record.pk)  # Redirect to the detail page
    else:
        form = TailoringForm(instance=tailoring_record)
    
    return render(request, 'edit_tailoring.html', {'form': form})



def delete_record(request, record_id):
    if request.method == 'POST':
        record = get_object_or_404(Tailoring, id=record_id)
        record.delete()
    return redirect('details') 