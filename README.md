# GitHub Self-Hosted Runners Disk Space

This repository provides automated weekly disk space analysis for GitHub Actions runners on different architectures (x86_64 and aarch64).

## Features

- 🔄 **Automated Weekly Reports**: GitHub Actions workflow runs every Monday at 00:00 UTC
- 📊 **Multi-Architecture Support**: Collects data from both x86_64 and aarch64 runners
- 🌐 **Interactive Web Interface**: Beautiful GitHub Pages site to visualize disk usage
- 📈 **Tree View**: Browse disk usage in an interactive tree structure
- 🎯 **Summary Statistics**: Quick overview of total and average disk usage

## How It Works

1. **Data Collection**: The workflow uses `ncdu` (NCurses Disk Usage) to scan the filesystem on both x86_64 and aarch64 runners
2. **Data Processing**: Results are exported to JSON format with metadata (timestamp, architecture, runner type)
3. **Publishing**: Reports are automatically published to GitHub Pages
4. **Visualization**: An interactive HTML page displays the data with expandable tree views

## Viewing the Reports

Visit the GitHub Pages site to see the latest disk space reports:
- https://fbnrst.github.io/Github-Self-Hosted-Runners-Disk-Space/

## Manual Workflow Trigger

You can manually trigger the workflow from the Actions tab:
1. Go to the "Actions" tab
2. Select "Disk Space Overview" workflow
3. Click "Run workflow"

## Workflow Schedule

The workflow runs automatically:
- **Schedule**: Every Monday at 00:00 UTC
- **Trigger**: Can also be manually triggered via `workflow_dispatch`

## Technical Details

- **Tool**: ncdu (NCurses Disk Usage) v1.15+
- **Format**: JSON export format
- **Exclusions**: `/proc`, `/sys`, `/dev`, `/run`, `/tmp` directories are excluded from scans
- **Runners**: 
  - x86_64: `ubuntu-latest`
  - aarch64: `ubuntu-latest-arm64`

## Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── disk-space-overview.yml  # GitHub Actions workflow
├── docs/
│   ├── index.html                    # GitHub Pages viewer
│   └── data/                         # Generated disk space reports
│       ├── x86_64.json
│       └── aarch64.json
└── README.md
```

## License

This project is open source and available under the MIT License.