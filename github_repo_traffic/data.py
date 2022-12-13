from datetime import datetime, timedelta
import os
from pathlib import Path

import asciichartpy
from dotenv import load_dotenv
from github import Github
from pandas import DataFrame, read_csv, Timestamp


NUM_DAYS = 90


def get_kpi(path: Path, kpi: str):
    repo = Github(os.getenv("TRAFFIC_ACTION_TOKEN")).get_repo(os.getenv("GITHUB_REPOSITORY"))
    data = getattr(repo, f"get_{kpi}_traffic")()

    counts = {value.timestamp: {f"total_{kpi}": value.count, f"unique_{kpi}": value.uniques} for value in data[kpi]}

    if path.exists():
        old_counts = read_csv(path, index_col="date", parse_dates=["date"]).to_dict(orient="index")
        old_counts.update(counts)
        counts = old_counts

    if counts:
        start_date, end_date = min(counts.keys()), max(*counts.keys(), Timestamp.now())
        for i in range((end_date - start_date).days + 1):
            day = start_date + timedelta(days=i)
            if day not in counts:
                counts[day] = {f"total_{kpi}": 0, f"unique_{kpi}": 0}

    dataframe = DataFrame.from_dict(data=counts, orient="index", columns=[f"total_{kpi}", f"unique_{kpi}"])
    dataframe.index.name = "date"
    dataframe.sort_index(inplace=True)
    dataframe.to_csv(path)
    return dataframe


def get_views(path: Path):
    return get_kpi(path, "views")


def get_clones(path: Path):
    return get_kpi(path, "clones")


def get_kpi_plot(data: DataFrame, kpi: str):
    kpis = data[f"total_{kpi}"].to_list()
    kpis = kpis if len(kpis) < NUM_DAYS else kpis[-NUM_DAYS:]

    chart = f"""
        Total {kpi.title()} per Day from {data.index[-1].date() - timedelta(days=len(kpis) - 1)} to {data.index[-1].date()}

        Repository Views
{asciichartpy.plot(kpis, {"height": 15, "format": "{:8.0f}"})}

        Chart last updated - {datetime.utcnow().strftime("%c")} UTC
        """
    return chart


def get_views_plot(data: DataFrame):
    return get_kpi_plot(data, "views")


def get_clones_plot(data: DataFrame):
    return get_kpi_plot(data, "clones")


def main():
    load_dotenv(Path.cwd() / ".env")
    workplace_path = Path(os.getenv("GITHUB_WORKSPACE")).resolve() / os.getenv("TRAFFIC_DIR")

    workplace_path.mkdir(exist_ok=True)

    views_frame = get_views(workplace_path / "views.csv")
    clone_frame = get_clones(workplace_path / "clones.csv")

    if not views_frame.empty:
        with open(workplace_path / "views_chart.txt", "w", encoding="utf-8") as views_chart:
            views_chart.write(get_views_plot(views_frame))

    if not clone_frame.empty:
        with open(workplace_path / "clones_chart.txt", "w", encoding="utf-8") as clones_chart:
            clones_chart.write(get_clones_plot(clone_frame))


if __name__ == "__main__":
    main()
