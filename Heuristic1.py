from bs4 import BeautifulSoup
import re
class Heuristic1:
    def __init__(self , html : str , url : str):
        self.soup = BeautifulSoup(html , "html.parser")
        self.url = url
    def check_focus_marking(self):

        bad_focus_elements = self.soup.find_all(attrs = {"style" : re.compile(r"outline\s*:\s*(none|0)",re.I)})

        bad_focus_element_list = []
        for tag in bad_focus_elements:
            bad_focus_element_list.append(str(tag)[:50])
        return {
            "suppressed_tags" : len(bad_focus_elements),
            "sample" : bad_focus_element_list[:5]
        }
    def check_title(self):
        title = self.soup.find("title")
        has_title =  bool(title and title.get_text(strip= True))
        title_text = title.get_text(strip = True) if has_title else "No title"
        return {
            "has_title" : has_title,
            "title_text" : title_text
        }
    def check_breadcrumbs(self):

        crumbs_aria = self.soup.find(attrs={"aria-label" : re.compile("breadcrumb" , re.I)})
        crumbs_class = self.soup.find(class_ = re.compile("breadcrumb" , re.I))

        has_crumbs = bool(crumbs_aria or crumbs_class)

        return{
            "has_breadcrumbs" : has_crumbs,
        }
    def run_all_checks(self):
        focus = self.check_focus_marking()
        title = self.check_title()
        breadcrumbs = self.check_breadcrumbs()

        c9_binary = 1 if focus["suppressed_tags"] == 0 else 0

        title_binary = 1 if title["has_title"] else 0

        crumbs_binary = 1 if breadcrumbs["has_breadcrumbs"] else 0

        h1_binary =1 if (c9_binary == 1 and title_binary == 1) else 0

        return {
            "Heuristic_voilation_summary" :{
                "focus_marking" : focus,
                "page_title" : title,
                "breadcrumbs" : breadcrumbs,
                "Binary_Summary" : {
                    "C9" : c9_binary,
                    "Title" : title_binary,
                    "Breadcrumbs" : crumbs_binary,
                    "H1_total" : h1_binary,

                }
            }


        }

