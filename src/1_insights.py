import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()


class AirportInsights:
    def __init__(self):
        self.data_dir = os.getenv("DATA_DIR", "./data")

        self.airports = pd.read_csv(os.path.join(self.data_dir, "airports.csv"))
        self.countries = pd.read_csv(os.path.join(self.data_dir, "countries.csv"))
        self.runways = pd.read_csv(os.path.join(self.data_dir, "runways.csv"))

    def run(self):
        self._airports_by_country()
        self._longest_runways()

    def _airports_by_country(self):
        """Compute the number of airports per country and identify the top 3 and bottom 10 countries."""
        self.airports_by_country = (
            self.airports.groupby("iso_country", dropna=False)
            .size()
            .reset_index(name="airport_count")
            .merge(self.countries[["code", "name"]], left_on="iso_country", right_on="code", how="left")
        )

    def get_top_countries(self, n=3):
        """Return the top n countries by airport count."""
        return self.airports_by_country.sort_values("airport_count", ascending=False).head(n)

    def get_bottom_countries(self, n=10):
        """Return the bottom n countries by airport count."""
        return self.airports_by_country.sort_values("airport_count", ascending=True).head(n)

    def _longest_runways(self):
        """Identify the longest runway for each country."""
        merged = self.runways.merge(
            self.airports[["id", "name", "iso_country"]],
            left_on="airport_ref",
            right_on="id",
            how="left",
            suffixes=("", "_airport")
        )

        idx = merged.groupby("iso_country")["length_ft"].idxmax()
        self.longest_runways = merged.loc[idx, ["iso_country", "name", "length_ft", "width_ft"]]

    def save_results(self, folder="results/1_insights", top_n=3, bottom_n=10):
        """Save computed insights to CSV files."""
        os.makedirs(folder, exist_ok=True)

        # Full datasets
        self.airports_by_country.to_csv(os.path.join(folder, "airports_by_country.csv"), index=False)
        self.longest_runways.to_csv(os.path.join(folder, "longest_runways.csv"), index=False)

        # Top / bottom N countries
        self.get_top_countries(top_n).to_csv(os.path.join(folder, f"top_{top_n}_countries.csv"), index=False)
        self.get_bottom_countries(bottom_n).to_csv(os.path.join(folder, f"bottom_{bottom_n}_countries.csv"), index=False)

        print(f"Results saved to '{folder}' folder.")
    
if __name__ == "__main__":
    insights = AirportInsights()
    insights.run()
    insights.save_results()

  
    print("Top 3 countries by airport count:")
    print(insights.get_top_countries(3))

    print("Bottom 10 countries by airport count:")
    print(insights.get_bottom_countries(10))

    print("Longest runways by country (example):")
    print(insights.longest_runways.head(10))