import flet as ft
import hashlib
import pg8000
import requests
from datetime import datetime

# PostgreSQL connection setup
DB_URL = "postgresql://patient_db_xa13_user:FKIcfjuDn7HCJfOAsIV43pZsUgeSJtYn@dpg-csmbgh3qf0us73fvpjsg-a.oregon-postgres.render.com/patient_db_xa13"

# Replace with your Hugging Face FastAPI URL
FASTAPI_URL = "https://pavankm96-bt-fastapi.hf.space/predict"

# Hash password for storage
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to connect to the PostgreSQL database using pg8000
# Function to connect to the PostgreSQL database using pg8000
def get_db_connection():
    conn = pg8000.connect(
        user="patient_db_xa13_user",
        password="FKIcfjuDn7HCJfOAsIV43pZsUgeSJtYn",
        host="dpg-csmbgh3qf0us73fvpjsg-a.oregon-postgres.render.com",
        database="patient_db_xa13"
    )
    return conn

# Function to calculate age from DOB
def calculate_age(birth_date):
    # If birth_date is a string, convert it to a datetime object
    if isinstance(birth_date, str):
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d")  # Adjust the format as needed

    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

# Main function to define the app's behavior
def main(page: ft.Page):
    page.title = "Authentication App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#101820"  # Gradient from blue to purple

    # Error message placeholders
    login_error_msg = ft.Text("", color="red")
    register_error_msg = ft.Text("", color="red")

    # Define UI fields for login and register sections
    register_email = ft.TextField(label="Email", width=250,bgcolor="white")
    register_username = ft.TextField(label="Username", width=250,bgcolor="white")
    register_password = ft.TextField(label="Password", password=True, width=250,bgcolor="white")
    register_phone = ft.TextField(label="Phone Number", width=250,bgcolor="white")
    # Create TextField components for Day, Month, and Year
    register_dob_day = ft.TextField(label="Day", width=75, keyboard_type=ft.KeyboardType.NUMBER,bgcolor="white")
    register_dob_month = ft.TextField(label="Month", width=75, keyboard_type=ft.KeyboardType.NUMBER,bgcolor="white")
    register_dob_year = ft.TextField(label="Year", width=100, keyboard_type=ft.KeyboardType.NUMBER,bgcolor="white")

    # Create TextField components for Day, Month, and Year
    register_dob_day = ft.TextField(label="Day", width=75, keyboard_type=ft.KeyboardType.NUMBER,bgcolor="white")
    register_dob_month = ft.TextField(label="Month", width=75, keyboard_type=ft.KeyboardType.NUMBER,bgcolor="white")
    register_dob_year = ft.TextField(label="Year", width=100, keyboard_type=ft.KeyboardType.NUMBER,bgcolor="white")

    # Create a container to hold the three parts of the Date (Day, Month, Year)
    register_dob_container = ft.Row(
        [
            register_dob_day,
            register_dob_month,
            register_dob_year
        ],
        alignment=ft.MainAxisAlignment.CENTER  # Use alignment for horizontal centering
    )

    login_email = ft.TextField(label="Email", width=250,bgcolor="white")
    login_password = ft.TextField(label="Password", password=True, width=250,bgcolor="white")

    uploaded_image = ft.Image(width=200, height=200)
    tumor_detection_result = ft.Text("", size=18,weight="bold")

    # Define sections for registration, login, and profile
    register_section = ft.Column(visible=False)
    login_section = ft.Column(visible=False)
    profile_section = ft.Column(visible=False)

    # Function to clear all sections, ensuring they are hidden
    def clear_sections(e=None):
        register_section.visible = False
        login_section.visible = False
        profile_section.visible = False
        register_error_msg.value = ""
        login_error_msg.value = ""
        register_phone.value=""
        register_password.value=""
        register_username.value=""
        register_email.value=""
        register_dob_day.value=""
        register_dob_month.value=""
        register_dob_year.value=""
        login_email.value=""
        login_password.value=""

    # Function to show the register page
    def show_register(e=None):
        clear_sections()
        register_section.visible = True
        register_section.update()
        login_section.visible=False
        login_section.update()

    # Function to show the login page and hide all other sections
    def show_login(e=None):
        clear_sections()
        login_section.visible = True
        login_error_msg.value = ""  # Clear any previous login errors
        login_section.update()
        profile_section.visible = False
        profile_section.update()
        register_section.visible=False
        register_section.update()

    def clear_and_show_login(e=None):
        clear_image_and_result(e)
        show_login(e)


    # Function to show the profile page with image upload
    def show_profile(email):
        clear_sections()

        # FilePicker instance for image upload
        file_picker = ft.FilePicker(on_result=upload_image)
        file_picker.allowed_file_types = [".jpg", ".jpeg", ".png"]

        # Trigger button to open the FilePicker
        file_picker_button = ft.ElevatedButton(
            "Upload MRI Image",
            on_click=lambda e: file_picker.pick_files(),
            color="#CC313D",
            bgcolor="#F7C5CC"
        )

        # Define profile_section content as a Column with a card-like background
        profile_section.controls = [
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(f"Welcome, {email}", size=24, weight="bold"),
                            file_picker_button,
                            ft.Text("Tumor Detection Result:", size=18),
                            tumor_detection_result,
                            uploaded_image,
                            ft.ElevatedButton("Clear", on_click=clear_image_and_result, color="#CC313D", bgcolor="#F7C5CC"),
                            ft.ElevatedButton("Logout", on_click=clear_and_show_login, color="#CC313D", bgcolor="#F7C5CC"),
                            file_picker
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor="#FEE715",  # Background color for the container inside the card
                    padding=20,
                    border_radius=15,  # Optional: rounded corners
                ),
                elevation=5,  # Adds a shadow for a card-like effect
                width=400,  # Optional: set width
            )
        ]

        # Make profile_section visible and update it
        profile_section.visible = True
        profile_section.update()

    # Register user function
    from datetime import datetime

    def register_user(e):
        email = register_email.value
        username = register_username.value
        password = register_password.value
        phone = register_phone.value
        dob_day = register_dob_day.value
        dob_month = register_dob_month.value
        dob_year = register_dob_year.value

        # Make sure to convert day, month, and year from strings to integers
        try:
            dob_day = int(dob_day)
            dob_month = int(dob_month)
            dob_year = int(dob_year)

            # Create a datetime object for the Date of Birth
            dob = datetime(year=dob_year, month=dob_month, day=dob_day)

        except ValueError:
            register_error_msg.value = "Please enter a valid Date of Birth."
            register_section.update()
            return

        password_hash = hash_password(password)

        # Calculate age
        age = calculate_age(dob)  # Pass datetime object to calculate_age function

        if age < 18:
            register_error_msg.value = "You must be 18 or older to register."
            register_section.update()
            return

        try:
            # Connect to the database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if user already exists
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user:
                register_error_msg.value = "Email already registered."
            else:
                # Insert new user into the database
                cursor.execute(
                    "INSERT INTO users (email, username, password_hash, phone, dob) VALUES (%s, %s, %s, %s, %s)",
                    (email, username, password_hash, phone, dob))
                conn.commit()
                register_error_msg.value = "Registration successful!"
                show_login()

            cursor.close()
            conn.close()
        except Exception as error:
            register_error_msg.value = f"Error: {error}"

        register_section.update()

    # Login user function
    def login_user(e):
        email = login_email.value
        password = login_password.value
        password_hash = hash_password(password)

        try:
            # Connect to the database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Retrieve user and check password
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user and user[2] == password_hash:  # user[3] is the password_hash field
                show_profile(email)
            else:
                login_error_msg.value = "Invalid email or password."

            cursor.close()
            conn.close()
        except Exception as error:
            login_error_msg.value = f"Error: {error}"

        login_section.update()

    # Image upload handler
    import os

    def upload_image(file_picker_result):
        if file_picker_result.files:
            image_path = file_picker_result.files[0].path

            # Check if the path exists before proceeding
            if not os.path.exists(image_path):
                tumor_detection_result.value = "Error: File not found. Please try uploading again."
                profile_section.update()
                return

            uploaded_image.src = image_path if image_path else "D:/pythonProject/brain_tumor_pred/assets/upload.png" # Set the image source to the uploaded file path
            uploaded_image.update()

            try:
                # Send image to FastAPI endpoint
                with open(image_path, "rb") as image_file:
                    files = {"upload": image_file}
                    response = requests.post(FASTAPI_URL, files=files)

                if response.status_code == 200:
                    result = response.json().get("result")
                    confidence = response.json().get("confidence")
                    tumor_detection_result.value = f"Tumor Detection Result: {result} with {confidence}"
                else:
                    tumor_detection_result.value = f"Error: Unable to get a response, Status Code: {response.status_code}"
            except Exception as error:
                tumor_detection_result.value = f"Error: {error}"
            finally:
                profile_section.update()

    # Clear image and result function
    def clear_image_and_result(e):
        uploaded_image.src = ""  # Reset the image source
        tumor_detection_result.value = ""
        uploaded_image.update()  # Ensure the image is cleared
        profile_section.update()

    # Define sections with panels (using Card to create panels)
    register_section = ft.Card(
        content=ft.Container(
            content=ft.Column(
            [
                ft.Text("Register", size=24, weight="bold"),
                register_email,
                register_username,
                register_password,
                register_phone,
                ft.Text("Date of Birth", size=16, weight="bold"),
                register_dob_container,  # Display the Date of Birth fields
                ft.ElevatedButton("Register", color="#CC313D", bgcolor="#F7C5CC", on_click=register_user),
                register_error_msg,
                ft.TextButton("Already have an account? Login", on_click=show_login),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        bgcolor="#FEE715",
        padding=20,
        border_radius=15,
    ),
    elevation=5,
    width=350,
    visible=False
    )

    login_section = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Login", size=24, weight="bold"),
                    login_email,
                    login_password,
                    ft.ElevatedButton("Login", color="#CC313D", bgcolor="#F7C5CC", on_click=login_user),
                    login_error_msg,
                    ft.TextButton("Don't have an account? Register", on_click=show_register)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor="#FEE715",
            padding=20,
            border_radius=15,  # Optional: rounded corners
        ),
        elevation=5,
        width=350,
        visible=False
    )

    profile_section = ft.Column(visible=False)

    # Set up the page controls
    page.add(register_section, login_section, profile_section)

    # Show the login page initially
    show_login()

ft.app(target=main)
