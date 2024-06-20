# OCR Flask App
This is a simple OCR(Optical CHaracter Recognition) Flask application that allows the user to upload an image and extract text from it using Tesseract. It also allows to generate a report in PDF format with total number of words, top ten repeating words including the number of times they are repeating and a bar chart showing these words.

## Features
- Upload an image and extract text from it.
- Display the extracted text.
- Generate a PDF report with the following:
  - Total word count.
  - Top 10 most frequent words with their counts.
  - A bar chart of the top 10 words.

 ## Prerequisites
 - Python 3.6 or higher
- Tesseract OCR installed on your system. You can download it from (https://github.com/tesseract-ocr/tesseract)

## Installation
Step 1: Clone Repository

   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```
Step 2: Create Virtual Environment
   
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```
    
Step 3: Install Dependencies

    ```bash
    pip install -r requirements.txt
    ```
Step 4: Running Application 

    ```bash
    python main.py
    ```
Note: Check if your Tesseract ocr is correctly installed.

## Directory Structure

.
├── main.py

├── requirements.txt

├── templates

│   ├── index.html

│   └── result.html

└── README.md




    


  

