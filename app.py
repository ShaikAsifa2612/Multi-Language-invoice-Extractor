# from dotenv import load_dotenv

# load_dotenv()  # take environment variables from .env.

# import streamlit as st
# import os
# import pathlib
# import textwrap
# from PIL import Image


# import google.generativeai as genai


# # os.getenv("GOOGLE_API_KEY") genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# genai.configure(api_key="AIzaSyAz8Xzs4GLkwHpxbXe3QbAK79t0gy-4V20")

# ## Function to load OpenAI model and get respones

# def get_gemini_response(input,image,prompt):
#     # model = genai.GenerativeModel('gemini-pro-vision')
#     model = genai.GenerativeModel('gemini-1.5-flash')  # Updated modelName to 'gemini-1.5-flash'

#     response = model.generate_content([input,image[0],prompt])
#     return response.text
    

# def input_image_setup(uploaded_file):
#     # Check if a file has been uploaded
#     if uploaded_file is not None:
#         # Read the file into bytes
#         bytes_data = uploaded_file.getvalue()

#         image_parts = [
#             {
#                 "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
#                 "data": bytes_data
#             }
#         ]
#         return image_parts
#     else:
#         raise FileNotFoundError("No file uploaded")


# ##initialize our streamlit app

# st.set_page_config(page_title="Gemini Image Demo")

# st.header("Gemini Application")
# input=st.text_input("Input Prompt: ",key="input")
# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
# image=""   
# if uploaded_file is not None:
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Uploaded Image.", use_column_width=True)


# submit=st.button("Tell me about the image")

# input_prompt = """
#                You are an expert in understanding invoices.
#                You will receive input images as invoices &
#                you will have to answer questions based on the input image
#                """

# ## If ask button is clicked

# if submit:
#     image_data = input_image_setup(uploaded_file)
#     response=get_gemini_response(input_prompt,image_data,input)
#     st.subheader("The Response is")
#     st.write(response)

# from dotenv import load_dotenv
# import streamlit as st
# import os
# from PIL import Image
# import pandas as pd
# import google.generativeai as genai

# # Load environment variables
# load_dotenv()

# # Configure GenAI with API Key
# genai.configure(api_key="AIzaSyAz8Xzs4GLkwHpxbXe3QbAK79t0gy-4V20")


# # Function to prepare input images
# def input_image_setup(uploaded_files):
#     image_parts = []
#     for uploaded_file in uploaded_files:
#         if uploaded_file is not None:
#             # Open the image using PIL
#             Image.open(uploaded_file)

#             # Convert the image into bytes
#             byte_data = uploaded_file.getvalue()

#             # Append the image data in the required format
#             image_parts.append({
#                 "mime_type": uploaded_file.type,  # e.g., 'image/png'
#                 "data": byte_data                # Byte data of the image
#             })
#     return image_parts


# # Function to get Gemini response for a specific question
# def get_gemini_response(input_text, image, prompt):
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     response = model.generate_content([input_text, image, prompt])
#     return response.text


# # Function to extract predefined key points from the invoice
# def extract_key_points(image, prompt):
#     key_points_prompt = """
#         You are an expert in understanding invoices.
#         Please extract the following key points from the invoice:
#         - Invoice Number
#         - Invoice Date
#         - Total Amount
#         - Billed To
#         - Due Date (if available)
#         Provide the information in a structured format.
#     """
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     response = model.generate_content([key_points_prompt, image, prompt])
#     return response.text


# # Streamlit app configuration
# st.set_page_config(page_title="Invoice Processing App")
# st.header("Invoice Processing App")

# # User input for task description
# input_prompt = st.text_area(
#     "Describe the task (e.g., 'Analyze invoices')",
#     value=(
#         "You are an expert in understanding invoices. "
#         "You will receive input images as invoices & you will have to extract relevant data based on the user's question."
#     ),
#     key="task_description",
# )

# # User input and file uploader
# input_text = st.text_input(
#     "Enter your question (e.g., 'What is the invoice date?' or 'Who is the invoice billed to?')",
#     key="input",
#     placeholder="e.g., Extract invoice date or billing name"
# )
# uploaded_files = st.file_uploader("Choose image(s)...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# # Submit button
# submit = st.button("Process Invoices")

# # Handle submission
# if submit:
#     if not uploaded_files:
#         st.error("Please upload at least one image.")
#     else:
#         # Display the uploaded images
#         st.subheader("Uploaded Invoices:")
#         for uploaded_file in uploaded_files:
#             image = Image.open(uploaded_file)
#             st.image(image, caption=f"File: {uploaded_file.name}", use_column_width=True)

#         # Prepare image data for Gemini API
#         image_data = input_image_setup(uploaded_files)

#         # Process each file and collect responses
#         extracted_data = []
#         for idx, image in enumerate(image_data):
#             try:
#                 # Extract predefined key points
#                 key_points_response = extract_key_points(image, input_prompt)
                
#                 # Extract response to user question
#                 question_response = get_gemini_response(input_text, image, input_prompt)

#                 # Append structured data
#                 extracted_data.append({
#                     "File Name": uploaded_files[idx].name,
#                     "Key Points": key_points_response.strip(),
#                     "Question": input_text,
#                     "Response": question_response.strip()
#                 })
#             except Exception as e:
#                 extracted_data.append({
#                     "File Name": uploaded_files[idx].name,
#                     "Key Points": "Error extracting key points",
#                     "Question": input_text,
#                     "Response": f"Error: {e}"
#                 })

#         # Convert extracted data to a DataFrame
#         df = pd.DataFrame(extracted_data)

#         # Display the extracted data in a table
#         st.subheader("Extracted Data:")
#         st.table(df)

#         # Provide a download button for the extracted data
#         st.download_button(
#             label="Download Extracted Data as CSV",
#             data=df.to_csv(index=False),
#             file_name="extracted_data.csv",
#             mime="text/csv"
#         )






# from dotenv import load_dotenv
# import streamlit as st
# import os
# from PIL import Image
# import pandas as pd
# import google.generativeai as genai

# # Load environment variables
# load_dotenv()

# # Configure GenAI with API Key
# genai.configure(api_key="AIzaSyAz8Xzs4GLkwHpxbXe3QbAK79t0gy-4V20")

# # Function to prepare input images
# def input_image_setup(uploaded_files):
#     image_parts = []
#     for uploaded_file in uploaded_files:
#         if uploaded_file is not None:
#             # Open the image using PIL
#             Image.open(uploaded_file)

#             # Convert the image into bytes
#             byte_data = uploaded_file.getvalue()

#             # Append the image data in the required format
#             image_parts.append({
#                 "mime_type": uploaded_file.type,  # e.g., 'image/png'
#                 "data": byte_data                # Byte data of the image
#             })
#     return image_parts

# # Function to get Gemini response for a specific question
# def get_gemini_response(input_text, image, prompt):
#     enhanced_prompt = f"""
#     Please answer the following question in clear and concise English:
#     Question: {input_text}
#     Ensure the response is detailed and accurate while remaining in English.
#     """
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     response = model.generate_content([enhanced_prompt, image, prompt])
#     return response.text

# # Function to extract predefined key points from the invoice
# def extract_key_points(image, prompt):
#     key_points_prompt = """
#     You are an expert in understanding invoices.
#     Please extract the following key points from the invoice:
#     - Invoice Number
#     - Invoice Date
#     - Total Amount
#     - Billed To
#     - Due Date (if available)
#     Provide the information in structured and proper English, in the following format:
#     Invoice Number: [value]
#     Invoice Date: [value]
#     Total Amount: [value]
#     Billed To: [value]
#     Due Date: [value]
#     """
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     response = model.generate_content([key_points_prompt, image, prompt])
#     return response.text

# # Streamlit app configuration
# st.set_page_config(page_title="Invoice Processing App")
# st.header("Invoice Processing App")

# # User input for task description
# input_prompt = st.text_area(
#     "Describe the task (e.g., 'Analyze invoices')",
#     value=(
#         "You are an expert in understanding invoices. "
#         "You will receive input images as invoices & you will have to extract relevant data based on the user's question."
#     ),
#     key="task_description",
# )

# # User input and file uploader
# input_text = st.text_input(
#     "Enter your question (e.g., 'What is the invoice date?' or 'Who is the invoice billed to?')",
#     key="input",
#     placeholder="e.g., Extract invoice date or billing name"
# )
# uploaded_files = st.file_uploader("Choose image(s)...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# # Submit button
# submit = st.button("Process Invoices")

# # Handle submission
# if submit:
#     if not uploaded_files:
#         st.error("Please upload at least one image.")
#     else:
#         # Display the uploaded images
#         st.subheader("Uploaded Invoices:")
#         for uploaded_file in uploaded_files:
#             image = Image.open(uploaded_file)
#             st.image(image, caption=f"File: {uploaded_file.name}", use_column_width=True)

#         # Prepare image data for Gemini API
#         image_data = input_image_setup(uploaded_files)

#         # Process each file and collect responses
#         extracted_data = []
#         for idx, image in enumerate(image_data):
#             try:
#                 # Extract predefined key points
#                 key_points_response = extract_key_points(image, input_prompt)
                
#                 # Extract response to user question
#                 question_response = get_gemini_response(input_text, image, input_prompt)

#                 # Append structured data
#                 extracted_data.append({
#                     "File Name": uploaded_files[idx].name,
#                     "Key Points": key_points_response.strip(),
#                     "Question": input_text,
#                     "Response": question_response.strip()
#                 })
#             except Exception as e:
#                 extracted_data.append({
#                     "File Name": uploaded_files[idx].name,
#                     "Key Points": "Error extracting key points",
#                     "Question": input_text,
#                     "Response": f"Error: {e}"
#                 })

#         # Convert extracted data to a DataFrame
#         df = pd.DataFrame(extracted_data)

#         # Display the extracted data in a table
#         st.subheader("Extracted Data:")
#         st.table(df)

#         # Provide a download button for the extracted data
#         st.download_button(
#             label="Download Extracted Data as CSV",
#             data=df.to_csv(index=False),
#             file_name="extracted_data.csv",
#             mime="text/csv"
#         )





# from dotenv import load_dotenv
# import streamlit as st
# import os
# from PIL import Image
# import pandas as pd
# import google.generativeai as genai
# from googletrans import Translator
# from fpdf import FPDF
# import pytesseract

# # Load environment variables
# load_dotenv()

# # Configure GenAI with API Key
# # genai.configure(api_key="AIzaSyAz8Xzs4GLkwHpxbXe3QbAK79t0gy-4V20")

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# # Function to prepare input images
# # Function to prepare input images
# def input_image_setup(uploaded_files):
#     image_parts = []
#     for uploaded_file in uploaded_files:
#         if uploaded_file is not None:
#             # Open the image using PIL
#             Image.open(uploaded_file)

#             # Convert the image into bytes
#             byte_data = uploaded_file.getvalue()

#             # Append the image data in the required format
#             image_parts.append({
#                 "mime_type": uploaded_file.type,  # e.g., 'image/png'
#                 "data": byte_data                # Byte data of the image
#             })
#     return image_parts

# # Function to get Gemini response for a specific question
# def get_gemini_response(input_text, image, prompt):
#     enhanced_prompt = f"""
#     Please answer the following question in clear and concise English:
#     Question: {input_text}
#     Ensure the response is detailed and accurate while remaining in English.
#     """
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     response = model.generate_content([enhanced_prompt, image, prompt])
#     return response.text

# # Function to extract predefined key points from the invoice
# def extract_key_points(image, prompt):
#     key_points_prompt = """
#     You are an expert in understanding invoices.
#     Please extract the following key points from the invoice:
#     - Invoice Number
#     - Invoice Date
#     - Total Amount
#     - Billed To
#     - Due Date (if available)
#     Provide the information in structured and proper English, in the following format:
#     Invoice Number: [value]
#     Invoice Date: [value]
#     Total Amount: [value]
#     Billed To: [value]
#     Due Date: [value]
#     """
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     response = model.generate_content([key_points_prompt, image, prompt])
#     return response.text

# # Function to translate extracted text into English
# def translate_text(extracted_text):
#     translator = Translator()
#     translated_text = translator.translate(extracted_text, src="auto", dest="en").text
#     return translated_text

# # Function to generate PDF from translated text
# def generate_invoice_pdf_from_translated_text(translated_text, filename="translated_invoice.pdf"):
#     pdf = FPDF()
#     pdf.add_page()

#     # Use a custom font (Arial or any Unicode-compatible font)
#     pdf.set_font("Arial", size=12)

#     # Add invoice header
#     pdf.cell(200, 10, txt="Translated Invoice", ln=True, align="C")
#     pdf.ln(10)

#     # Add translated text
#     pdf.set_font("Arial", size=10)
#     pdf.multi_cell(0, 10, txt=translated_text)
    
#     # Output the PDF
#     pdf.output(filename)

# # Streamlit app configuration
# st.set_page_config(page_title="Invoice Processing App")
# st.header("Invoice Processing App")

# # User input for task description
# input_prompt = st.text_area(
#     "Describe the task (e.g., 'Analyze invoices')",
#     value=(
#         "You are an expert in understanding invoices. "
#         "You will receive input images as invoices & you will have to extract relevant data based on the user's question."
#     ),
#     key="task_description",
# )

# # User input and file uploader
# input_text = st.text_input(
#     "Enter your question (e.g., 'What is the invoice date?' or 'Who is the invoice billed to?')",
#     key="input",
#     placeholder="e.g., Extract invoice date or billing name"
# )
# uploaded_files = st.file_uploader("Choose image(s)...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# # Submit button
# submit = st.button("Process Invoices")

# # Handle submission
# if submit:
#     if not uploaded_files:
#         st.error("Please upload at least one image.")
#     else:
#         # Display the uploaded images
#         st.subheader("Uploaded Invoices:")
#         for uploaded_file in uploaded_files:
#             image = Image.open(uploaded_file)
#             st.image(image, caption=f"File: {uploaded_file.name}", use_column_width=True)

#         # Prepare image data for Gemini API
#         image_data = input_image_setup(uploaded_files)

#         # Process each file and collect responses
#         extracted_data = []
#         translated_text = ""
#         for idx, image in enumerate(image_data):
#             try:
#                 # Extract predefined key points
#                 key_points_response = extract_key_points(image, input_prompt)
                
#                 # Extract response to user question
#                 question_response = get_gemini_response(input_text, image, input_prompt)

#                 # Extract text from invoice using OCR
#                 image_pil = Image.open(uploaded_files[idx])
#                 extracted_text = pytesseract.image_to_string(image_pil)

#                 # Translate extracted text to English
#                 translated_text = translate_text(extracted_text)

#                 # Append structured data
#                 extracted_data.append({
#                     "File Name": uploaded_files[idx].name,
#                     "Key Points": key_points_response.strip(),
#                     "Question": input_text,
#                     "Response": question_response.strip()
#                 })
#             except Exception as e:
#                 extracted_data.append({
#                     "File Name": uploaded_files[idx].name,
#                     "Key Points": "Error extracting key points",
#                     "Question": input_text,
#                     "Response": f"Error: {e}"
#                 })

#         # Convert extracted data to a DataFrame
#         df = pd.DataFrame(extracted_data)

#         # Display the extracted data in a table
#         st.subheader("Extracted Data:")
#         st.table(df)

#         # Provide a download button for the extracted data
#         st.download_button(
#             label="Download Extracted Data as CSV",
#             data=df.to_csv(index=False),
#             file_name="extracted_data.csv",
#             mime="text/csv"
#         )

#         # Show translated text in a structured format within a text area
#         if st.button("Show Full Translated Text"):
#             st.subheader("Full Translated Text:")
#             st.text_area("Translated Invoice Text", translated_text, height=300)

#         # Button to generate and download PDF from translated text
#         if st.button("Download Translated Invoice as PDF"):
#             if translated_text:
#                 generate_invoice_pdf_from_translated_text(translated_text)
#                 st.success("PDF Generated!")
#             else:
#                 st.error("No translated text available.")



# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import google.generativeai as genai
# from fpdf import FPDF
# from PIL import Image
# from googletrans import Translator
# import pytesseract
# import matplotlib

# # Load environment variables
# # If you have an .env file, you can load it here using load_dotenv()
# # from dotenv import load_dotenv
# # load_dotenv()

# # Configure GenAI with API Key
# genai.configure(api_key="AIzaSyAz8Xzs4GLkwHpxbXe3QbAK79t0gy-4V20")

# # Initialize the Google Translate API
# translator = Translator()
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# # Function to prepare input images
# def input_image_setup(uploaded_files):
#     image_parts = []
#     for uploaded_file in uploaded_files:
#         if uploaded_file is not None:
#             # Open the image using PIL
#             Image.open(uploaded_file)

#             # Convert the image into bytes
#             byte_data = uploaded_file.getvalue()

#             # Append the image data in the required format
#             image_parts.append({
#                 "mime_type": uploaded_file.type,  # e.g., 'image/png'
#                 "data": byte_data                # Byte data of the image
#             })
#     return image_parts

# # Function to extract predefined key points from the invoice
# def extract_key_points(image, prompt):
#     key_points_prompt = """
#     You are an expert in understanding invoices.
#     Please extract the following key points from the invoice:
#     - Invoice Number
#     - Invoice Date
#     - Total Amount
#     - Billed To
#     - Due Date (if available)
#     """
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     response = model.generate_content([key_points_prompt, image, prompt])
#     return response.text

# # Function to extract product details and quantities from the invoice
# def extract_product_details(image, prompt):
#     product_details_prompt = """
#     Extract the following details about the products in the invoice:
#     - Product Name
#     - Quantity
#     Provide the information in structured English, in the following format:
#     Product Name: [Product Name], Quantity: [Quantity]
#     """
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     response = model.generate_content([product_details_prompt, image, prompt])
#     return response.text

# # Function to translate text to English if it's not already
# def translate_to_english(text):
#     # Detect the language
#     detected_language = translator.detect(text).lang

#     if detected_language != 'en':
#         # Translate to English if the language is not English
#         translated_text = translator.translate(text, src=detected_language, dest='en').text
#         return translated_text
#     else:
#         return text  # If it's already in English, return the original text

# # Function to generate the product-quantity pie chart with better aesthetics
# def generate_product_quantity_pie_chart(products, quantities):
#     fig, ax = plt.subplots(figsize=(8, 8))  # Adjust the size of the pie chart
#     ax.pie(quantities, labels=products, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)  # Elegant colors and percentage labels
    
#     ax.set_title('Products and Their Quantities', fontsize=16)  # Set title with larger font
    
#     # Display the pie chart
#     st.pyplot(fig)

# # Function to generate the product-quantity bar chart
# def generate_product_quantity_bar_chart(products, quantities):
#     fig, ax = plt.subplots(figsize=(10, 6))  # Set the size of the plot
#     ax.bar(products, quantities, color='skyblue')  # Bar chart color
#     ax.set_xlabel('Product Name')
#     ax.set_ylabel('Quantity')
#     ax.set_title('Product Quantities')
#     plt.xticks(rotation=45, ha='right')  # Rotate x labels to avoid overlap
#     st.pyplot(fig)

# # Streamlit app configuration
# st.set_page_config(page_title="Invoice Processing App")
# st.header("Invoice Processing App")

# # User input for task description
# input_prompt = st.text_area(
#     "Describe the task (e.g., 'Analyze invoices')",
#     value=( 
#         "You are an expert in understanding invoices. "
#         "You will receive input images as invoices & you will have to extract relevant data based on the user's question."
#     ),
#     key="task_description",
# )

# # User input and file uploader
# input_text = st.text_input(
#     "Enter your question (e.g., 'What is the invoice date?' or 'Who is the invoice billed to?')",
#     key="input",
#     placeholder="e.g., Extract invoice date or billing name"
# )
# uploaded_files = st.file_uploader("Choose image(s)...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# # Visualization choice options
# visualization_option = st.selectbox(
#     "Choose a visualization type",
#     ("Pie Chart", "Bar Chart")
# )

# # Submit button
# submit = st.button("Process Invoices")

# # Handle submission
# if submit:
#     if not uploaded_files:
#         st.error("Please upload at least one image.")
#     else:
#         # Display the uploaded images
#         st.subheader("Uploaded Invoices:")
#         for uploaded_file in uploaded_files:
#             image = Image.open(uploaded_file)
#             st.image(image, caption=f"File: {uploaded_file.name}", use_column_width=True)

#         # Prepare image data for Gemini API
#         image_data = input_image_setup(uploaded_files)

#         # Process each file and collect responses
#         extracted_data = []
#         for idx, image in enumerate(image_data):
#             try:
#                 # Extract key points (essential information) from the invoice
#                 key_points_response = extract_key_points(image, input_prompt)
#                 key_points_response = translate_to_english(key_points_response)  # Translate if needed

#                 # Extract product details and quantities
#                 product_details_response = extract_product_details(image, input_prompt)
#                 product_details_response = translate_to_english(product_details_response)  # Translate if needed
                
#                 # Process the product details to create a structured list of products and quantities
#                 products = []
#                 quantities = []
                
#                 # Here, you can parse the product details response and fill the lists accordingly
#                 # Let's assume the response is in a format like:
#                 # Product Name: Apple, Quantity: 10
#                 # Product Name: Banana, Quantity: 20
#                 for line in product_details_response.splitlines():
#                     if "Product Name:" in line and "Quantity:" in line:
#                         parts = line.split(",")
#                         product = parts[0].split(":")[1].strip()
#                         quantity = int(parts[1].split(":")[1].strip())
#                         products.append(product)
#                         quantities.append(quantity)

#                 # Display the key points extracted from the invoice
#                 st.subheader("Essential Information from Invoice:")
#                 st.write(key_points_response)

#                 # Generate and display the selected visualization
#                 if products and quantities:
#                     if visualization_option == "Pie Chart":
#                         generate_product_quantity_pie_chart(products, quantities)
#                     elif visualization_option == "Bar Chart":
#                         generate_product_quantity_bar_chart(products, quantities)

#                 # Append extracted data
#                 extracted_data.append({
#                     "File Name": uploaded_files[idx].name,
#                     "Key Points": key_points_response.strip(),
#                     "Product Details": product_details_response.strip()
#                 })
#             except Exception as e:
#                 extracted_data.append({
#                     "File Name": uploaded_files[idx].name,
#                     "Key Points": f"Error: {e}",
#                     "Product Details": f"Error: {e}"
#                 })

#         # Convert extracted data to a DataFrame
#         df = pd.DataFrame(extracted_data)

#         # Display the extracted data in a table
#         st.subheader("Extracted Data:")
#         st.table(df)

#         # Provide a download button for the extracted data
#         st.download_button(
#             label="Download Extracted Data as CSV",
#             data=df.to_csv(index=False),
#             file_name="extracted_data.csv",
#             mime="text/csv"
#         )








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
