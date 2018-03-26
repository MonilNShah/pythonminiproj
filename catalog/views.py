from django.shortcuts import render,redirect,get_object_or_404
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Patient,Slots,Doctor,Appointment
from django.contrib.auth.decorators import login_required
from .form import RegistrationForm,RegistrationForm2,apointForm
from django.contrib.auth.models import User
import datetime
import time
'''from django.views import generic

class BookListView(generic.ListView):
    model = Book
    template_name = 'book.html'  # Specify your own template name/location'''


def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    a=[]
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # The 'all()' is implied by default.
    book=Book.objects.all()
    # for bb in book:
    #     # print(bb.book_pic.url)
    #     a.append(bb.book_pic)
    author=Author.objects.all()
    print(book)
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors ,'book':book,'author':author}
    )


def takeapoint(request):
    registered=False
    apoint=apointForm()
    slots=Slots.objects.none()
    doctors=Doctor.objects.all()
    slots_time=Slots.objects.none()
    if request.method == 'POST':
        apoint_form =apointForm(request.POST)
        print(apoint_form)
        print("Before Validaion")
        dt=(request.POST['slot'])
        print("Value Taken=",dt)
        # apoint_form.Slot_Time_id=Slots.objects.filter(Slot_Time=dt).values('id')[0]['id'] 
        if (apoint_form.is_valid()):
            print("Validated")
            #return HttpResponse("HELOOOOOOOOOOOOO")
            user1=apoint_form.save(commit=False)
            value=request.POST['doctor_name']
            value2=(request.POST['slot'])
            value3=request.POST['date']
            user1.Date=value3
            # print(request.user.get_username())
            # print(value2)
            # {{value2|time:"%H:%M:%S"}}
            user1.Doctor_id_id=Doctor.objects.filter(First_Name=value).values('id')[0]['id'] 
            user1.Slot_Time_id=Slots.objects.filter(Slot_Time=dt).values('id')[0]['id'] 
            user1.u_id=User.objects.get(username=request.user.get_username())
            user1.Taken_time=datetime.datetime.now().time()
            #user_form.set_password(user.password)
            print("HELOOOOOOOOOOOOO")
            '''username = user_form.get('username')
            raw_password = user_form.get('password')
            print(username)
            user.first_name=user_form.get('first_name')
            user.last_name=user_form.get('last_name')
            user.email=user_form.get('email')'''
            '''user.first_name=request.POST.get('first_name')
            user.last_name=request.POST.get('last_name')
            user.email=request.POST.get('email')'''
            user1.save()
            #login(request, authenticate(username=username, password=raw_password))
            registered = True
            # print(user_form['username'])
        else:
             print(" NOt Validated")

    else:
        print("Not Validated")
        apoint=apointForm()
        slots=Slots.objects.none()
        doctors=Doctor.objects.all()
        slots_time=Slots.objects.none()
        # user_form = RegistrationForm()
    if registered:
         return redirect ('/takeapoint/')
         #return reverse ('home:base')
    else:
        return render(
            request,
            'apoint.html',
            context={'slots_time':slots_time,'apoint':apoint,'doctors':doctors}
    )


def book(request,pk):
    post = get_object_or_404(Book, pk=pk)
    print(post.id)
    ans_list = Book.objects.filter(id=post.id)
    return render(request,'bookdetial.html',context={'ans_dict':ans_list})

def author(request,pk):
    post = get_object_or_404(Author, first_name=pk)
    print(post)
    ans_list = Author.objects.filter(first_name=post.first_name)
    return render(request,'author.html',context={'ans_dict':ans_list})


def register(request):
    p=Patient.objects.all()
    print(p[0].u_id)
    registered = False
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        user_form2 = RegistrationForm2(request.POST)
        print("Before Validaion")
        if (user_form.is_valid() and user_form2.is_valid()):
            print("Validated")
            #return HttpResponse("HELOOOOOOOOOOOOO")
            user=user_form.save()
            print(user)
            print(user.id)
            print(user.username)
            user2=user_form2.save(commit =False)
            user2.u_id=user
            #user_form.set_password(user.password)
            print("HELOOOOOOOOOOOOO")
            '''username = user_form.get('username')
            raw_password = user_form.get('password')
            print(username)
            user.first_name=user_form.get('first_name')
            user.last_name=user_form.get('last_name')
            user.email=user_form.get('email')'''
            '''user.first_name=request.POST.get('first_name')
            user.last_name=request.POST.get('last_name')
            user.email=request.POST.get('email')'''
            user.save()
            user2.save()
            #login(request, authenticate(username=username, password=raw_password))
            registered = True
            print(user_form['username'])

    else:
        print("Not Validated")
        user_form = RegistrationForm()
        user_form2 = RegistrationForm2()
    if registered:
        #return HttpResponse("Logged In")
         #redirect_to = settings.LOGIN_REDIRECT_URL
         return redirect ('/register2/')
         #return reverse ('home:base')
    else:
        return render(request, 'register.html', {'user_form': user_form,'user_form2':user_form2})



def load_slots(request):
    i=0
    doctor_id = request.GET.get('doctor_name')
    date = request.GET.get('date')
    print(date)
    print(doctor_id)
    if(doctor_id!=' 'and date!=' '):
        slot=[]
        slot1=[]
        print("Slots Found")
        doctor=Doctor.objects.filter(First_Name=doctor_id).values('id')[0]['id']    
        slots=Slots.objects.filter(Doctor_id=doctor)
        print(slots)
        for s1 in slots:
            # print(s1)
            slot_id=Slots.objects.filter(Doctor_id=doctor).values('id')[i]['id']
            i=i+1
            print("i=",i)
            print("SLots Id",slot_id)
            appoint=Appointment.objects.filter(Doctor_id=doctor,Slot_Time=slot_id,Date=date)
            print("Appointment",appoint)
            if len(appoint) == 0:
                slot.append(s1)
                print("IN if ",slot)
            else:
                continue
        print("SLots",slot)
        print("Doctor Id",doctor_id)
       
    else:
        print("Slots Not Found")
        slots=Slots.objects.none()
    return render(request, 'slots_dropdown_list_option.html', {'slots': slot})



def load_finalslots(request):
    i=0
    doctor_id = request.GET.get('doctor_name')
    date = request.GET.get('date')
    print(date)
    print(doctor_id)
    if(doctor_id!=' 'and date!=' '):
        slot=[]
        slot1=[]
        print("Slots Found")
        doctor=Doctor.objects.filter(First_Name=doctor_id).values('id')[0]['id']    
        slots=Slots.objects.filter(Doctor_id=doctor)
        print(slots)
        for s1 in slots:
            # print(s1)
            slot_id=Slots.objects.filter(Doctor_id=doctor).values('id')[i]['id']
            i=i+1
            print("i=",i)
            print("SLots Id",slot_id)
            appoint=Appointment.objects.filter(Doctor_id=doctor,Slot_Time=slot_id,Date=date)
            print("Appointment",appoint)
            if len(appoint) == 0:
                slot.append(s1)
                print("IN if ",slot)
            else:
                continue
        print("SLots",slot)
        print("Doctor Id",doctor_id)
       
    else:
        print("Slots Not Found")
        slots=Slots.objects.none()
    return render(request, 'slots_dropdown_list_option.html', {'slots': slot})




'''
Error Time 
# value2.datetime.strptimestrftime('%H:%M:%S')
            # datetime.datetime.strptime(value2, '%H:%M p.m.').time()
            # dt = time.strptime(value2, "%H:%M p.m.")
            # print("DT++",dt)
            # ft=dt.tm_hour+dt.tm_min
            # print(ft)
            # value2.strftime('%H:%M:%S')
            # value2.time()


def bookdetail(request,pk):
    return HttpResponse("HELLO WORLD")
    post = get_object_or_404(Author, pk=pk)
    print(post.id)
    ans_list = Author.objects.filter(id=post.id)
    return render(request,'bookdetial.html',context={'ans_dict':ans_list})

 # Create your views here.
def show(request):
    return HttpResponse('HELLO')
'''