from bs4 import BeautifulSoup

class Heuristic4:
    def __init__(self, html : str , url : str):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.url = url

    def check_buttons_consitency(self):
        buttons = self.soup.find_all('button')
        link_buttons = self.soup.find_all('a' , class_ = True)

        all_styles = []

        for button in buttons:
            classes = button.get('class')
            if classes :
                style_name = " ".join(sorted(classes))
                all_styles.append(style_name)
            else :
                all_styles.append("default_browser_style")
        for link_button in link_buttons:
            classes = link_button.get('class')
            if classes and any ("btn" in c.lower() or "button" in c.lower() for c in classes):
                style_name = " ".join(sorted(classes))
                all_styles.append(style_name)

        total_buttons_found = len(all_styles)
        unique_styles = list(set(all_styles))
        unique_count = len(unique_styles)

        is_style_consistent = unique_count <= 5

        return {
            "total_buttons_found" : total_buttons_found,
            "unique_styles" : unique_styles,
            "styles_found" : unique_styles[:10],
            "is_style_consistent" : is_style_consistent
        }
    def run_all_checks(self):
        consistency_result = self.check_buttons_consitency()
        h4_binary = 1 if consistency_result["is_style_consistent"] else 0

        return {
            "H4_summary" :
                {
                    "consistency_check" : consistency_result,
                    "binary_summary" :{
                        "C7" : h4_binary,
                        "H4_total" : h4_binary
                    }
                }
        }

