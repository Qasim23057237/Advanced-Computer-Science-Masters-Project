from bs4 import BeautifulSoup

class Heuric2():
    def __init__(self , html : str , url : str = " "):
        self.soup = BeautifulSoup(html , 'html.parser')
        self.url = url


    def check_language(self):
        html_tag = self.soup.find("html")
        if html_tag and html_tag.get("lang"):
            return {"has_lang" : True , "lang" : html_tag.get("lang")}
        return { "has_lang" : False, "lang" : None}

    def check_unclear_links(self):
        unclear_links = []
        all_links = self.soup.findAll("a")
        for i , link in enumerate(all_links, start=1):
            text = link.get_text(separator= " " , strip = True).lower()
            has_aria = link.get("aria-label") or link.get("title")

            unclear_words = ["click here" , "here" , "read more" , "more" , "details"]
            if text in unclear_words and not  has_aria:
                unclear_links.append({"index" : i, "issue" : "unclear text " , "html" : str(link)[:50]})

            elif not text and not has_aria:

                img = link.find("img")
                if not (img and img.get("alt")):
                    unclear_links.append({"index" : i , "issue" : "no text" , "html" : str(link)[:50]})

        return {"total_links " : len(all_links), "unclear_links" : len(unclear_links) , "samples" : unclear_links[:5]}



    def check_button_labels(self):

        buttons = self.soup.findAll("button")
        unlabeled_buttons = []
        for i , button in enumerate(buttons, start=1):
            text = button.get_text(strip=True)
            has_aria = button.get("aria-label") or button.get("aria-labelledby") or button.get("title") or button.get("value")

            if not text and not has_aria:
                unlabeled_buttons.append({"index " : i , "html" : str(button)[:50]})
        return {"total_buttons" : len(buttons) , "unlabeled_count" : len(unlabeled_buttons) , "samples" : unlabeled_buttons[:5]}

    def return_all_checks(self):
        lang_check  = self.check_language()
        unclear_links = self.check_unclear_links()
        button_labels = self.check_button_labels()

        c6_binary  = 1 if lang_check["has_lang"]  else 0
        c3_binary = 1 if unclear_links["unclear_links"] == 0 else 0
        c4_binary = 1 if button_labels["unlabeled_count"] == 0 else 0

        h2_binary = 1 if (c6_binary and c3_binary and c4_binary) else 0

        return {
            "Heuristic2_voilations_summary" : {
                "c6" : lang_check,
                "c3" : unclear_links,
                "c4" : button_labels,

                "Binary_Summary" : {
                    "c6" : c6_binary,
                    "c3" : c3_binary,
                    "c4" : c4_binary,
                    "H2_total" : h2_binary
                }
            }
        }
