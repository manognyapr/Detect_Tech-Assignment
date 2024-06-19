from flask import Flask, request, render_template, redirect, url_for, send_file
import pytesseract
from PIL import Image
import os
from collections import Counter
import matplotlib.pyplot as plt
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        text, word_counts = extract_text(filepath)
        total_word_count = sum(word_counts.values())
        report_path = create_report(word_counts, filename, total_word_count)
        return render_template('result.html', text=text, report_path=report_path)

def extract_text(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    word_counts = Counter(text.split())
    return text, word_counts

def create_report(word_counts, filename, total_word_count):
    # Create a bar chart
    words, counts = zip(*word_counts.most_common(10))  # Top 10 words
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts)
    plt.xlabel('Words')
    plt.ylabel('Counts')
    plt.title('Top 10 Words by Count')
    plt.xticks(rotation=45)
    
    # Save the plot to a temporary file
    img_tempfile = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    plt.savefig(img_tempfile.name, format='png')
    img_tempfile.close()
    plt.close()

    # Create a PDF with the report
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{filename}.pdf')
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawString(100, 750, "OCR Report")
    c.drawString(100, 735, f"File: {filename}")
    c.drawString(100, 720, f"Total Word Count: {total_word_count}")
    c.drawString(100, 705, "Top 10 Word Counts:")
    
    y = 685
    for word, count in word_counts.most_common(10):
        if y < 100:  # Check if we need to start a new page
            c.showPage()
            y = 750
        c.drawString(100, y, f"{word}: {count}")
        y -= 20  # Adjust spacing to avoid overlap

    # Draw the bar chart image
    y -= 20  # Add some space before the chart
    c.drawImage(img_tempfile.name, 100, y - 300, width=400, height=300)

    c.save()
    
    # Clean up the temporary image file
    os.remove(img_tempfile.name)
    
    return f'{filename}.pdf'

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
