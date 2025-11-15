from django.shortcuts import render, redirect
from .forms import EmployeeForm   # ensure this exists
def home(request):
    return render(request, 'myapp/home.html')
def landing(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_success')
    else:
        form = EmployeeForm()
    return render(request, 'myapp/register.html', {'form': form})
def success_page(request):
    return render(request, 'myapp/success.html')