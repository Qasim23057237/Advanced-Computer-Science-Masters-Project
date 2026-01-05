import requests
from bs4 import BeautifulSoup

class Hueristic9:
    def __init__(self,html : str ,  url : str):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.url = url
    def check_404_page(self):
        url = self.url.rstrip('/')+ "/random-example-page"
        try:
            response = requests.get(url , timeout=5)
            status_code = response.status_code
            is_code_404 = (status_code == 404)
        except Exception:
            status_code = "Error"
            is_code_404 = False
        return {
            "status_code" : status_code,
            "is_code_404" : is_code_404
        }
    def check_for_alerts(self):

        alerts = self.soup.find_all(attrs={"role" : "alert"})

        error_classes = self.soup.select(".alert , .error , .invalid-feedback")

        found_alerts = len(alerts) + len(error_classes)

        has_error_applied = found_alerts > 0

        return {
          "alerts_found" : len(alerts),
            "error_classes" : len(error_classes),
            "has_error_applied" : has_error_applied
        }

    def run_all_checks(self):
        check_404 = self.check_404_page()
        check_for_alerts = self.check_for_alerts()
        h9_binary =     1 if (check_404["is_code_404"] or check_for_alerts["has_error_applied"]) else 0

        return{
            "H9_summary" : {
                "404_check" : check_404,
                "alert_check" : check_for_alerts,
                "binary_summary" : {
                    "C7_error" : h9_binary,
                    "H9_total" : h9_binary
                }
            }
        }