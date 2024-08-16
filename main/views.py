from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

@login_required
def debts(request):
    client = Client.objects.filter(user=request.user)
    context = {
        'clients': client.order_by('-debt'),
        'all_debt': sum([i.debt for i in client.filter(debt__gt=0)]),
    }
    return render(request, 'debts.html', context)

@login_required
def add(request):
    name = request.POST.get('name')
    debt = request.POST.get('debt')
    Client.objects.create(
        user=request.user,
        name=name,
        debt=int(debt),
    )
    return redirect('debts')

@login_required
def edit(request, id):
    client = Client.objects.get(id=id)
    client.name = request.POST.get('name')
    client.save()
    return redirect('detail', client.id)

@login_required
def delete(request, id):
    client = Client.objects.get(id=id)
    client.delete()
    return redirect('debts')

# to'lov qilish
@login_required
def plus(request, id):
    client = Client.objects.get(id=id)
    summa = request.POST.get('summa')
    client.debt -= int(summa)
    Payment.objects.create(
        summa=int(summa),
        client=client,
        type=1
    )
    client.save()
    return redirect('debts')

# qarz olish
@login_required
def minus(request, id):
    client = Client.objects.get(id=id)
    summa = request.POST.get('summa')
    client.debt += int(summa)
    Payment.objects.create(
        summa=int(summa),
        client=client,
        type=2
    )
    client.save()
    return redirect('debts')

@login_required
def detail(request, id):
    sd = request.GET.get('sd')
    ed = request.GET.get('ed')
    client = Client.objects.get(id=id)
    if client.user != request.user:
        return redirect('/')
    payments = Payment.objects.filter(client=client)
    if sd and ed:
        payments = payments.filter(date__date__gte=sd, date__date__lte=ed)
    else:
        payments = payments.filter(date__date__gte=datetime.now().date().replace(day=1))
    context = {
        'client': client,
        'payments': payments.order_by('-date'),
        'sd': sd,
        'ed': ed,
    }
    return render(request, 'detail.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')  # Redirect to a home page or any other page
        else:
            messages.error(request, 'Noto\'g\'ri login yoki parol')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/')