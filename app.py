# import necessary libraries
from flask import Flask, render_template, request, send_from_directory, send_file
import spacy
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import csv
import os

app = Flask(__name__)

# Load spaCy NER model
nlp = spacy.load("en_core_web_sm")

# Initialize results variable
results = []

# Extract text from PDFs
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

# Extract entities using spaCy NER
def extract_entities(text):
    emails = re.findall(r'\S+@\S+', text)
    names = re.findall(r'^([A-Z][a-z]+)\s+([A-Z][a-z]+)', text)
    if names:
        names = [" ".join(names[0])]
    return emails, names

@app.route('/', methods=['GET', 'POST'])
def about():
    results = []
    # Check if the request method is POST (indicating form submission)
    if request.method == 'POST':
        
        # Retrieve the job description and list of uploaded resume files from the submitted form
        job_description = request.form['job_description']
        resume_files = request.files.getlist('resume_files')

        # Create a directory for uploads if it doesn't exist
        if not os.path.exists("uploads"):
            os.makedirs("uploads")

        # Process uploaded resumes
        processed_resumes = []
        for resume_file in resume_files:
            # Save the uploaded file
            resume_path = os.path.join("uploads", resume_file.filename)
            resume_file.save(resume_path)

            # Process the saved file
            resume_text = extract_text_from_pdf(resume_path)
            emails, names = extract_entities(resume_text)
            processed_resumes.append((names, emails, resume_text))

        # TF-IDF vectorizer
        tfidf_vectorizer = TfidfVectorizer()
        job_desc_vector = tfidf_vectorizer.fit_transform([job_description])

        # Rank resumes based on similarity
        ranked_resumes = []
        for (names, emails, resume_text) in processed_resumes:
            resume_vector = tfidf_vectorizer.transform([resume_text])
            similarity = cosine_similarity(job_desc_vector, resume_vector)[0][0] * 100
            ranked_resumes.append((names, emails, similarity))

        # Sort resumes by similarity score
        ranked_resumes.sort(key=lambda x: x[2], reverse=True)

        results = ranked_resumes
        return render_template("category.html",results=results)

    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)