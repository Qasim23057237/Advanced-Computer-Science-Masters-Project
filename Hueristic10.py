from bs4 import BeautifulSoup

class Heuristic10:

    def __init__(self , html : str , url : str):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.url = url

    def check_help_links(self):
        keywords = ["help" , "support" , "contact" , "faq" , "documentation" , "Contact Us" ]

        links = self.soup.find_all('a')
        help_links = []

        for index, link in enumerate(links , start =1):
            text = link.get_text(strip = True).lower() if link.get_text() else ""
            href = link.get('href' , "").lower()

            for word in keywords:
                if word in text or word in href:
                    help_links.append({
                        "index" : index,
                        "text" : text,
                        "href" : href
                    })
                    break
        result = {
            "total_links" : len(links),
            "help_links" : len(help_links),
            "samples" : help_links[:5]
        }
        return result
    def check_keyboard_functionality(self):
        interactive_element = self.soup.find_all(['div', 'span' , 'a'] , attrs={"onclick" : True})
        inaccesible_elements = []

        for tag in interactive_element:
            is_div_span = tag.name in ['div', 'span']
            missing_tabindex =  not tag.get('tabindex')

            is_broken_link = tag.name == 'a' and not tag.get('href')
            if (is_div_span and missing_tabindex) or is_broken_link:
                inaccesible_elements.append(str(tag)[:60])

        return{
            "total_interactive_elements" : len(interactive_element),
            "inaccisible_elements" : len(inaccesible_elements),
            "samples" : inaccesible_elements[:5]
        }


    def check_runs(self):
        help_links_result = self.check_help_links()
        keyboard_check = self.check_keyboard_functionality()

        if help_links_result["help_links"] > 0:
            help_binary = 1
        else :
            help_binary = 0
        binary_summary = {
            "c10_help" : help_binary
        }

        if keyboard_check["inaccisible_elements"] > 0:
            keyboard_binary = 1
        else:
            keyboard_binary = 0

        binary_summary = {
            "c10_help" : help_binary,
            "c10_keyboard" : keyboard_binary
        }


        return {
            "H10_summary" : {
                "help_links" : help_links_result,
                "keyboard_checks" : keyboard_check,
                "binary_summary" : binary_summary
            }
        }






