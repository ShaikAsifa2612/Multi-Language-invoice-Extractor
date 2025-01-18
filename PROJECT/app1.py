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
            image = Image.open(uploaded_file)
            byte_data = uploaded_file.getvalue()
            image_parts.append({
                "mime_type": uploaded_file.type,
                "data": byte_data,
                "image": image
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

# Function to answer user queries based on the invoice image content
def answer_user_question_directly(image, user_prompt):
    try:
        dynamic_answer_prompt = f"""
        Here is an invoice. Provide a response to the user's query based on this image content:
        User Query: {user_prompt}
        """
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([dynamic_answer_prompt, image])
        return response.text.strip()
    except Exception as e:
        return f"Error while answering the question: {str(e)}"

# Function to translate text to the target language
def translate_text(text, target_language):
    language_code = language_mapping.get(target_language, "en")
    detected_language = translator.detect(text).lang
    if detected_language != language_code:
        translated_text = translator.translate(text, src=detected_language, dest=language_code).text
        return translated_text
    else:
        return text

# Categorize invoice based on extracted product/service data and due date
def categorize_invoice(translated_product_details, translated_key_points):
    # Keywords for identifying products or services
    product_keywords = ["product", "item", "goods", "sale"]
    service_keywords = ["service", "consulting", "subscription", "maintenance"]

    # Check if the product details contain any keywords related to products or services
    for product in translated_product_details.lower().split("\n"):
        if any(keyword in product for keyword in product_keywords):
            return "Product Invoice"
        elif any(keyword in product for keyword in service_keywords):
            return "Service Invoice"

    # Improved Due Date and Paid Status Detection
    # Look for terms that indicate due date or payment status
    due_date_keywords = ["due date", "payment due", "outstanding", "due"]
    payment_keywords = ["not available on the invoice" ,"paid", "payment completed", "settled", "finalized", "payment received"]

    # Check for specific phrases indicating no due date is mentioned
    no_due_date_phrases = [
        "not available on the invoice",
        "not mentioned",
        "no explicit due date mentioned"
    ]
    
    If any of the phrases indicating "no due date" is found, consider the invoice as paid
    if any(phrase.lower() in translated_key_points.lower() for phrase in no_due_date_phrases):
        return "Paid"

    # Check if any of the due date or payment-related terms are found in translated key points
    is_due_date_found = any(keyword in translated_key_points.lower() for keyword in due_date_keywords)
    is_paid_found = any(keyword in translated_key_points.lower() for keyword in payment_keywords)

    # If payment-related terms are found, classify as "Paid"
    if is_paid_found:
        return "Paid"
    
    # If no due date or payment term is found, classify as "Paid" (default behavior)
    if not is_due_date_found:
        return "Paid"
    
    # If due date or outstanding terms are found, classify as "Unpaid"
    return "Unpaid"
    


# Function to generate the product-quantity pie chart
def generate_product_quantity_pie_chart(products, quantities):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(quantities, labels=products, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    ax.set_title('Products and Their Quantities', fontsize=16)
    st.pyplot(fig)

# Function to generate the product-quantity bar chart
def generate_product_quantity_bar_chart(products, quantities):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(products, quantities, color='skyblue')
    ax.set_xlabel('Product Name')
    ax.set_ylabel('Quantity')
    ax.set_title('Product Quantities')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

# Function to create a highlighted box for answers
def highlight_box(content, color="lightblue"):
    st.markdown(
        f"""
        <div style="
            background-color: {color};
            border-radius: 5px;
            padding: 10px;
            margin: 10px 0;
            font-size: 16px;
            font-weight: bold;
            color: black;
        ">
            {content}
        </div>
        """,
        unsafe_allow_html=True
    )

# Streamlit app configuration
st.set_page_config(page_title="Invoice Processing App")
st.header("Invoice Processing App")

# User input for task description
# input_prompt = st.text_area(
#     "Describe the task (e.g., 'Analyze invoices')",
#     value=("You are an expert in understanding invoices. "
#            "You will receive input images as invoices & you will have to extract relevant data based on the user's question."),
#     key="task_description",
# )

# User input and file uploader
input_text = st.text_input(
    "Enter your question (e.g., 'What is the invoice date?' or 'Who is the invoice billed to?')",
    key="input",
    placeholder="e.g., Extract invoice date or billing name"
)
menu = st.sidebar.radio("Navigate to", ["Home"])
if menu == "Home":
    # User inputs
    input_prompt = st.text_area(
        "Describe the task",
        value="You are an expert in understanding invoices. Extract data from invoices based on user questions.",
        key="task_description"
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
        st.subheader("Uploaded Invoices:")
        image_data = input_image_setup(uploaded_files)
        
        extracted_data = []
        products = []
        quantities = []
        for idx, image in enumerate(image_data):
            try:
                st.image(image["image"], caption=f"File: {uploaded_files[idx].name}", use_column_width=True)

                # Extract key points and product details
                key_points_response = extract_key_points(image["image"], input_prompt)
                translated_key_points = translate_text(key_points_response, target_language)

                product_details_response = extract_product_details(image["image"], input_prompt)
                translated_product_details = translate_text(product_details_response, target_language)

                user_answer = answer_user_question_directly(image["image"], input_text)

                st.subheader("Key Points (Translated):")
                st.write(translated_key_points)

                st.subheader("Product Details (Translated):")
                st.write(translated_product_details)

                st.subheader(f"Answer to Your Question: {input_text}")
                highlight_box(user_answer, color="lightyellow")

                # Categorize the invoice
                category = categorize_invoice(translated_product_details, translated_key_points)
                status = "Paid" if "paid" in translated_key_points.lower() else "Unpaid"

                st.subheader("Invoice Summary")
                highlight_box(f"Category: {category}")
                highlight_box(f"Status: {status}", color="lightgreen" if status == "Paid" else "lightcoral")

                # Append the extracted data
                extracted_data.append({
                    "File Name": uploaded_files[idx].name,
                    "Key Points": translated_key_points.strip(),
                    "Product Details": translated_product_details.strip(),
                    "Category": category,
                    "Status": status
                })

                # Extract product names and quantities
                product_details_lines = translated_product_details.split("\n")
                products = []
                quantities = []

                for detail in product_details_lines:
                    if "Product Name" in detail and "Quantity" in detail:
                        try:
                            product_name = detail.split(",")[0].split(":")[1].strip()
                            quantity_str = detail.split(",")[1].split(":")[1].strip()

                            # Check if the quantity is a valid number (int or float)
                            if quantity_str.isdigit():
                                quantity = int(quantity_str)  # Convert to integer if valid
                            else:
                                quantity = 0  # Set quantity to 0 if it's not a valid number

                            products.append(product_name)
                            quantities.append(quantity)

                        except Exception as e:
                            st.warning(f"Error processing line '{detail}': {e}")

                # Visualization for product quantities
                if products and quantities:
                    st.subheader("Product Quantities Visualization:")
                    if visualization_option == "Pie Chart":
                        generate_product_quantity_pie_chart(products, quantities)
                    elif visualization_option == "Bar Chart":
                        generate_product_quantity_bar_chart(products, quantities)

            except Exception as e:
                extracted_data.append({
                    "File Name": uploaded_files[idx].name,
                    "Key Points": f"Error: {e}",
                    "Product Details": f"Error: {e}",
                    "Category": f"Error: {e}",
                    "Status": "Error"
                })

        # Convert extracted data to a DataFrame
        df = pd.DataFrame(extracted_data)

        st.subheader("Extracted Data:")
        st.table(df)

        st.download_button(
            label="Download Extracted Data as CSV",
            data=df.to_csv(index=False),
            file_name="extracted_data.csv",
            mime="text/csv"
        )
