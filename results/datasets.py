import pandas as pd
import matplotlib.pyplot as plt

file_paths = {
    "goodwill": "/Users/janellemarie/Downloads/Goodwill Value - Sheet1.csv",
    "yearly_sales": "/Users/janellemarie/Downloads/Fashion Yearly Sales Data - Sheet1.csv",
    "quarterly_sales": "/Users/janellemarie/Downloads/Fashion Brand Quarterly Sales - Sheet1 (1).csv",
    "h&m_goodwill": "/Users/janellemarie/Downloads/h&m_goodwill_converted.csv",
    "h&m_quarterly_sales": "/Users/janellemarie/Downloads/h&m_quarterly_sales_converted.csv",
    "h&m_sales": "/Users/janellemarie/Downloads/h&m_sales_converted.csv",
}

dataframes = {name: pd.read_csv(path) for name, path in file_paths.items()}

data_preview = {name: df.head() for name, df in dataframes.items()}

dataframes["h&m_quarterly_sales"].rename(columns={"Net Sales (USD Millions)": "Net Sales ($ Millions)"}, inplace=True)
dataframes["h&m_goodwill"].rename(columns={"Goodwill Value (USD Millions)": "Goodwill Value ($ Millions)"}, inplace=True)

h_m_quarterly_sales = dataframes["h&m_quarterly_sales"][["Year", "Brand", "Luxury or Mass-Market", "Net Sales ($ Millions)", "Fiscal Quarter"]]
h_m_goodwill_data = dataframes["h&m_goodwill"][["Year", "Brand", "Luxury or Mass-Market", "Goodwill Value ($ Millions)"]]

quarterly_sales = dataframes["quarterly_sales"][["Year", "Brand", "Luxury or Mass-Market", "Net Sales ($ Millions)", "Fiscal Quarter"]]

quarterly_sales = pd.concat([quarterly_sales, h_m_quarterly_sales])

quarterly_sales_grouped = quarterly_sales.groupby(["Year", "Luxury or Mass-Market"])["Net Sales ($ Millions)"].sum().unstack()

goodwill_data = dataframes["goodwill"][["Year", "Brand", "Luxury or Mass-Market", "Goodwill Value ($ Millions)"]]

goodwill_data = pd.concat([goodwill_data, h_m_goodwill_data])

goodwill_grouped = goodwill_data.groupby(["Year", "Luxury or Mass-Market"])["Goodwill Value ($ Millions)"].sum().unstack()

plt.figure(figsize=(12, 6))

plt.plot(quarterly_sales_grouped.index, quarterly_sales_grouped["Luxury"], label="Luxury Sales ($M)", linestyle="-", marker="o")
plt.plot(quarterly_sales_grouped.index, quarterly_sales_grouped["Mass-Market"], label="Mass-Market Sales ($M)", linestyle="--", marker="o")

plt.plot(goodwill_grouped.index, goodwill_grouped["Luxury"], label="Luxury Goodwill ($M)", linestyle="-", marker="s")
plt.plot(goodwill_grouped.index, goodwill_grouped["Mass-Market"], label="Mass-Market Goodwill ($M)", linestyle="--", marker="s")

events = {
    2016: "2016 Election",
    2020: "COVID-19 & 2020 Election",
    2022: "Inflation Surge",
}
for year, label in events.items():
    plt.axvline(x=year, color="gray", linestyle=":", alpha=0.7)
    plt.text(year, plt.ylim()[1] * 0.9, label, rotation=45, verticalalignment="top")

plt.xlabel("Year")
plt.ylabel("Sales & Goodwill ($M)")
plt.title("Sales Trends and Goodwill Valuations (2012-2024)")
plt.legend()
plt.grid(True)

plt.show()

