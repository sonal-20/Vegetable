
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Receipe  # Make sure your model name matches exactly
from django.http import HttpResponse  # Correct import
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student , SubjectMarks, Subject
from django.contrib.auth import get_user_model
from vege.seed import *
from django.conf import settings
from .utiils import send_email_to_client , send_email_with_attachment
user = get_user_model()
# Create your views here.
@login_required(login_url="/login/")

# @login_required(login_url="/login/")


def send_email(request):
    send_email_to_client()
    
    subject = "This email is from django server with attachment"
    message = "Hey please find this attach file with mail"
    recipient_list = ["chokhandesonal20@gmail.com"]
    file_path = f"{settings.BASE_DIR}/Sonal.pdf"
    
    send_email_with_attachment(subject,message,recipient_list, file_path)
    return redirect('/')



def receipes(request):
    seed_db(100)
    if request.method == "POST":
        data = request.POST
        receipe_image = request.FILES.get('receipe_image')
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
       
        Receipe.objects.create(
            receipe_image=receipe_image,
            receipe_name=receipe_name,
            receipe_description=receipe_description
        )
        return redirect('/receipes/')

    queryset = Receipe.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(receipe_name__icontains = request.GET.get('search') )


    context = {'receipes': queryset}

    return render(request, 'receipes.html', context)  # Correct placement

def delete_receipe(request, id):

    queryset = Receipe.objects.get(id  = id)
    queryset.delete()
    return redirect('/receipes/')



def update_recipes(request, id):
    queryset = Receipe.objects.get(id = id)
    
    context = {'receipe': queryset}
    if request.method == "POST":

        data = request.POST
        receipe_image = request.FILES.get('receipe_image')
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description 

        if receipe_image:
            queryset.receipe_image = receipe_image
 
        queryset.save()    
        return redirect('/receipes/')

    
    return render(request, 'update_receipe.html', context)


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request, 'Invalid username')
            return redirect('/login/')
        
        user = authenticate(username = username, password = password)

        if user is None:
            messages.error(request, 'Invalid password')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/receipes/')

    return render(request, 'login.html')
def logout_page(request):
    logout(request)
    return redirect('/login/')

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
          
        user = User.objects.filter(username= username)
        
        if user.exists():
            messages.info(request, 'Username already exists')
            return redirect('/register/')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
            
        )
        user.set_password(password)
        user.save()
        messages.success(request, 'Registration successful')   
        return redirect('/login/')

    return render(request, 'register.html')



from django.db.models import Q, Sum

def get_students(request):
    queryset = Student.objects.all()
   
    search = request.GET.get('search', '')
    if search:
        queryset = queryset.filter(
            Q(student_name__icontains=search) |
           Q(department__department__icontains=search)|
           Q(student_age__icontains =search ) |
           Q (student_id__student_id__icontains = search)
            )
    
    paginator = Paginator(queryset, 25)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'report/student.html', {'queryset': page_obj})


# def see_marks(request , student_id):
#     queryset = SubjectMarks.objects.filter(student__student_id__student_id = student_id)
#     total_marks = queryset.aggregate(total_marks = Sum('marks'))
#     current_rank = -1
#     ranks = Student.objects.annotate(marks = Sum('studentmarks__marks')).order_by('-marks', 'student_age')
#     i = 1
#     for rank in ranks:
#         if student_id == rank.student_id.student_id:
#             current_rank = i
#             break
#         i += 1

#     return render (request, 'report/see_marks.html',{'queryset':queryset, 'total_marks':total_marks , 'current_rank' : current_rank})

from .seed import generate_report_card
def see_marks(request, student_id):
    generate_report_card()
    queryset = SubjectMarks.objects.filter(student__student_id__student_id=student_id)
    total_marks = queryset.aggregate(total_marks=Sum('marks'))['total_marks']

    # Calculate rank based on total marks and age
    ranks = Student.objects.annotate(marks=Sum('studentmarks__marks')).order_by('-marks', 'student_age')
    current_rank = None
    for i, rank in enumerate(ranks, start=1):
        if student_id == rank.student_id.student_id:
            current_rank = i
            break

    return render(request, 'report/see_marks.html', {
        'queryset': queryset,
        'total_marks': total_marks,
        'current_rank': current_rank,
    })
