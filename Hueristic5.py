from bs4 import BeautifulSoup
from urllib.parse import urlparse , urljoin
import requests

class Hueristic5_voilations:
    def __init__(self, html : str , base_url : str):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.base_url = base_url
        self.base_host = urlparse(base_url).netloc

    def check_missing_alt(self):
        imgs = self.soup.find_all('img')
        missing_alt = []
        for i, img in enumerate(imgs, start=1):
            alt = (img.get('alt') or "").strip()
            if not alt:
                src = (img.get('src') or "")[:120]
                missing_alt.append({"index": i , "src": src})
        return {
            "total_images": len(imgs),
            "missing_alt": len(missing_alt),
            "samples" : missing_alt[:10]
        }

    def check_unclear_links(self):
        unclear_words = {"click here" , "here" , "read more" , "learn more" , "more" , "details" , "links"}
        unclear_links = []
        links = self.soup.find_all('a')
        for a in links:
            text = (a.getText(separator=" " , strip= True)).lower()
            has_image_only = (not text) and a.find('img') and not (a.get("aria-label") or a.get("title"))
            if (text in unclear_words) or has_image_only:
                href = (a.get('href') or "") [:120]
                unclear_links.append({"text" : text or "[no visible text]" , "href" : href})
        return {"total links ": len(links), "unclear_links": len(unclear_links) , "samples ": unclear_links[:10]}

    def check_labels(self, inp):
        iid = inp.get("id")
        if iid and self.soup.find_all("label" , attrs={"for": iid}):
            return True
        p = inp.parent
        while p and getattr(p, "name" , None):
            if p.name == "label":
                return True
            p = p.parent
        if inp.get("aria-label") or inp.get("aria-labelledby"):
            return True
        return False

    def check_unlabeled_inputs(self):
        all_inputs = []
        for tag in self.soup.find_all(["input" , "textarea" , "select"]):
            input_type = tag.get("type" , "").lower()
            if input_type not in ["hidden" , "submit" , "image" , "button" , "reset"]:
                all_inputs.append(tag)

        missing_labels = []
        count = 0

        for inp in all_inputs:
            count += 1
            has_labels = False

            if inp.get("id"):
                label = self.soup.find_all("label" , attrs={"for": inp.get("id")})
                if label:
                    has_labels = True
            if not has_labels:
                 parent  = inp.find_parent("label")
                 if parent:
                    has_labels = True
            if not has_labels:
                if inp.get("aria-label") or inp.get("aria-labelledby") or inp.get("title"):
                    has_labels = True
            if not has_labels:
                field_name = inp.get("name") or inp.get("id") or str(inp)[:30]
                missing_labels.append({"index" : count, "text" : field_name})
        return {
            "total_fields": len(all_inputs),
            "missing_labels": len(missing_labels),
            "samples ": missing_labels[:10]
        }


    def check_basic_voilation(self):
        forms = self.soup.find_all("form")
        flagged_forms = 0
        details = []
        for form in forms:
            inputs = form.find_all(["input" , "textarea"])
            has_any = False
            for input in inputs:
                if any (attr in input.attrs for attr in ["required" , "pattern" , "minlength" , "maxlength"]):
                    has_any = True
                    break
                if input.get("type", "").lower() in {"email" , "url" , "number"}:
                    has_any = True
                    break
            if not has_any and inputs:
                flagged_forms += 1
                details.append({"action": (form.get("action") or "")[:120] , "inputs" : len(inputs)})
        return {"total_forms": len(forms), "flagged_forms": flagged_forms, "samples": details[:5]}

    def check_html_language(self):
            html_tag = self.soup.find("html")
            if html_tag and html_tag.get("lang"):
                lang_value = html_tag.get("lang").strip()
                has_lang = True
            else:
                lang_value = ""
                has_lang = False
            return {
                "has_lang" : has_lang,
                "lang_value" : lang_value,
            }
    def run_all_checks(self):
        c1 = self.check_missing_alt()
        c3 = self.check_unclear_links()
        c4 = self.check_unlabeled_inputs()
        c5 = self.check_basic_voilation()
        c10 = self.check_html_language()

        if c1["missing_alt"] > 0:
            c1_binary = 1
        else:
            c1_binary = 0
        if c3["unclear_links"] > 0:
            c3_binary = 1
        else:
            c3_binary = 0

        if c4["missing_labels"] > 0:
            c4_binary = 1
        else:
            c4_binary = 0
        if c5["flagged_forms"] > 0:
            c5_binary = 1
        else:
            c5_binary = 0

        if c10["has_lang"] > 0:
            c10_binary = 0
        else:
            c10_binary = 1
        binary_summary =\
            {
            "C1" : c1_binary,
            "C3" : c3_binary,
            "C4" : c4_binary,
            "C5" : c5_binary,
            "C10" : c10_binary
            }

        return{
            "Hueristic5_voilation_summary" :
            {
                "C1 missing Alt": c1,
                "C3 unclear text" : c3,
                "C5 forms without validation" : c5,
                "C4 Unlabeled inputs": c4,
                "C10_Html_language" : c10,
                "Binary_Summary" : binary_summary
            }
        }



