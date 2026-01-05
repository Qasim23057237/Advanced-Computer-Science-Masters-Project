import requests
import time
from Heuristic1 import Heuristic1
from Heurictic2 import Heuric2
from Hueristic3 import Heuristic3
from Heuristic4 import Heuristic4
from Hueristic5 import Hueristic5_voilations
from Heuristic6 import Heuristic6
from Hueristic7 import Hueristic7
from Heuristic8 import  Heuristic8
from Hueristic9 import Hueristic9
from Hueristic10 import Heuristic10


def calculate_severity(heuristic_name , result_data):
    severity_score = 0

    if heuristic_name == "H1":
        #focuc marking error which is equivalent to C9
        score = result_data["Heuristic_voilation_summary"]["Binary_Summary"]["H1_total"]
        if score == 0:
            severity_score = 2
        else:
            severity_score = 0

    elif heuristic_name == "H2":
        #h2 is a match between system and real world
        score = result_data["Heuristic2_voilations_summary"]["Binary_Summary"]["H2_total"]
        if score == 0:
            severity_score = 3
        else:
            severity_score = 0
    elif heuristic_name == "H3":
        #h3 is user control and freedom
        score = result_data["H3_summary"]["binary_summary"]["C3_usercontrols"]

        if score == 0:
            severity_score = 3
        else:
            severity_score = 0
    elif heuristic_name == "H4":
        #H4 is consistency and binary
        score = result_data["H4_summary"]["binary_summary"]["H4_total"]

        if score == 0:
            severity_score = 1
        else :
            severity_score = 0

    elif heuristic_name == "H5":
        #h5 check for error prvevention did some change in severity change logic which was neccessary
        binary_summary = result_data["Hueristic5_voilation_summary"]["Binary_Summary"]
        h5_summary = result_data["Hueristic5_voilation_summary"]
        missing_alt  = h5_summary.get("C1 missing Alt",{}).get("missing_alt",0)
        unlabeled_inputs = h5_summary.get("C4 Unlabeled inputs",{}).get("missing_labels",0)
        unclear_links = h5_summary.get("C3 unclear text",{}).get("unclear_links",0)
        if unlabeled_inputs > 0:
            severity_score = 4
        elif unclear_links > 0:
            severity_score = 3
        elif missing_alt > 5:
            severity_score = 2
        elif missing_alt > 0:
            severity_score = 1
        else:
            severity_score = 0

        #is_voilation = False
       # for key in binary_summary:
          #  if binary_summary[key] == 1 :
            #    is_voilation = True
             #   break
      #  if is_voilation == True:
           # severity_score = 3
       # else :
           # severity_score = 0
    elif heuristic_name == "H6":
        score = result_data["H6_summary"]["binary_summary"]["H6_total"]
        if score == 0:
            severity_score = 2
        else :
            severity_score = 0
    elif heuristic_name == "H7":
        score = result_data["H7_summary"]["binary_summary"]["H7_total"]

        if score  == 0:
            severity_score = 2
        else:
            severity_score = 0

    elif heuristic_name == "H8":
        #score = result_data["H8_summary"]["H8_total"]
        h8_summary = result_data["H8_summary"]
        binary_summary = h8_summary.get("binary_summary", {})

        issues_found = 0

        if binary_summary.get("C1_visual_clutter") == 0 : issues_found += 1
        if binary_summary.get("C2_text_clutter") == 0 : issues_found += 1
        if binary_summary.get("C3_style_clutter") == 0 : issues_found += 1

        if issues_found >= 3:
            severity_score = 3
        elif issues_found >= 2:
            severity_score = 2
        elif issues_found >= 1:
            severity_score = 1
        else:
            severity_score = 0


        #if score == 0:
           # severity_score = 1
       # else:
          #  severity_score = 0

    elif heuristic_name == "H9":

        score = result_data["H9_summary"]["binary_summary"]["H9_total"]
        if score  == 0:
            severity_score = 4
        else :
            severity_score = 1

    elif heuristic_name == "H10":
        h10_summary = result_data["H10_summary"]["binary_summary"]
        if h10_summary.get("c10_keyboard") == 1:
            severity_score = 4
        elif h10_summary.get("c10_help") == 0:
            severity_score = 2
        else:
            severity_score = 0
       # score = result_data["H10_summary"]["binary_summary"]["c10_help"]

       # if score == 0:
          #  severity_score = 2
      #  else :
    #  severity_score = 0

    return severity_score




def evaluate_page(url):
    results = {}

    start_time = time.perf_counter()

    try:
        response = requests.get(url , timeout=5 , headers={'User-Agent': 'Mozilla/5.0'})
        html_data = response.text
    except Exception as error:
        return {"error": str(error)} , {}

    try:
        H1_checker  = Heuristic1(html_data , url)
        results["H1"] = H1_checker.run_all_checks()

        H2_checker = Heuric2(html_data , url)
        results["H2"] = H2_checker.return_all_checks()

        H3_checker = Heuristic3(html_data , url)
        results["H3"] = H3_checker.run_all_checks()

        H4_checker = Heuristic4(html_data , url)
        results["H4"] = H4_checker.run_all_checks()

        H5_checker = Hueristic5_voilations(html_data , url)
        results["H5"] = H5_checker.run_all_checks()

        H6_checker = Heuristic6(html_data , url)
        results["H6"] = H6_checker.run_all_checks()

        H7_checker = Hueristic7(html_data , url)
        results["H7"] = H7_checker.run_all_checks()

        H8_checker = Heuristic8(html_data , url)
        results["H8"] = H8_checker.run_all_checks()

        H9_checker = Hueristic9(html_data , url)
        results["H9"] = H9_checker.run_all_checks()

        H10_checker = Heuristic10(html_data , url)
        results["H10"] = H10_checker.check_runs()

    except Exception as error:
        print(error)
        return { "error": str(error)} , {}

    end_time = time.perf_counter()
    time_taken = end_time - start_time
    total_voilations = 0
    severity_mapping = {}
    sum_impact = 0
    Heuristic_list = ["H1","H2","H3","H4","H5","H6","H7","H8","H9","H10"]
    for h in Heuristic_list:
        sev = calculate_severity(h , results[h])
        severity_mapping[f"{h}_severity"] = sev
        if sev > 0 :
            total_voilations += 1
        norm_sev = sev / 4.0
        weight = 1.0 / 10.0
        sum_impact += (norm_sev * weight)
    efficiency = 0

    if time_taken > 0 :
        efficiency = total_voilations / time_taken

    usability_score  = 1.0 - sum_impact

    final_output = {
        "url" : url,
        "metrics" : {
        "time_taken_seconds" : round(time_taken,4),
        "efficiency_score" : round(efficiency,4),
        "usability_score" : usability_score,
        "total_voilations" : total_voilations
        },
        "severity_breakdown" : severity_mapping,
        "error" : None,
        "details" : results
    }
    return final_output , results






    # try:
    #     response = requests.get(url)
    #     response.raise_for_status()
    # except Exception as ex:
    #     err = {"error": str(ex)}
    #     return {"Hueristic5_voilation_summary" : err } , {"H8_summary": err}
    #
    # html = response.text
    # h5_checker = Hueristic5_voilations(html , url)
    # h5_results = h5_checker.run_all_checks()
    # h8_checker = Heuristic8(html)
    # h8_results = h8_checker.run_all_checks()
    #
    # return h5_results , h8_results


















































































