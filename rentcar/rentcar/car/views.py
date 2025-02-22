from django.shortcuts import render
from .models import Car
from django.db.models import Q



# fake

from django.shortcuts import render,redirect
from django.contrib import messages
# from .models import Product,Cart,CartItem,CustomUser,OrderItem,Order,Category,Address,Material
from django.http import HttpResponseRedirect

from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect

from django.contrib.auth import logout
from django.contrib.auth import authenticate,login
from django.contrib.auth import update_session_auth_hash

from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

from django.db.models import Q
from django.http import HttpResponse
from decimal import Decimal

from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import User

from .models import Address, CartItem
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Order, OrderItem ,Cart,CartItem,Address,Feedback
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.conf import settings




# Create your views here.
from django.db.models import Q
from django.shortcuts import render
from .models import Car  # Ensure you're importing the Car model
from django.db.models import Q
from django.shortcuts import render
from .models import Car

from django.shortcuts import render
from django.db.models import Q
from .models import Car, Location

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Profile, Car, Location, Feedback, CartItem
from django.contrib import messages
from django.db.models import Q



@login_required
def index(request):
    # Handle feedback form submission
    if request.method == 'POST':
        message = request.POST.get('message')  # Get the feedback message
        if message:  # Check if a message was provided
            Feedback.objects.create(user=request.user, message=message)
            messages.success(request, 'Thank you for your response')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # Redirect back to the page
    
    # Profile and car-related logic
    profile = Profile.objects.filter(user=request.user).first()
    
    if profile and not profile.location:  # Check if profile location is empty
        profile_incomplete = True
    else:
        profile_incomplete = False
    
    # Handle car search and filtering logic
    search = request.GET.get('search')
    location_name = request.GET.get('location')
    
    cars = Car.objects.all()
    
    if search:
        cars = cars.filter(Q(car_name__icontains=search))
    
    if location_name and location_name != 'Location':
        cars = cars.filter(location__name__iexact=location_name)
    
    locations = Location.objects.all()
    
    # Location-based filtering for user's profile
    if profile and profile.location:
        location_obj = Location.objects.filter(name=profile.location).first()
        if location_obj:
            lbased = Car.objects.filter(location=location_obj)
        else:
            lbased = Car.objects.none()
    else:
        lbased = Car.objects.none()

    # Get the number of items in the user's cart
    if request.user.is_authenticated:
        user_cart = CartItem.objects.filter(cart__user=request.user)
        cart_count = user_cart.count()
    else:
        cart_count = 0
    
    feedback = Feedback.objects.all()
    
    # Prepare the context to pass to the template
    context = {
        'cars': cars,
        'search': search,
        'feedback': feedback,
        'location': location_name,
        'locations': locations,
        'lbased': lbased,
        'profile_incomplete': profile_incomplete,
        'cart_count': cart_count,  # Add cart count to the context
    }
    
    return render(request, "index.html", context)



def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Fetch the user based on the username
        user_obj = User.objects.filter(username=username).first()

        if not user_obj:
            messages.warning(request, 'Account not found')
            return redirect(request.META.get('HTTP_REFERER'))  # Redirect back if user not found

        # Authenticate the user
        user_authenticated = authenticate(request, username=username, password=password)

        if not user_authenticated:
            messages.warning(request, 'Invalid password')
            return redirect(request.META.get('HTTP_REFERER'))  # Redirect back if authentication fails

        # Log the user in
        login(request, user_authenticated)

        # Check if the logged-in user has a profile
        if Profile.objects.filter(user=user_authenticated).exists():
            return redirect('index')  # Redirect to index if profile exists
        else:
            return redirect('profile_create')  # Redirect to profile creation if no profile exists

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect(index)

def register_view(request):
    if request.method == 'POST':
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user with the provided email already exists
        user_exists = User.objects.filter(email=email).exists()

        if user_exists:
            messages.warning(request, 'User with this email already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # Create a new CustomUser
        user = User.objects.create(username=username, email=email,first_name=firstname,last_name=lastname)
        user.set_password(password)
        user.save()

        # Redirect to the login page
        return redirect('login')

    # If the request method is not POST, render the registration page
    return render(request, 'register.html')


def car_list(request):
    # Retrieve all cars from the database
    cars = Car.objects.all()
    
    # Pass the cars to the template
    return render(request, 'about.html', {'cars': cars})


from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import CartItem, Cart
@login_required
def cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_price = 0

    for cart_item in cart_items:
        cart_item.total_price = cart_item.car.price * cart_item.days  # Update to use days
        total_price += cart_item.total_price

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_cart_items': cart_items.count(),
    }
    return render(request, 'shoping-cart.html', context)

@require_POST
def update_days(request):
    cart_item_id = request.POST.get('cart_item_id')
    days = request.POST.get('days')

    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.days = days  # Update the days
        cart_item.save()
        return JsonResponse({'status': 'success', 'days': cart_item.days})
    except CartItem.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Cart item not found'}, status=404)



from django.http import JsonResponse
from .models import CartItem

from django.http import JsonResponse
from .models import CartItem

def update_cart_item(request, cart_item_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        days = data.get('days')

        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
            cart_item.days = days  # Update days
            cart_item.save()  # Save changes

            return JsonResponse({'success': True, 'message': 'Days updated successfully!'})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Cart item not found.'})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})


def remove_from_cart(request,cart_item_id):
    cart_item=get_object_or_404(CartItem,id=cart_item_id)
    cart_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cancel(request,order_item_id):
    order_item=get_object_or_404(OrderItem,id=order_item_id)
    order_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def add_to_cart(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, car=car)

    # Set default values
    cart_item.quantity += 1  # Increment quantity
    cart_item.days = 1  # Set initial days or however you want to handle it
    cart_item.save()

    messages.success(request, 'Product added to the cart')
    return redirect(request.META.get('HTTP_REFERER')) # Redirect to cart or wherever needed


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile

from django.contrib import messages

@login_required
def profile_create(request):
    # Check if the user already has a profile
    if Profile.objects.filter(user=request.user).exists():
        return redirect('profile')  # Redirect if profile already exists

    if request.method == 'POST':
        # Get the form data
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        location = request.POST.get('location')
        proof = request.FILES.get('proof')  # Handle file upload

        # Ensure no fields are empty (basic validation)
        if not all([name, phone_number, address, location]):
            messages.error(request, 'Please fill out all fields.')
            return render(request, 'profile_create.html')

        # Additional validation for phone number
        if not phone_number.isdigit() or len(phone_number) < 10:
            messages.error(request, 'Invalid phone number.')
            return render(request, 'profile_create.html')

        # Create and save the new profile
        profile = Profile(
            user=request.user,
            name=name,
            phone_number=phone_number,
            address=address,
            location=location,
            proof=proof  # Save the uploaded file
        )
        profile.save()
        messages.success(request, 'Profile created successfully.')
        return redirect('profile')  # Redirect to the relevant page

    return render(request, 'profile_create.html')


from django.shortcuts import get_object_or_404
from django.contrib import messages

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        # Update profile fields if new values are provided
        profile.name = request.POST.get('name', profile.name)
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        profile.address = request.POST.get('address', profile.address)
        profile.location = request.POST.get('location', profile.location)
        
        # Handle file upload for proof
        if 'proof' in request.FILES:
            profile.proof = request.FILES['proof']

        # Save the updated profile
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')  # Redirect to profile view after saving

    return render(request, 'edit_profile.html', {'profile': profile})



@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'profile.html', {'profile': profile})


from datetime import datetime, timedelta

from datetime import datetime, date
from decimal import Decimal
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem, Address


from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

def start_order(request):
    if request.method == "POST":
        # Validate and retrieve address and cart
        try:
            address = Address.objects.get(user=request.user)
        except Address.DoesNotExist:
            messages.error(request, "Please add your address before proceeding.")
            return redirect('checkout')

        user_cart = Cart.objects.filter(user=request.user).first()
        if not user_cart:
            messages.error(request, "No cart found for this user.")
            return redirect('cart')

        cart_items = CartItem.objects.filter(cart=user_cart)
        if not cart_items.exists():
            messages.error(request, "No items in cart.")
            return redirect('cart')

        # Parse `start_date`, `end_date`, and `aadhar_number` from request
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        aadhar_number = request.POST.get('aadhar_number')

        # Validate Aadhar number (12 digits)
        if not aadhar_number or not aadhar_number.isdigit() or len(aadhar_number) != 12:
            messages.error(request, "Please enter a valid 12-digit Aadhar number.")
            return redirect('checkout')

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            today = date.today()
            
            if start_date < today:
                messages.warning(request, "Start date cannot be earlier than today.")
                return redirect('checkout')
            if end_date < today:
                messages.warning(request, "End date cannot be earlier than today.")
                return redirect('checkout')
            if start_date > end_date:
                messages.warning(request, "End date must be on or after the start date.")
                return redirect('checkout')
        except ValueError as e:
            messages.error(request, f"Invalid date input: {e}")
            return redirect('checkout')

        # Calculate total price and cost
        total_price = sum(cart_item.car.price * cart_item.days for cart_item in cart_items)
        shipping_option = request.POST.get('shipping-option', 'Standard Delivery')
        speed_delivery_cost = Decimal('16.00') if shipping_option == 'Speed Delivery' else Decimal('0.00')
        total_cost = total_price + speed_delivery_cost

        # Create order and order items
        try:
            order = Order.objects.create(
                user=request.user,
                first_name=address.first_name,
                last_name=address.last_name,
                email=address.email,
                address=address.address,
                zipcode=address.zipcode,
                shipping_method=shipping_option,
                shipping_cost=speed_delivery_cost,
                total_cost=total_cost,
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    car=item.car,
                    price=item.car.price * item.days,
                    quantity=item.days,
                    days=item.days,
                    start_date=start_date,
                    end_date=end_date,
                    aadhar_number=aadhar_number,  # Save the Aadhar number
                )

            cart_items.delete()
            messages.success(request, "Order placed successfully!")
            return redirect('wishlist')  # Redirect after successful order
        except Exception as e:
            messages.error(request, f"An error occurred while placing the order: {e}")
            return redirect('cart')

    return redirect('checkout')




def wishlist(request):
    return render(request, 'payment.html')

@login_required
def address(request):
    try:
        address = Address.objects.get(user=request.user)  # Get the unique address for the user
    except Address.DoesNotExist:
        address = None  # If no address exists, set address to None

    if request.method == "POST":
        # Fetch data from form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address_field = request.POST.get('address')  # Avoid name conflict with 'address' variable
        zipcode = request.POST.get('zipcode')

        if address:
            # Update existing address
            address.first_name = first_name
            address.last_name = last_name
            address.email = email
            address.address = address_field
            address.zipcode = zipcode
            address.save()
            messages.success(request, 'Address updated successfully!')
        else:
            # Create new address if none exists
            Address.objects.create(user=request.user, first_name=first_name, last_name=last_name, email=email, address=address_field, zipcode=zipcode)
            messages.success(request, 'Address added successfully!')

        return redirect('address')  # Redirect to the same page to avoid resubmission of form

    # Prepare form data if address exists; otherwise, use empty strings
    form_data = {
        'first_name': address.first_name if address else '',
        'last_name': address.last_name if address else '',
        'email': address.email if address else '',
        'address': address.address if address else '',
        'zipcode': address.zipcode if address else '',
    }

    return render(request, 'address.html', {'address': address, 'form_data': form_data})
@login_required
def checkout(request):
    try:
        address = Address.objects.get(user=request.user)
    except Address.DoesNotExist:
        address = None  # Handle case where no address exists for the user

    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_price = 0

    for cart_item in cart_items:
        cart_item.total_price = cart_item.car.price * cart_item.days  # Update to use days
        total_price += cart_item.total_price
    

    # Populate form data based on whether an address exists
    form_data = {
        'first_name': address.first_name if address else '',
        'last_name': address.last_name if address else '',
        'email': address.email if address else '',
        'address': address.address if address else '',
        'zipcode': address.zipcode if address else '',
    }

    context = {
        'cart_items': cart_items,
        'address': address,
        'form_data': form_data,
        
        
        
        'total_price': total_price,
        'total_cart_items': cart_items.count(),

    }
    return render(request, 'checkout.html', context)
# Ensure these are imported correctly
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

@login_required
def vieworder(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('action')

        if order_id:
            order = get_object_or_404(OrderItem, pk=order_id)
            if new_status in [status[0] for status in OrderItem.STATUS_CHOICES]:  # Check if new status is valid
                order.status = new_status
                order.save()
                messages.success(request, f"Order status updated to {new_status}.")
                return redirect('view_order')  # Make sure this matches your URL name
        else:
            messages.error(request, "Order ID not provided.")

    # For buyers: List OrderItems linked to Orders made by the user
    buyer_orders = OrderItem.objects.filter(order__user=request.user).order_by('-created_at')
    seller_orders = OrderItem.objects.filter(car__user=request.user).order_by('-created_at')

    context = {
        'buyer_orders': buyer_orders,
        'seller_orders': seller_orders,
    }

    return render(request, 'order-page.html', context)



def adminconsumer(re):
    farmer = User.objects.all()
    return render(re,'admin_view_cunsumer.html', {'farmer': farmer})

def deletefeedback(re):
    feedback = Feedback.objects.all()
    return render(re,'admin_feedback.html', {'feedback': feedback})

def remove_from_feedback(request,feedback_id):
    feed=get_object_or_404(Feedback,id=feedback_id)
    feed.delete()
    messages.success(request, 'Feedback Deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def adminproduct(re):
    cars=Car.objects.all()
    return render(re,'admin_view_product.html',{'cars': cars})

def adminorder(re):
    order=OrderItem.objects.all().order_by('-created_at')
    return render(re,'admin_view_order.html',{'order': order})

def about(re):
    return render(re,'about.html')

def contacts(re):
    return render(re,'contact.html')

def product(request):
    if request.method == 'POST':
        if 'loca_name' in request.POST:  # Handling location creation
            loca_name = request.POST.get('loca_name')
            if not Location.objects.filter(name=loca_name).exists():
                Location.objects.create(name=loca_name)
                messages.success(request, 'Location Created Successfully!')
            else:
                messages.error(request, 'Location already exists.')
        
        elif 'car_name' in request.POST:  # Handling car creation
            car_name = request.POST.get('car_name')
            car_type = request.POST.get('car_type')
            price = request.POST.get('price')
            kilometers_drove = request.POST.get('kilometers_drove')
            seats = request.POST.get('seats')
            stock_quantity = request.POST.get('stock_quantity')
            car_image = request.FILES.get('car_image')
            location_id = request.POST.get('location')  # Fetching location by id
            
            # Check if the location exists by id
            try:
                location = Location.objects.get(id=location_id)
            except Location.DoesNotExist:
                messages.error(request, 'Location does not exist.')
                return redirect('product')

            Car.objects.create(
                user=request.user,
                car_name=car_name,
                car_type=car_type,
                price=price,
                location=location,
                kilometers_drove=kilometers_drove,
                seats=seats,
                stock_quantity=stock_quantity,
                car_image=car_image
            )
            messages.success(request, 'Car Created Successfully!')
        
        return redirect('product')
    
    locations = Location.objects.all()
    products = Car.objects.filter(user=request.user)
    return render(request, 'product.html', {'locations': locations, 'products': products})

