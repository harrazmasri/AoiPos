from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from aoiPosApp.forms import LoginForm, RegisterForm, ProductForm
from aoiPosApp.models import Product
from django.core.files.storage import default_storage

# Create your views here.
def login(request):
    if request.session.get('user_id'):
        return redirect('/pos')

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.user_cache
            
            request.session['user_id'] = user.id
            request.session['user_username'] = user.username
            
            return redirect('/pos')
    else:
        form = LoginForm()

    return render(request, 'aoiPosApp/login.html', {'form': form})

def register (request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            request.session['user_id'] = user.id
            request.session['user_username'] = user.username
            return redirect('pos')

    return render(request, 'aoiPosApp/register.html', {
        'form': form,
    })

def pos (request):
    return render(request, 'aoiPosApp/pos-dashboard.html')

def catalogue (request):
    return render(request, 'aoiPosApp/catalogue.html')

def view(request, id=None):
    print("========== CATALOGUE CREATE ==========")
    print("METHOD:", request.method)
    print("POST:", request.POST)
    print("FILES:", request.FILES)

    product = None

    if id:
        product = get_object_or_404(Product, pk=id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        print("FORM VALID:", form.is_valid())
        print("FORM ERRORS:", form.errors)
        print("FORM NON FIELD ERRORS:", form.non_field_errors())

        if form.is_valid():
            product = form.save()

            print("PRODUCT CREATED:", product.id)
            
            return redirect('product-view', id=product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'aoiPosApp/view.html', {
        'form': form,
        'product': product,
    })

def summary (request):
    return render(request, 'aoiPosApp/summary.html')


def logout (request):
    request.session.flush()
    return redirect('login')

#test