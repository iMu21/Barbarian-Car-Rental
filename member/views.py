from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import memberWebsite, pendingAccount,memberBasic,memberPhoneNumber ,websiteType
from django.conf import settings
from django.core.mail import send_mail
import uuid
from django.contrib.auth import authenticate,login,logout
from shop.models import SuperCategory


def profile(request):
    if request.user.is_authenticated:
        member  = memberBasic.objects.all().get(username=request.user)
        memberPhone = [] 
        if memberPhoneNumber.objects.filter(userName=request.user).first():
            memberPhone = memberPhoneNumber.objects.all().filter(userName=request.user)
        else:
            pass  
        website = []
        if memberWebsite.objects.filter(userName = request.user).first():
            website = memberWebsite.objects.all().filter(userName=request.user)
        else:
            pass   
        superCategory = SuperCategory.objects.all()
        params={'superCategory': superCategory,'member':member,'memberPhone':memberPhone,'website':website }
        return render(request,'profile.html',params)
    else:
        superCategory = SuperCategory.objects.all()
        params = {'superCategory': superCategory}
        return redirect('logIn',params)     

def profileEdit(request):
    superCategory = SuperCategory.objects.all()
    member  = memberBasic.objects.all().get(username=request.user)
    params = {'superCategory': superCategory,'member':member}
    return render(request,'profileEdit.html',params)

def profileEdited(request):
    firstName = request.POST.get('firstName')
    lastName = request.POST.get('lastName')
    memberDivision = request.POST.get('memberDivision')
    memberDistrict = request.POST.get('memberDistrict')
    about = request.POST.get('about')
    memberBirthDate = request.POST.get('memberBirthDate')
    if memberBasic.objects.filter(username=request.user).first():
        obj = memberBasic.objects.get(username=request.user)
        obj.firstName = firstName
        obj.lastName = lastName
        obj.memberDivision = memberDivision
        obj.memberDistrict = memberDistrict
        obj.memberBirthDate = memberBirthDate
        obj.about = about
        obj.save()
    return redirect ('profile')


def phoneDelete(request):
    phoneid = request.GET.get('phoneid')
    if memberPhoneNumber.objects.filter(id=phoneid).first():
        phone = memberPhoneNumber.objects.get(id=phoneid)
        phone.delete()
        messages.warning(request, 'Your number has been deleted.') 
    else:
        messages.warning(request, 'The number you have requested to delete is invalid.')       
    superCategory = SuperCategory.objects.all()
    params = {'superCategory': superCategory}
    return redirect ('profile',params)

def phoneEdit(request):
    phoneid = request.GET.get('phoneid')
    if memberPhoneNumber.objects.filter(id=phoneid).first():
        phone = memberPhoneNumber.objects.get(id=phoneid)
        superCategory = SuperCategory.objects.all()
        params = {'superCategory': superCategory,'phone':phone}
        return render (request,'phoneEdit.html',params) 
    messages.warning(request, 'The number you have requested to edit is invalid.')
    return redirect ('profile')

def phoneAdd(request):
    superCategory = SuperCategory.objects.all()
    params = {'superCategory': superCategory}
    return render (request,'phoneAdd.html',params)        

def phoneEdited(request):
    phoneid = request.POST.get('phoneid')
    correctPhone = request.POST.get('correctPhone')
    if memberPhoneNumber.objects.filter(id=phoneid).first():
        phone = memberPhoneNumber.objects.get(id=phoneid)
        phone.phoneNumber = correctPhone
        phone.save()
        messages.warning(request, 'Your phone number has been updated.') 
    return redirect ('profile')  

def phoneAdded(request):
    if request.method =="POST": 
        phone = request.POST.get('phone') 
        phoneObj = memberPhoneNumber.objects.create(userName=request.user ,phoneNumber=phone ) 
        phoneObj.save()
        messages.warning(request, 'Your phone number has been saved.') 
    print("hosse na")
    return redirect ('profile')


def websiteDelete(request):
    websiteid = request.GET.get('websiteid')
    if memberWebsite.objects.filter(id=websiteid).first():
        website = memberWebsite.objects.get(id=websiteid)
        website.delete()
    messages.warning(request, 'The website adress you have requested to delete is invalid.') 
    return redirect ('profile')    



def websiteEdit(request):
    websiteid = request.GET.get('websiteid')
    if memberWebsite.objects.filter(id=websiteid).first():
        website = memberWebsite.objects.get(id=websiteid)
        superCategory = SuperCategory.objects.all()
        params = {'superCategory': superCategory,'website':website}
        return render (request,'websiteEdit.html',params) 
    messages.warning(request, 'The website address you have requested to edit is invalid.') 
    return redirect ('profile') 

def websiteEdited(request):
    websiteid = request.POST.get('websiteid')
    correctAddress = request.POST.get('correctaddress')
    correctType = request.POST.get('correcttype')
    if memberWebsite.objects.filter(id=websiteid).first():
        website = memberWebsite.objects.get(id=websiteid)
        website.address = correctAddress
        website.about = correctType
        website.save()
        messages.warning(request, 'Your '+str(website.type)+'adress has been updated.') 
    return redirect ('profile')

def websiteAdd(request):
    types = websiteType.objects.all()
    superCategory = SuperCategory.objects.all()
    params = {'superCategory': superCategory,"websiteType":types}
    return render (request,'websiteAdd.html',params )  

def websiteAdded(request):
    if request.method =="POST":
        address = request.POST.get('address')
        typeid = request.POST.get('typeid')
        websiteObj = memberWebsite.objects.create(userName=request.user , address=address , type = websiteType.objects.get(id=typeid)) 
        websiteObj.save()
        messages.warning(request, 'Your website address has been saved.') 
    return redirect ('profile')



 

def signUp(request):
    superCategory = SuperCategory.objects.all()
    params = {'superCategory': superCategory}
    return render(request,'signUp.html',params)

def logIn(request):
    superCategory = SuperCategory.objects.all()
    params = {'superCategory': superCategory}   
    return render(request,'logIn.html',params)    

def logOut(request):   
    logout(request) 
    return redirect('logIn')

def logInAttempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('logIn')
        
        
        profile_obj = pendingAccount.objects.filter(username = username ).first()

        if  profile_obj :
            messages.success(request, 'Profile is not verified, check your mail.')
            return redirect('logIn')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('logIn')
        
        login(request , user)
        return redirect('profile')
    superCategory = SuperCategory.objects.all()
    params = {'superCategory': superCategory}
    return render(request , 'logIn.html',params)

def signUpConfirmation(request):
    if request.method=='POST':
        username = request.POST.get('username')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        retypePassword = request.POST.get('retypePassword') 
        if User.objects.filter(username = username).first(): 
            messages.success(request, 'This username is taken before.')
            return redirect('signUp')

        if User.objects.filter(email = email).first(): 
            messages.success(request, 'This email is already in used.')
            return redirect('signUp')

        if password!=retypePassword:
            messages.success(request, "Re-entered password doesn't match.")
            return redirect('signUp')
        if len(password)<8:
            messages.success(request, "Password is too short.")
            return redirect('signUp')
        token= str(uuid.uuid4() ) 
        obj = pendingAccount.objects.create(username=username,firstName=firstName,lastName=lastName,email=email,authToken=token,password=password)
        obj.save() 
        sendMail(email,token)
    superCategory = SuperCategory.objects.all()
    params = {'superCategory': superCategory}
    return render(request,'signUpConfirmation.html',params )  


def sendMail(email,token):
    subject = "Email confirmation for KnowledgeHub"  
    message = f"This is your verifaction code:{token}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = {email}
    send_mail(subject,message,email_from,recipient_list)

def  verificationCheck(request):
    token = request.POST.get('token')
    email = request.POST.get('email')
    if pendingAccount.objects.filter(authToken = token,email=email ).first():
        obj = pendingAccount.objects.get(authToken = token ) 
        userObject = User.objects.create(username = obj.username , email = obj.email ) 
        userObject.set_password(obj.password)
        userObject.save()
        memberBasicObject = memberBasic.objects.create(username = userObject,firstName = obj.firstName, lastName = obj.lastName, joinAt = obj.joinAt)
        memberBasicObject.save()
        pendingAccount.objects.filter(email=email).delete()
        pendingAccount.objects.filter(username=userObject.username).delete()
        messages.success(request, "Signed Up successfully. Log In here")
        return redirect('logIn')
    messages.success(request, "Incorrect Email or Verification Code")
    return redirect('signUpConfirmation')    
