import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.style.core import available


class GenerateGraph:
    def __init__(self, excel_path: str , output_dir: str = "graphs_out"):
        self.excel_path = excel_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.df = pd.read_excel(self.excel_path)

        self.df = self.df.dropna(subset=["Agreement_Score"])

    def _save(self , filename: str):
        path = os.path.join(self.output_dir, filename)
        plt.tight_layout()
        plt.savefig(path , dpi = 300)
        plt.close()
        return path
    def plot_agreement_histogram(self):
        plt.figure()
        plt.hist(self.df["Agreement_Score"] , bins = 10)
        plt.xlabel("Agreement Score (0 - 1)")
        plt.ylabel("Number of websites")
        plt.title("Agreement Score Distribution")
        return self._save("agreement_histogram.png")

    def plot_effecincy_vs_time(self):
        plt.figure()
        plt.scatter(self.df["Time_Taken_s"], self.df["Efficiency_Score"])
        plt.xlabel("Time Taken in seconds")
        plt.ylabel("Efficiency Score")
        plt.title("Efficiency vs Time Taken")
        return self._save("effecincy_vs_time.png")

    def plot_accuracy_by_criterion(self):
        match_columns = [f"C{i}_Match" for i in range(2,11)]
        available = [c for c in match_columns if c in self.df.columns]

        means  = self.df[available].mean(numeric_only=True)
        plt.figure()
        plt.bar(means.index, means.values)
        plt.xlabel("Criterion")
        plt.ylabel("Mean Agreement (0 - 1)")
        plt.title("Agreement with expert by Citeration")
        return self._save("accuracy_by_criterion.png")

    def plot_tools_passrate_by_criterion(self):

        crit_columns = [f"C{i}" for i in range(2,11)]
        available = [c for c in crit_columns if c in self.df.columns]

        means = self.df[available].mean(numeric_only=True)
        plt.figure()
        plt.bar(means.index, means.values)
        plt.xlabel("Criterion")
        plt.ylabel("Tool Passrate (0 - 1)")
        plt.title("Tool Passrate by Criterion")
        return self._save("tools_passrate_by_criterion.png")

    def generate_all(self):
        paths = []
        paths.append(self.plot_agreement_histogram())
        paths.append(self.plot_effecincy_vs_time())
        paths.append(self.plot_accuracy_by_criterion())
        paths.append(self.plot_tools_passrate_by_criterion())
        return paths
if __name__ == "__main__":
        gg = GenerateGraph("final_experiment_results.xlsx" , output_dir="graphs_out")
        out = gg.generate_all()
        print("Saved Graphs: ")
        for p in out:
            print(" _" , p)

