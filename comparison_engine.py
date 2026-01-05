import pandas as pd
import time
from scraper import evaluate_page


# --- 1. Data Loader ---
def load_simple_data():
    filename = "undp-ua-basic_web_accessibility_of_100_websites-2024-eng-2.xlsx"
    print(f"Loading data from {filename}")

    try:
        # Read Excel with openpyxl
        df = pd.read_excel(filename, header=None, engine='openpyxl')

        # Extract specific columns (Indices: ID, URL, Name, C1..C10)
        target_indices = [0, 1, 14, 35, 38, 41, 44, 47, 49, 51, 55, 58, 61]
        clean_df = df.iloc[1:, target_indices].copy()

        clean_df.columns = ['ID', 'URL', 'Name', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10']
        print(f"Loaded {len(clean_df)} websites.")
        return clean_df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


def map_tool_results_to_undp(details):
    scores = {}

    # C1: Contrast (Placeholder)
    scores['C1'] = 1

    # C2: Alt Text (H5)
    h5 = details.get("H5", {}).get("Hueristic5_voilation_summary", {})
    scores['C2'] = 0 if h5.get("C1 missing Alt", {}).get("missing_alt", 0) > 0 else 1

    # C3: Unclear Links (H5)
    scores['C3'] = 0 if h5.get("C3 unclear text", {}).get("unclear_links", 0) > 0 else 1

    # C4: Button Labels (H2)
    h2 = details.get("H2", {}).get("Heuristic2_voilations_summary", {})
    scores['C4'] = 0 if h2.get("c4", {}).get("unlabeled_count", 0) > 0 else 1

    # C5: Form Labels (H5)
    scores['C5'] = 0 if h5.get("C4 Unlabeled inputs", {}).get("missing_labels", 0) > 0 else 1

    # C6: Language (H5)
    lang_check = h5.get("C10_Html_language", {})
    scores['C6'] = 1 if lang_check.get("has_lang") else 0

    # C7: Code Errors (H8)
    h8 = details.get("H8", {}).get("H8_summary", {})
    dupes = h8.get("C7_duplicate_ids", {}).get("duplicate_results", {})
    scores['C7'] = 0 if len(dupes) > 0 else 1

    # C8: Skip Links (H7)
    h7 = details.get("H7", {}).get("H7_summary", {})
    scores['C8'] = 1 if h7.get("skip_links_check", {}).get("has_skip_links", False) else 0

    # C9: Focus Marking (H1)
    h1 = details.get("H1", {}).get("Heuristic_voilation_summary", {})
    scores['C9'] = 0 if h1.get("focus_marking", {}).get("suppressed_tags", 0) > 0 else 1

    # C10: Keyboard Support (H10)
    h10 = details.get("H10", {}).get("H10_summary", {})
    scores['C10'] = 0 if h10.get("keyboard_checks", {}).get("inaccisible_elements", 0) > 0 else 1

    return scores


def run_experiment(limit=None):
    df_undp = load_simple_data()
    if df_undp is None: return

    results_list = []

    # Loop through websites
    count = 0
    for index, row in df_undp.iterrows():
        if limit and count >= limit:
            break

        url = str(row['URL']).replace(" ", "").strip()
        count += 1
        print(f"\n Testing ({count}): {url}")

        try:

            summary, details = evaluate_page(url)

            if summary.get('error'):
                print(f"Tool Error: {summary['error']}")
                continue


            metrics = summary.get('metrics', {})
            efficiency_score = metrics.get('efficiency_score', 0)
            time_taken = metrics.get('time_taken_seconds', 0)
            tool_violations = metrics.get('total_voilations', 0)

            tool_scores = map_tool_results_to_undp(details)

            match_count = 0
            comparisons = {}
            active_criteria = ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10']

            for c in active_criteria:
                tool_val = tool_scores[c]
                undp_val = row[c]

                is_match = int(tool_val) == int(undp_val)
                comparisons[f"{c}_Match"] = 1 if is_match else 0
                if is_match:
                    match_count += 1

            agreement_score = match_count / len(active_criteria)
            print(f"Agreement: {agreement_score:.2f} | Efficiency: {efficiency_score}")

            result_row = {
                'URL': url,
                'Agreement_Score': agreement_score,
                'Efficiency_Score': efficiency_score,
                'Time_Taken_s': time_taken,
                'Tool_Violations_Count': tool_violations,
                **tool_scores,
                **comparisons
            }
            results_list.append(result_row)

        except Exception as e:
            print(f"Critical Script Error: {e}")

        time.sleep(1)

    if results_list:
        results_df = pd.DataFrame(results_list)
        results_df.to_excel("final_experiment_results.xlsx", index=False)
        print(f"COMPLETE. Saved {len(results_df)} results to 'final_experiment_results.xlsx'")
    else:
        print("\n No results generated.")


if __name__ == "__main__":
    run_experiment(limit=None)