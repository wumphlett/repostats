# Repository Traffic

This Github action can be used to store traffic data beyond the two-week period currently supported.
It uses the Github API to pull down the traffic data and stores it into a configurable directory and commits it to your 
repository. In addition, ascii charts are generated and can be automatically inserted into your README to display traffic.

# Usage
## Permissions
1. Create a personal access token (PAT) with repo permissions
2. Store it in your repository secrets with the key `TRAFFIC_ACTION_TOKEN`

## Workflow
Create a `workflow.yml` file in your `.github/workflows` directory. An example is provided.

```yaml
name: Repository Traffic
on:
  push:
    branches:
      - main
  schedule:
    - cron: "55 23 * * *"
  workflow_dispatch:

jobs:
  traffic:
    runs-on: ubuntu-latest
    steps:
      - name: Repository Traffic
        uses: wumphlett/repostats@v1.0.3
        with:
          format_readme: true
        env:
          TRAFFIC_ACTION_TOKEN: ${ secrets.TRAFFIC_ACTION_TOKEN }
```
The env directive with the `TRAFFIC_ACTION_TOKEN` is required. Any variables defined in with are optional.

## Configuration
Three values can be configured in the with directive of the action.
```
format_readme (true/false) - control whether the action will format a template readme with traffic data (see below)
  default: false
commit_msg (str) - The commit message used when updating traffic data
  default: "Updating repository traffic"
traffic_dir (str) - The directory used to store and update traffic data
  default: ".traffic"
```

## README Formatting
Optionally, you can use this action to format your readme with traffic data. This works best if you schedule this action
daily.

1. Create a TEMPLATE_README.<any type> file in your `.github` directory
2. Include either {VIEWS_CHART} or {CLONES_CHART} in your template file
   1. Note: its recommended that you wrap your formatting directive in triple backticks to preserve spacing
3. Enable `format_readme` in your `workflow.yml` file
4. Trigger the action to format your readme which will automatically commit the changes
   1. Note, all changes that you want to make to your readme must now be made to the template instead of the readme in the root of the repo

```

    Total Views per Day from 2022-08-25 to 2022-08-25

    Repository Views
    3.00  ┼

    Chart last updated - Thu Aug 25 08:26:39 2022 UTC
    
```
