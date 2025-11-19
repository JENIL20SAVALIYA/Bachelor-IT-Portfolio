from flask import Flask, render_template, redirect, url_for, flash, send_file, request
from extensions import db, login_manager  # Import db and login_manager from extensions
from flask_login import login_user, logout_user, login_required, current_user
from io import BytesIO
import qrcode
from forms import LoginForm, RegistrationForm, PersonalDetailsForm
from models import User
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Configurations
import os
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'changeme')
print(f"SECRET_KEY type: {type(app.config['SECRET_KEY'])}")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

from flask_mail import Mail

# Email configuration for IONOS
app.config['MAIL_SERVER'] = 'smtp.ionos.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'm117466458-165639547'  # Ensure this is correct
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'changeme')  # Set MAIL_PASSWORD in your environment
app.config['MAIL_DEFAULT_SENDER'] = 'yourqr@qrcode.earth'

# Initialize Flask-Mail extension
mail = Mail(app)


# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Generate QR code from vCard data
def generate_qr_code(data):
    qr_img = qrcode.make(data)
    return qr_img


# Route to generate QR code with vCard data
@app.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    if request.method == 'POST':
        try:
            # Get form data
            full_name = request.form.get('full_name')
            first_name, last_name = (full_name.split(' ', 1) + [""])[:2]
            company_name = request.form.get('company_name')
            email_address = request.form.get('email_address')
            mobile_number = request.form.get('mobile_number')
            facebook = request.form.get('facebook')
            linkedin = request.form.get('linkedin')
            instagram = request.form.get('instagram')
            premises_address = request.form.get('premises_address')

            # Construct the vCard data with all fields
            vcard_data = f"""BEGIN:VCARD
VERSION:3.0
N:{last_name};{first_name};;;
FN:{first_name} {last_name}
ORG:{company_name}
EMAIL:{email_address}
TEL:{mobile_number}
ADR:;;{premises_address}
URL:{facebook}
URL:{linkedin}
URL:{instagram}
END:VCARD"""

            # Generate the QR code image from vCard data
            print("Generating QR code...")  # Debugging statement
            img = generate_qr_code(vcard_data)

            # Prepare the image to be sent as a response
            img_io = BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)

            # Create a meaningful filename using the full name
            filename = f"{full_name.replace(' ', '_')}_contact_qr.png"

            # Send the QR code image as a downloadable file
            print("QR code generated successfully.")  # Debugging statement
            return send_file(img_io, mimetype='image/png', as_attachment=True, download_name=filename)

        except Exception as e:
            print(f"Error occurred during QR code generation: {e}")
            flash("An error occurred while generating the QR code.", 'danger')
            return redirect(url_for('personal_details'))
    else:
        # If the method is GET, show an error or redirect
        flash('Method not allowed for this endpoint.', 'danger')
        return redirect(url_for('personal_details'))

# Landing page route
@app.route('/')
def index():
    form = LoginForm()  # Create an instance of the login form
    return render_template('index.html', form=form)  # Connects with index.html


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('personal_details'))  # Redirect after login
        else:
            flash('Invalid email or password', 'danger')
    return render_template('index.html', form=form)


# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if not existing_user:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email is already registered. Please use a different one.', 'danger')
    return render_template('register.html', form=form)


# Personal details route
@app.route('/personal_details', methods=['GET', 'POST'])
@login_required
def personal_details():
    form = PersonalDetailsForm()
    if form.validate_on_submit():
        return redirect(url_for('generate'))  # Redirect to the generate route to create the QR code
    return render_template('personal_details.html', form=form)


# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

from flask_mail import Message
from forms import RequestResetForm, ResetPasswordForm

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', form=form)

from flask_mail import Message
from flask import url_for

def send_reset_email(user):
    # Generate the reset token
    token = user.get_reset_token()

    # Create the email message
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',  # You can use your email address here
                  recipients=[user.email])    # Send email to the user's registered email address

    # The body of the email
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''

    # Send the email
    mail.send(msg)

from flask_mail import Message
from flask import Flask


@app.route('/test_email')
def test_email():
    try:
        msg = Message(
            'Test Email from Flask',
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=['aniza.khan529@gmail.com']
        )
        msg.body = 'This is a test email sent from Flask using IONOS SMTP settings.'

        # Debug output before sending
        print(f"Sending email to {msg.recipients} from {msg.sender}")

        mail.send(msg)

        # If email sending is successful
        print("Email sent successfully")
        return 'Test email sent successfully!'
    except Exception as e:
        # Output error for debugging
        print(f"An error occurred: {e}")
        return 'Failed to send test email.'


if __name__ == '__main__':
    app.run(debug=True)