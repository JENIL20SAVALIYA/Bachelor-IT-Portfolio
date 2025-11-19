from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CSVUploadForm #UserRegistrationForm,
from .models import QRCode
import qrcode

# accounts/views.py

from django.shortcuts import render

def home(request):
    """
    Home view function to render the home page.
    """
    return render(request, 'accounts/home.html')


# views.py

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .tokens import email_verification_token

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'accounts/activation_invalid.html')


# views.py

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .tokens import email_verification_token

# views.py

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .tokens import email_verification_token

from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from .tokens import email_verification_token


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate the account until email is verified
            user.save()

            # Email verification token generation
            current_site = get_current_site(request)
            subject = 'Verify your email address'
            message = render_to_string('accounts/verify_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': email_verification_token.make_token(user),
            })

            try:
                # Attempt to send the email
                send_mail(subject, message, 'your_verified_sender_email@example.com', [user.email])
                print("Email sent successfully")
            except Exception as e:
                print(f"Error sending email: {e}")

            # Show a success page or message indicating that the verification email was sent
            return render(request, 'accounts/verification_sent.html')
        else:
            print("Form is not valid:", form.errors)  # Debugging form errors
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/registration.html', {'form': form})


'''def register(request):
    """
    View to handle user registration.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/registration.html', {'form': form})

from django.contrib.auth.forms import AuthenticationForm
'''
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

from django.contrib import messages
from django.shortcuts import redirect

# accounts/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def profile(request):
    """
    View to display the user's profile information.
    """
    return render(request, 'accounts/profile.html', {'user': request.user})


def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home')


# views.py
import os
import qrcode
from django.core.files.base import ContentFile
import csv

import qrcode
from django.core.files.base import ContentFile
import csv
from io import BytesIO
from django.contrib.auth.decorators import login_required

import csv
from io import BytesIO
from django.core.files.base import ContentFile
import qrcode
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import QRCode
from django.conf.urls.static import static


@login_required
def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)

            # Extract the header row to use as titles
            headers = next(reader, None)  # Assuming the first row is the header

            for row in reader:
                attributes = [f"{headers[i]}: {row[i]}" for i in range(len(headers))]
                row_data = '\n'.join(attributes)

                # Create and save the QRCode object with the encoded data
                qr_code = QRCode(name=row[0], data=row_data, user=request.user)
                qr_code.save()

                # Generate a URL pointing to the display page for this QR code
                # In your views.py where you generate the QR code
                qr_code_url = f"https://www.csvtoqrcode.com/display_qr_data/{qr_code.id}/"
                # Generate the QR code with the URL
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4
                )
                qr.add_data(qr_code_url)
                qr.make(fit=True)

                # Create an image from the QRCode object
                img = qr.make_image(fill_color="black", back_color="white")

                # Save the image to an in-memory buffer
                img_buffer = BytesIO()
                img.save(img_buffer, format='PNG')
                img_buffer.seek(0)  # Rewind the buffer to the beginning

                # Save the QR code image in the database
                img_name = f"{row[0]}_{row[1]}.png"  # Use the first and second columns for naming
                img_content = ContentFile(img_buffer.read())
                qr_code.filename.save(img_name, img_content, save=True)

            messages.success(request, "CSV uploaded successfully, and QR codes were generated.")
            return redirect('view_qr_codes')
    else:
        form = CSVUploadForm()

    return render(request, 'accounts/upload_csv.html', {'form': form})

'''
@login_required
def upload_csv(request):
    """
    View to handle CSV uploads and generate QR codes.
    The uploaded CSV is parsed, and for each row, a QR code is generated and saved.
    """
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            # Reading the CSV file
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)

            # Skip the header row
            next(reader, None)

            for row in reader:
                # Assuming that the first column in each row is the identifier/name
                name = row[0]

                # Generate the QR code
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
                qr.add_data(name)
                qr.make(fit=True)

                # Create an image from the QRCode object
                img = qr.make_image(fill_color="black", back_color="white")

                # Save the QR code image in memory
                img_name = f"{name}.png"
                img_content = ContentFile(img.tobytes())

                # Save the QR code image in the database
                qr_code = QRCode(name=name)
                qr_code.filename.save(img_name, img_content, save=True)

            messages.success(request, "CSV uploaded successfully, and QR codes were generated.")
            return redirect('view_qr_codes')
    else:
        form = CSVUploadForm()

    return render(request, 'accounts/upload_csv.html', {'form': form})
'''
# views.py
from django.conf import settings
from django.http import HttpResponse
from django.core.files.storage import default_storage
import zipfile

# views.py
# views.py
from django.contrib.auth.decorators import login_required


def view_qr_codes(request):
    """
    View to display all the generated QR codes for the logged-in user.
    """
    # Get only the QR codes generated by the logged-in user
    qr_codes = QRCode.objects.filter(user=request.user)
    return render(request, 'accounts/view_qr_codes.html', {'qr_codes': qr_codes})


'''
def view_qr_codes(request):
    """
    View to display all the generated QR codes.
    Allows the user to see individual QR codes and download them all as a ZIP file.
    """
    # Get all the QR codes from the database
    qr_codes = QRCode.objects.all()
    return render(request, 'accounts/view_qr_codes.html', {'qr_codes': qr_codes})
'''
# views.py
import io
@login_required
def download_all_qr_codes(request):
    """
    View to download all generated QR codes as a ZIP file.
    Creates a ZIP file containing all QR code images in the database.
    """
    # Create an in-memory file
    buffer = io.BytesIO()

    # Create a zip file in the buffer
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        # Get all QR codes from the database
        qr_codes = QRCode.objects.all()
        for qr_code in qr_codes:
            # Get the file path of each QR code
            qr_path = qr_code.filename.path
            # Add the QR code to the zip file
            zip_file.write(qr_path, os.path.basename(qr_path))

    buffer.seek(0)

    # Create the response to download the ZIP file
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=qr_codes.zip'

    return response

# accounts/views.py
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import QRCode

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import QRCode
@login_required
def download_qr_code(request, qr_code_id):
    qr_code = get_object_or_404(QRCode, id=qr_code_id, user=request.user)
    response = HttpResponse(qr_code.filename, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="{qr_code.filename.name}"'
    return response

from django.shortcuts import render, get_object_or_404
from .models import QRCode

from django.shortcuts import render, get_object_or_404
from .models import QRCode

from django.shortcuts import render, get_object_or_404
from .models import QRCode


def display_qr_data(request, qr_code_id):
    # Fetch the QRCode object by ID
    qr_code = get_object_or_404(QRCode, id=qr_code_id)

    # Retrieve the data that was encoded in the QR code
    data = qr_code.data

    # Render the template with the data
    return render(request, 'accounts/display_qr_data.html', {'data': data})


