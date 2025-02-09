# Description: Fetches the results of the Cangur competition from the official website
import itertools
import pandas as pd


grades = (
    "5e 6e 1s 2s 3s 4s 1b 2b".split()
)  # e stands for "primaria" (?), s for "secundaria" and b for "batxillerat"
years = [2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024]  # no cangur in 2020


def prefix(grade):
    """Map a grade to the prefix used in the URL."""
    number, letter = grade
    if letter == "e":
        return "p"
    elif letter == "s":
        if number in ("1", "2"):
            return "2"
        else:
            return "3"
    elif letter == "b":
        return "b"


dfs = {}
for grade, year in itertools.product(grades, years):
    url = f"https://inscripcions.cangur.org/cangur/{year}/puntuacions/c{prefix(grade)}/{grade}/"
    try:
        dfs[(grade, year)] = pd.read_html(url)[0].sort_index(axis=1)
    except Exception:
        print(f"Failed to fetch data for grade {grade} and year {year} using url: {url}")
results = pd.concat(
    dfs,
    names=["Grade", "Year"],
).reset_index(level=2, drop=True)

results.to_csv("results.csv.gz")
