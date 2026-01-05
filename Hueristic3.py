from bs4 import BeautifulSoup

class Heuristic3:
    def __init__(self , html : str , url : str):

        self.soup = BeautifulSoup(html , 'html.parser')
        self.url = url

    def get_text_from_element(self,element):

        text = (element.get_text(separator = " " , strip = True) or "").strip()
        if text == "":
            text_val = (element.get("aria-label")
                    or element.get("title")
                    or element.get("value")
                    )
            if text_val:
                text = text_val.lower()
        else:
            text = text.lower()

        return text
    def check_user_controls(self):

        navigation_words = ["back" , "cancel" , "close" , "exit" , "home" , "logout" , "log out" , "previous" , "go back" , "clear"]

        elements = []
        elements.extend(self.soup.find_all("a"))
        elements.extend(self.soup.find_all("button"))
        elements.extend(self.soup.find_all("input"))

        found_navigations = []

        index = 0
        for element in elements:
            index += 1
            text = self.get_text_from_element(element)

            if text == "":
                continue
            for word in navigation_words:
                if word in text:
                    found_navigations.append({
                        "index" : index,
                        "type" : element.name,
                        "text" : text

                    })
                    break
        results = {
            "total_checks" : len(elements),
            "found_navigations" : found_navigations,
            "samples" : found_navigations[:10]
        }
        return results
    def run_all_checks(self):
        results = self.check_user_controls()
        if len(results["found_navigations"]) > 0:
            binary_value = 1
        else:
            binary_value = 0

        return {
            "H3_summary" : {
                "user_controls" : results,
             "binary_summary" : {
                 "C3_usercontrols" : binary_value
             }
            }
        }
