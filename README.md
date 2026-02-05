# GitHub Self-Hosted Runners Disk Space

This repository provides automated weekly disk space analysis for GitHub Actions runners on different architectures (x86_64 and aarch64).

## Features

- 🔄 **Automated Weekly Reports**: GitHub Actions workflow runs every Monday at 00:00 UTC
- 📊 **Multi-Architecture Support**: Collects data from both x86_64 and aarch64 runners
- 🌐 **Interactive Web Interface**: Beautiful GitHub Pages site to visualize disk usage
- 📈 **Tree View**: Browse disk usage in an interactive tree structure
- 🎯 **Summary Statistics**: Quick overview of total and average disk usage

## How It Works

1. **Data Collection**: The `collect-disk-space.yml` workflow uses `ncdu` (NCurses Disk Usage) to scan the filesystem on both x86_64 and aarch64 runners
2. **Data Storage**: Results are exported to JSON format with metadata (timestamp, architecture, runner type) and committed to the repository
3. **Page Deployment**: The `deploy-pages.yml` workflow automatically deploys updates to GitHub Pages when changes are made to the `docs/` directory
4. **Visualization**: An interactive HTML page displays the data with expandable tree views

## Workflows

### Data Collection Workflow

The data collection workflow (`collect-disk-space.yml`) runs weekly to gather disk usage information:
- **Schedule**: Every Monday at 00:00 UTC
- **Trigger**: Can also be manually triggered via `workflow_dispatch`
- **Process**: 
  1. Runs ncdu on x86_64 and aarch64 runners in parallel
  2. Generates JSON reports with metadata
  3. Commits reports to `docs/data/` directory

### Pages Deployment Workflow

The pages deployment workflow (`deploy-pages.yml`) runs independently:
- **Trigger**: Automatically on push to `docs/` directory
- **Trigger**: Can also be manually triggered via `workflow_dispatch`
- **Process**: Deploys the `docs/` directory to GitHub Pages

This separation allows you to:
- Update page layouts without re-running expensive ncdu scans
- Collect data on a scheduled basis without triggering deployments
- Deploy page updates quickly and independently

## Viewing the Reports

Visit the GitHub Pages site to see the latest disk space reports:
- https://fbnrst.github.io/Github-Self-Hosted-Runners-Disk-Space/

## Manual Workflow Trigger

You can manually trigger the workflows from the Actions tab:

### Data Collection
1. Go to the "Actions" tab
2. Select "Collect Disk Space Data" workflow
3. Click "Run workflow"

### Pages Deployment
1. Go to the "Actions" tab
2. Select "Deploy GitHub Pages" workflow
3. Click "Run workflow"

## Workflow Schedule

The data collection workflow runs automatically:
- **Schedule**: Every Monday at 00:00 UTC
- **Trigger**: Can also be manually triggered via `workflow_dispatch`

The pages deployment workflow runs automatically:
- **Trigger**: On push to `docs/` directory (e.g., when data is updated or layout changes)
- **Trigger**: Can also be manually triggered via `workflow_dispatch`

## Technical Details

- **Tool**: ncdu (NCurses Disk Usage) v1.15+
- **Format**: JSON export format
- **Runners**:
  - x86_64: `ubuntu-latest`
  - aarch64: `ubuntu-latest-arm64`

## Development

### Pre-commit Hooks

This repository uses pre-commit hooks to maintain code quality. To set up:

```bash
pip install pre-commit
pre-commit install
```

The hooks will automatically check:
- Trailing whitespace
- End of file fixers
- YAML syntax validation
- JSON syntax validation
- Large file detection
- Merge conflict markers

## Repository Structure

```
.
├── .github/
│   └── workflows/
│       ├── collect-disk-space.yml    # Data collection workflow (weekly)
│       └── deploy-pages.yml          # GitHub Pages deployment workflow
├── .pre-commit-config.yaml           # Pre-commit hooks configuration
├── docs/
│   ├── index.html                     # GitHub Pages viewer
│   └── data/                          # Generated disk space reports
│       ├── x86_64.json
│       └── aarch64.json
└── README.md
```

## License

This project is open source and available under the MIT License.
