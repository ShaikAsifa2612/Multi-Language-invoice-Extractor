from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb
import subprocess
import os

app = Flask(__name__)

# Database Configuration
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'Team7JNTU4Year'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'trail6'  # Database name

mysql = MySQL(app)
app.secret_key = 'your_secret_key'  # For flashing messages

@app.route('/')
def index():
    print("Index route accessed")
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    print("Register route accessed")
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
        mysql.connection.commit()
        flash("Registration successful!", "success")
    except MySQLdb.MySQLError as e:
        print(f"Error: {e}")
        mysql.connection.rollback()
        flash("Registration failed, please try again.", "error")
    finally:
        cursor.close()
    
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    print("Login route accessed")
    username_email = request.form['username-email']
    password = request.form['password']
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE (username = %s OR email = %s) AND password = %s', (username_email, username_email, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        print("Login Successful")
        flash("Login successful!", "success")
        return redirect(url_for('success'))  # Redirect to success page after login
    else:
        flash("Invalid credentials, please try again.", "error")
        return redirect(url_for('index'))  # Redirect back to index with an error message

@app.route('/success')



def success():
   
    os.environ["BROWSER"] = "none"
    # Directly execute the Streamlit app
    try:
        subprocess.run(["streamlit", "run", "app1.py"], check=True)
    except subprocess.CalledProcessError as e:
        # Handle any error if the Streamlit app fails to execute
        print(f"Error occurred while running Streamlit app: {e}")



#def success():
 #
 #   return "<h1 style='color:red;'>Welcome, you have logged in successfully!</h1>"

if __name__ == '__main__':
    app.run(debug=True, port=5001)


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai
from fpdf import FPDF
from PIL import Image
from googletrans import Translator
import pytesseract

# Configure GenAI with API Key
genai.configure(api_key="AIzaSyAz8Xzs4GLkwHpxbXe3QbAK79t0gy-4V20")

# Initialize the Google Translate API
translator = Translator()
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Map language names to language codes
language_mapping = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Hindi": "hi",
    "Chinese": "zh-cn",
    "Telugu": "te"
}

# Function to prepare input images
def input_image_setup(uploaded_files):
    image_parts = []
    for uploaded_file in uploaded_files:
        if uploaded_file is not None:
            # Open the image using PIL
            Image.open(uploaded_file)

            # Convert the image into bytes
            byte_data = uploaded_file.getvalue()

            # Append the image data in the required format
            image_parts.append({
                "mime_type": uploaded_file.type,  # e.g., 'image/png'
                "data": byte_data                # Byte data of the image
            })
    return image_parts

# Function to extract predefined key points from the invoice
def extract_key_points(image, prompt):
    key_points_prompt = """
    You are an expert in understanding invoices.
    Please extract the following key points from the invoice:
    - Invoice Number
    - Invoice Date
    - Total Amount
    - Billed To
    - Due Date (if available)
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([key_points_prompt, image, prompt])
    return response.text

# Function to extract product details and quantities from the invoice
def extract_product_details(image, prompt):
    product_details_prompt = """
    Extract the following details about the products in the invoice:
    - Product Name
    - Quantity
    Provide the information in structured English, in the following format:
    Product Name: [Product Name], Quantity: [Quantity]
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([product_details_prompt, image, prompt])
    return response.text

# Function to translate text to the target language
def translate_text(text, target_language):
    # Get the language code
    language_code = language_mapping.get(target_language, "en")

    # Detect the original language
    detected_language = translator.detect(text).lang

    # Translate only if the detected language is different from the target language
    if detected_language != language_code:
        translated_text = translator.translate(text, src=detected_language, dest=language_code).text
        return translated_text
    else:
        return text  # Return the original text if it's already in the target language

# Function to generate the product-quantity pie chart with better aesthetics
def generate_product_quantity_pie_chart(products, quantities):
    fig, ax = plt.subplots(figsize=(8, 8))  # Adjust the size of the pie chart
    ax.pie(quantities, labels=products, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)  # Elegant colors
    ax.set_title('Products and Their Quantities', fontsize=16)  # Set title with larger font
    st.pyplot(fig)  # Display the plot

# Function to generate the product-quantity bar chart
def generate_product_quantity_bar_chart(products, quantities):
    fig, ax = plt.subplots(figsize=(10, 6))  # Set the size of the plot
    ax.bar(products, quantities, color='skyblue')  # Bar chart color
    ax.set_xlabel('Product Name')
    ax.set_ylabel('Quantity')
    ax.set_title('Product Quantities')
    plt.xticks(rotation=45, ha='right')  # Rotate x labels to avoid overlap
    st.pyplot(fig)  # Display the plot

# Streamlit app configuration
st.set_page_config(page_title="Invoice Processing App")
st.header("Invoice Processing App")

# User input for task description
input_prompt = st.text_area(
    "Describe the task (e.g., 'Analyze invoices')",
    value=(
        "You are an expert in understanding invoices. "
        "You will receive input images as invoices & you will have to extract relevant data based on the user's question."
    ),
    key="task_description",
)

# User input and file uploader
input_text = st.text_input(
    "Enter your question (e.g., 'What is the invoice date?' or 'Who is the invoice billed to?')",
    key="input",
    placeholder="e.g., Extract invoice date or billing name"
)
uploaded_files = st.file_uploader("Choose image(s)...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Language selection for translation
target_language = st.selectbox(
    "Select the language to translate the invoice text for extraction:",
    options=list(language_mapping.keys()),
    index=0
)

# Visualization choice options
visualization_option = st.selectbox(
    "Choose a visualization type",
    ("Pie Chart", "Bar Chart")
)

# Submit button
submit = st.button("Process Invoices")

# Handle submission
if submit:
    if not uploaded_files:
        st.error("Please upload at least one image.")
    else:
        # Display the uploaded images
        st.subheader("Uploaded Invoices:")
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            st.image(image, caption=f"File: {uploaded_file.name}",use_container_width=True)

        # Prepare image data for Gemini API
        image_data = input_image_setup(uploaded_files)

        # Process each file and collect responses
        extracted_data = []
        for idx, image in enumerate(image_data):
            try:
                # Extract key points (essential information) from the invoice
                key_points_response = extract_key_points(image, input_prompt)
                
                # Translate key points to the target language
                key_points_response = translate_text(key_points_response, target_language)

                # Extract product details and quantities
                product_details_response = extract_product_details(image, input_prompt)
                
                # Translate product details to the target language
                product_details_response = translate_text(product_details_response, target_language)

                # Process the product details to create a structured list of products and quantities
                products = []
                quantities = []

                for line in product_details_response.splitlines():
                    if "Product Name:" in line and "Quantity:" in line:
                        parts = line.split(",")
                        product = parts[0].split(":")[1].strip()
                        quantity = int(parts[1].split(":")[1].strip())
                        products.append(product)
                        quantities.append(quantity)

                # Display the translated key points
                st.subheader("Essential Information from Invoice (Translated):")
                st.write(key_points_response)

                # Generate and display the selected visualization
                if products and quantities:
                    if visualization_option == "Pie Chart":
                        generate_product_quantity_pie_chart(products, quantities)
                    elif visualization_option == "Bar Chart":
                        generate_product_quantity_bar_chart(products, quantities)

                # Append extracted data
                extracted_data.append({
                    "File Name": uploaded_files[idx].name,
                    "Key Points": key_points_response.strip(),
                    "Product Details": product_details_response.strip()
                })
            except Exception as e:
                extracted_data.append({
                    "File Name": uploaded_files[idx].name,
                    "Key Points": f"Error: {e}",
                    "Product Details": f"Error: {e}"
                })

        # Convert extracted data to a DataFrame
        df = pd.DataFrame(extracted_data)

        # Display the extracted data in a table
        st.subheader("Extracted Data:")
        st.table(df)

        # Provide a download button for the extracted data
        st.download_button(
            label="Download Extracted Data as CSV",
            data=df.to_csv(index=False),
            file_name="extracted_data.csv",
            mime="text/csv"
        )

