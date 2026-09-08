from decimal import Decimal
import json

from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from aoiPOS import settings
from aoiPosApp.forms import LoginForm, RegisterForm, ProductForm, TransactionForm
from aoiPosApp.models import Product, Transaction, TransactionItem, User
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
            request.session['user_role'] = user.role
            
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
    products = Product.objects.all()
    return render(request, 'aoiPosApp/pos-dashboard.html', {'products': products})

def catalogue (request):
    products = Product.objects.all()
    form = ProductForm()

    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('catalogue')

    return render(request, 'aoiPosApp/catalogue.html', {'products': products,'form': form,})

def deleteProduct(request):
    if request.method == "POST":
        prodId = request.POST.get('id')
        product = Product.objects.get(id=prodId)
        if product.image_path:
            product.image_path.delete(save=False)
        product.delete()

    return redirect('catalogue')
    
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

    transactions = Transaction.objects.all().select_related('user').prefetch_related('items__product').order_by('-created_at')

    pageData = {
        'performance': {

        },

        'transactions': transactions,
    }

    return render(request, 'aoiPosApp/summary.html', pageData)


def logout (request):
    request.session.flush()
    return redirect('login')


######### API functions ##########

def getAuthUser(request):
    if request.method == 'GET':
        session_user_id = request.session.get('user_id')
        
        user = User.objects.filter(id=session_user_id).first() if session_user_id else None

        if not user and request.user.is_authenticated:
            user = request.user

        if user:
            data = {
                'authenticated': True,
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
            return JsonResponse(data)
        
        return JsonResponse({
            'authenticated': False,
            'id': '',
            'username': '',
            'email': '',
        }, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def getProductList(request):
    products = Product.objects.all()
    data = []

    for product in products:
        image_url = ""
        if product.image_path:
            image_url = f"{settings.MEDIA_URL}{product.image_path}"

        data.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price) if product.price else 0.0,
            'image_url': image_url,
        })

    return JsonResponse(data, safe=False)


def storeTransaction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # {
            #     "isSuccess": true,
            #     "user": 1,
            #     "cut_price": 25,
            #     "items": [
            #         {
            #             "id": 2,
            #             "name": "davrqa",
            #             "price": 123.55,
            #             "image_url": "/media/products/the-original-image-of-the-monkey-thinking-meme-v0-94pwblzk4caf1_Sf8Gy7q.jpg",
            #             "quantity": 1
            #         }
            #     ]
            # }

            user_id = data.get('user')
            is_success = data.get('isSuccess')
            cart_items = data.get('items', [])
            cut_price = data.get('cut_price', 100.00)

            if not cart_items:
                return JsonResponse(
                    {
                        'status': 'error',
                        'message': 'Cart cannot be empty',
                    }, 
                    status=400,
                )

            user_instance = User.objects.filter(id=user_id).first() if user_id else None

            with transaction.atomic(): # db transaction for rollback
                new_transaction = Transaction.objects.create(
                    user=user_instance,
                    cut_price=cut_price,
                    status=is_success,
                )

                running_total = 0

                for item in cart_items:
                    product_instance = Product.objects.filter(id=item.get('id')).first()

                    unit_price = item.get('price', 0.0)
                    quantity = item.get('quantity', 1)

                    transaction_item = TransactionItem.objects.create(
                        transaction=new_transaction,
                        product=product_instance,
                        product_name=item.get('name', ''),
                        unit_price=unit_price,
                        quantity=quantity
                    )

                    running_total += transaction_item.subtotal

                new_transaction.total_amount = running_total
                discount_factor = Decimal(str(cut_price)) / Decimal('100.00')
                new_transaction.effective_amount = running_total * discount_factor
                new_transaction.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Transaction has been saved',
                'transaction_id': new_transaction.unique_id,
                'total_amount': float(new_transaction.total_amount)
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Invalid JSON body',
                },
                status=400,
            )
        except Exception as e:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': str(e),
                }, 
                status=500
            )