from flask import Flask, render_template, request
from scraper import evaluate_page
from report_generator import generate_pdf
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    summary_data = None
    detailed_data = None
    pdf_file = None

    if request.method=='POST':
        website_url = request.form['website_url']
        summary_data , detailed_data = evaluate_page(website_url)
        if summary_data and not summary_data.get('error'):
            try:
                pdf_file = generate_pdf(website_url , summary_data , detailed_data)
            except Exception as e:
                print(f"Error in generating the report: {e}")

    return render_template("index.html", summary= summary_data, details = detailed_data , pdf_link = pdf_file)
if __name__ == '__main__':
    app.run(debug=True,port = 5001)