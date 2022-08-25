import os
from pathlib import Path

from dotenv import load_dotenv


def main():
    load_dotenv()
    workplace_path = Path(os.getenv("GITHUB_WORKSPACE")).resolve() / ".traffic"
    github_path = Path(os.getenv("GITHUB_WORKSPACE")).resolve() / ".github"

    readme_path = next((path for path in github_path.iterdir() if path.stem.startswith("TEMPLATE_README")), None)

    if readme_path is None:
        raise Exception("Error: A README template must be present in the base of the .github directory")

    with open(readme_path, encoding="utf-8") as readme_template:
        readme_template = readme_template.read()

    with open(workplace_path / "views_chart.txt", encoding="utf-8") as views_chart:
        views_chart = views_chart.read()

    with open(workplace_path / "clones_chart.txt", encoding="utf-8") as clones_chart:
        clones_chart = clones_chart.read()

    readme = readme_template.format(VIEWS_CHART=views_chart, CLONES_CHART=clones_chart)

    readme_name = readme_path.name.replace("TEMPLATE_", "")

    with open(Path(os.getenv("GITHUB_WORKSPACE")).resolve() / readme_name, "w", encoding="utf-8") as readme_file:
        readme_file.write(readme)


if __name__ == "__main__":
    main()
