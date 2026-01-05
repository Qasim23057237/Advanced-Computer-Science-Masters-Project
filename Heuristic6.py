from bs4 import BeautifulSoup

class Heuristic6:
    def __init__(self, html : str , url : str):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.url = url
    def check_navigations(self):
        nav_tags = self.soup.find_all('nav')

        menu_keywords = ["nav" , "menu" , "header"]
        non_semantic_navs = []

        divs_and_lists = self.soup.find_all(['div' , 'ul'])
        for tag in divs_and_lists:
            classes = tag.get('class')
            if classes:

                if any(keyword in " ".join(classes).lower() for keyword in menu_keywords):
                    non_semantic_navs.append(str(tag.name))
        has_navigation = len(nav_tags) > 0 or len(non_semantic_navs) > 0

        return{
            "semenstic_nav_count" : len(nav_tags),
            "potential_nav_elements" : len(non_semantic_navs),
            "has_navigation" : has_navigation

        }
    def check_page_heading(self):

        h1_tags = self.soup.find('h1')

        has_h1 = h1_tags is not None

        h1_text = h1_tags.get_text(strip=True )if has_h1 else 'No h1 found'

        return{
            "has_h1" : has_h1,
            "h1_text" : h1_text[:50]
        }

    def run_all_checks(self):
        nav_checks = self.check_navigations()
        page_heading = self.check_page_heading()

        h6_binary = 1 if (nav_checks["has_navigation"] and page_heading["has_h1"]) else 0

        return {
            "H6_summary" : {
                "nav_check" : nav_checks,
                "page_heading" : page_heading,
                "binary_summary" : {
                    "C8_navigation" : h6_binary,
                    "H6_total" : h6_binary
                }
            }
        }