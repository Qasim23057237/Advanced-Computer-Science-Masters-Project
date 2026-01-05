from fpdf import FPDF
import matplotlib
import matplotlib.pyplot as plt
import datetime
import os

matplotlib.use('Agg')

class ReportGenerator(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10 , 'Usability Report' , 0 , 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0 , 10 , f'Page {self.page_no()} ', 0 , 0, 'C' )


def get_error_list(data):
    found_errors = []

    # CASE 1: The item is a Dictionary (A Box)
    if isinstance(data, dict):
        for key, value in data.items():

            # Did we find the treasure? (Key is 'samples')
            if key == 'samples' and isinstance(value, list):
                found_errors.extend(value)  # Grab it!

            # Is this another box? (Nested Dictionary)
            elif isinstance(value, dict):
                # RECURSION: "Run this whole function again on this smaller box"
                found_errors.extend(get_error_list(value))

            # Is this a list of items?
            elif isinstance(value, list):
                for item in value:
                    # If an item in the list is a box, search it too!
                    if isinstance(item, dict):
                        found_errors.extend(get_error_list(item))

    # CASE 2: The item is a List
    elif isinstance(data, list):
        for item in data:
            # Check every item in the list
            if isinstance(item, dict):
                found_errors.extend(get_error_list(item))

    return found_errors


def severity_chart(summary_data):
        heuristics = ["H1" , "H2" , "H3" , "H4" , "H5" , "H6" , "H7" , "H8" , "H9" , "H10"]
        scores = []
        colors = []
        severities = summary_data.get('severity_breakdown', {})
        for h in heuristics:
            score = severities.get(f"{h}_severity", 0)
            scores.append(score)
            if score == 4 : colors.append('red')
            elif score == 3 : colors.append('orange')
            elif score > 0  : colors.append('gold')
            else : colors.append('green')
        plt.figure(figsize = (10,4))
        plt.bar(heuristics, scores , color = colors)
        plt.title("Severity Overview (4 = Criticial)")
        plt.ylim(0 , 4.5)
        plt.ylabel("Severity")

        if not os.path.exists('static'):
            os.makedirs('static')
        file_name = 'static/chart_img.png'
        plt.savefig(file_name)
        plt.close()
        return file_name
def generate_pdf(url , summary_data , detailed_data):
        pdf = ReportGenerator()
        pdf.add_page()
        pdf.set_font('Arial', '', 12)
        pdf.cell(0 , 10 , f"Target : {url}" , 0 , 1 )
        pdf.cell(0 , 10 , f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}" , 0 , 1 )
        pdf.ln(10)

        chart_file = severity_chart(summary_data)
        pdf.image(chart_file , x = 10 , w = 190)
        pdf.ln(10)


        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0 , 10 , "Detailed Findings" , 0 , 1 )
        pdf.ln(5)
        heuristics = ["H1" , "H2" , "H3" , "H4" , "H5" , "H6" , "H7" , "H8" , "H9" , "H10"]

        for h in heuristics:
            score = summary_data.get("severity_breakdown" , {}).get(f"{h}_severity", 0)
            if score > 0:
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(0 , 10 , f"{h} - Severity {score}/4" , 0 , 1 )

                h_data = detailed_data.get( h ,  {})
                errors_samples = get_error_list(h_data)
                pdf.set_font('Arial', '', 10)
                if errors_samples:
                    count = 0
                    for error in errors_samples:
                        count += 1
                        text = str(error).encode("latin-1" , "replace").decode('latin-1')
                        pdf.cell(10)
                        pdf.multi_cell(0 , 6, f"- {text[:150]}")

                        if count >= 5:
                            pdf.cell(10)
                            pdf.cell(0 , 6, "see raw data for more details" , 0 , 1 )
                            break
                else:
                    pdf.cell(10)
                    pdf.cell(0 , 6, "Issues detected no text sample available" , 0 , 1 )
                pdf.ln(5)


        file_name = f"report_{datetime.datetime.now().strftime('%H%M%S')}.pdf"
        pdf.output(f"static/{file_name}")
        return file_name