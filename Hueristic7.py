from bs4 import BeautifulSoup

class Hueristic7:
    def __init__(self , html : str , url : str):
        self.soup = BeautifulSoup(html , 'html.parser')
        self.url = url

    def check_search_bar(self):
        search_inputs = []
        inputs = self.soup.find_all('input')
        for input in inputs:
            type_attr = input.get('type' , "").lower()
            name_attr = input.get('name' , "").lower()
            id_attr = input.get('id' , "").lower()
            placeholder_attr = input.get('placeholder' , "").lower()

            if (type_attr == 'search'
                or "search" in name_attr or
                "search" in placeholder_attr or
                "search" in id_attr):
                search_inputs.append(str(input)[:50])
        has_search = len(search_inputs) > 0
        return {
            "has_search_bar" : has_search,
            "count" : len(search_inputs),
            "samples" : search_inputs[:3]
        }
    def check_skip_links(self):
        skip_keywords = ["skip to" , "jump to" , "main content"]

        all_links = self.soup.find_all('a')
        potential_links = []
        found_functional_skip = False
        for link in all_links:
            link_text = link.get_text(strip = True).lower()
            link_href = str(link.get("href") or "").lower()


            if link_href.startswith("#"):
                is_skip_text = False
                for keyword in skip_keywords:
                    if keyword in link_text:
                        is_skip_text = True
                        break
                if is_skip_text:
                    potential_links.append(link)
                    target_id =link_href.lstrip("#")
                    target_element = self.soup.find(id = target_id)
                    if target_element:
                        found_functional_skip = True
                        break

        return{
            "has_skip_links" : found_functional_skip,
            "count_potential" : len(potential_links),
            "status_details" : "Functional Link Found" if found_functional_skip else "Functional Link Not Found"
        }
    def run_all_checks(self):
        search = self.check_search_bar()
        skip_links = self.check_skip_links()
        h7_binary = 1 if (search["has_search_bar"] or skip_links["has_skip_links"]) else 0

        return {
            "H7_summary" : {
                "search_bar_check" : search,
                "skip_links_check" : skip_links,
                "binary_summary" :
                    {
                        "C8" : h7_binary,
                        "H7_total" : h7_binary,
                    }
            }
        }

