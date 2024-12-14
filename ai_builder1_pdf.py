import streamlit as st
import os
from io import BytesIO
from fpdf import FPDF
from PIL import Image

def generate_resume(data, image_path=None):
    """Generate a PDF resume based on collected data."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    if image_path:
        pdf.image(image_path, x=10, y=8, w=25, h=25)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=data['name'], ln=True, align='C')
    pdf.cell(200, 10, txt=f"{data['address']} | {data['contact']} | {data['email']}", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, txt="Objective", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=data['objective'])
    pdf.ln(5)

    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, txt="Education", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=data['education'])
    pdf.ln(5)

    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, txt="Work Experience", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=data['work_experience'])
    pdf.ln(5)

    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, txt="Skills", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=data['skills'])
    pdf.ln(5)

    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, txt="References", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=data['references'])

    return pdf

# Streamlit App
st.title("AI Resume Builder")
st.write("Answer the questions below to build your resume step by step.")

# Personal Information
st.header("Personal Information")
name = st.text_input("Full Name")
address = st.text_input("Address")
contact = st.text_input("Contact Number")
email = st.text_input("Email Address")

# Upload Picture
st.header("Upload Picture (1\" x 1\")")
image_file = st.file_uploader("Upload your picture in JPG or PNG format", type=["jpg", "png"])
image_path = None
if image_file:
    img = Image.open(image_file)
    img = img.resize((300, 300))  # Resize to 1"x1" approximately for PDF
    image_path = "temp_image.jpg"
    img.save(image_path)

# Career Objective
st.header("Career Objective")
objective = st.text_area("Briefly describe your career objective (Optional)", "")

# Education
st.header("Educational Background")
education_entries = []
number_of_education = st.number_input("Number of educational qualifications:", min_value=1, step=1)
for i in range(number_of_education):
    st.subheader(f"Education {i+1}")
    degree = st.text_input(f"Degree for Education {i+1}")
    school = st.text_input(f"School/University for Education {i+1}")
    year = st.text_input(f"Graduation Year for Education {i+1}")
    education_entries.append(f"{degree}, {school} - {year}")
education = "\n".join(education_entries)

# Work Experience
st.header("Work Experience")
work_entries = []
number_of_jobs = st.number_input("Number of previous jobs:", min_value=1, step=1)
for i in range(number_of_jobs):
    st.subheader(f"Job {i+1}")
    job_title = st.text_input(f"Job Title for Job {i+1}")
    company = st.text_input(f"Company Name for Job {i+1}")
    dates = st.text_input(f"Dates of Employment for Job {i+1}")
    responsibilities = st.text_area(f"Key Responsibilities for Job {i+1}")
    work_entries.append(f"{job_title} at {company} ({dates})\n- {responsibilities}")
work_experience = "\n".join(work_entries)

# Skills
st.header("Skills")
skills = st.text_area("List your skills (comma-separated)", "")

# References
st.header("References")
reference_entries = []
number_of_references = st.number_input("Number of references:", min_value=1, step=1)
for i in range(number_of_references):
    st.subheader(f"Reference {i+1}")
    ref_name = st.text_input(f"Name of Reference {i+1}")
    ref_contact = st.text_input(f"Contact Number of Reference {i+1}")
    ref_email = st.text_input(f"Email of Reference {i+1}")
    reference_entries.append(f"{ref_name}, {ref_contact}, {ref_email}")
references = "\n".join(reference_entries)

# Generate Resume
if st.button("Generate Resume"):
    user_data = {
        "name": name,
        "address": address,
        "contact": contact,
        "email": email,
        "objective": objective,
        "education": education,
        "work_experience": work_experience,
        "skills": skills,
        "references": references
    }

    pdf = generate_resume(user_data, image_path)
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    st.header("Your Resume")
    st.download_button(
        label="Download Resume as PDF",
        data=pdf_buffer,
        file_name="resume.pdf",
        mime="application/pdf"
    )

    # Cleanup temporary image file
    if image_path and os.path.exists(image_path):
        os.remove(image_path)
