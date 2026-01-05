from collections import Counter

from bs4 import BeautifulSoup

class Heuristic8:

    def __init__(self, html : str , url : str):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.url = url

    def check_duplicate_ids(self):
        all_tags = self.soup.find_all(attrs={"id": True})
        ids = [tag["id"] for tag in all_tags]
        total_id_counts = Counter(ids)
        dupicates = {}
        for id_names , count in total_id_counts.items():
            if count > 1:
                dupicates[id_names] = count
        duplicate_results = []

        for id , count in dupicates.items():
            duplicate_results.append({"id" : id, "count" : count})
        return {
            "total_ids" : len(ids),
            "duplicate_results" : dupicates,
            "samples" : duplicate_results[:5]
        }

    def check_for_visual_clutter(self):
        images = self.soup.find_all("img")
        iframes = self.soup.find_all("iframe")
        videos = self.soup.find_all("video")

        total_elements = len(images) + len(iframes) + len(videos)

        visual_element_limit = 40
        is_clutter = total_elements > visual_element_limit

        result =\
            {
                "total_images" : len(images),
                "total_iframes" : len(iframes),
                "total_videos" : len(videos),
                "total_elements" : total_elements,
                "visual_element_limit" : visual_element_limit,
                "is_clutter" : is_clutter,

            }
        return result
    def check_word_clutter(self):
        paragraphs = self.soup.find_all("p")
        long_paragraphs = []

        paragraph_limit = 400

        for index , paragraph in enumerate(paragraphs , start = 1):
            paragraph_text = paragraph.get_text()
            length = len(paragraph_text)
            if length > paragraph_limit:
                paragraph_sample = paragraph_text[:20]
                long_paragraphs.append(
                    {
                        "index" : index,
                        "length" : length,
                        "sample" : paragraph_sample

                    }
                )

        result = {
            "total_paragraphs" : len(paragraphs),
            "total_paragraph_count" : len(long_paragraphs),
            "paragraph_limit" : paragraph_limit,
            "samples" : long_paragraphs[:5]
        }
        return result

    def check_style_clutter(self):
        scripts_tags = self.soup.find_all("script")
        style_tags = self.soup.find_all("style")
        css_links = []

        for link in self.soup.find_all("link"):
            rel = link.get("rel")
            if rel and "stylesheet" in [r.lower() for r in rel]:
                css_links.append(link)
        total_scripts = len(scripts_tags)
        total_styles = len(style_tags) + len(css_links)

        script_limit = 20
        style_limit = 15

        too_many_scripts = total_scripts > script_limit
        too_many_styles = total_styles > style_limit
        result = {
            "total_scripts" : total_scripts,
            "total_styles" : style_tags,
            "css_links" : css_links,
            "total_style_elements" : total_styles,
            "script_limit" : script_limit,
            "too_many_scripts" : too_many_scripts,
            "too_many_styles" : too_many_styles,

        }
        return result

    def run_all_checks(self):
        C7_duplicates = self.check_duplicate_ids()
        C1_visual = self.check_for_visual_clutter()
        C2_text_clutter = self.check_word_clutter()
        C3_style_clutter = self.check_style_clutter()

        c7_binary = 1 if len(C7_duplicates["duplicate_results"]) == 0 else 0
        binary_summary = {

            "C1_visual_clutter" : 1 if C1_visual["is_clutter"] == 0 else 0,
            "C2_text_clutter" : 1 if C2_text_clutter["total_paragraph_count"] == 0 else 0,
            "C3_style_clutter" : 1 if not (C3_style_clutter["too_many_scripts"] or C3_style_clutter["too_many_styles"]) else 0,



        }

        h8_total = 1 if (c7_binary and binary_summary["C1_visual_clutter"] and binary_summary["C2_text_clutter"] and binary_summary["C3_style_clutter"]) else 0


        return {
            "H8_summary" :
                {
                    "C7_duplicate_ids" : C7_duplicates,
                    "C1_visual" : C1_visual,
                    "C2_text_clutter" : C2_text_clutter,
                    "C3_style_clutter" : C3_style_clutter,
                    "binary_summary" : binary_summary,
                    "H8_total" : h8_total
                }
        }


