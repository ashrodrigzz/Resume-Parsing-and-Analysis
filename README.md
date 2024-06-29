# Resume-Parsing-and-Analysis <br>
I am excited to present a resume parsing and analysis model that I have developed. This project takes in the job description, matches one or more resumes with it, and identifies the best fit resume for the given job role. This model streamlines the hiring process by efficiently matching candidate qualifications with job requirements, ensuring that the most suitable candidates are highlighted for consideration.<br>
**Dataset:** <br> To ensure the model's accuracy and effectiveness, I have used many resumes to train it. <br>
**Approach used:** <br> I have retrieved the job description and a list of resumes from the Flask Python framework. The text is extracted from resume’s PDF files and entities such as name and email address are extracted using the Spacy library. TF-IDF vectorization is applied to transform the text data. Cosine similarity is then used to find the similarity between the resume details and the job description. This similarity score helps identify the best fit resume for the job description.<br>
**Set-Up Instruction:** <br>
•	Install and Open Visual Code Studio application for windows.<br>
o	https://code.visualstudio.com/download<br>
•	Python Version: Python 3.12.4<br>
•	Install requirement.txt using the below code<br>
o	!pip install -r **requirement.txt**<br>
•	Run python **app.py**<br>
