# Git LFS Setup for JSON Files

This repository has been configured to use Git LFS (Large File Storage) for JSON files in the `docs/data/` directory.

## What Has Been Configured

1. **`.gitattributes` file**: Created to track `docs/data/*.json` files with Git LFS
2. **Git LFS initialization**: Git LFS has been initialized in the local repository
3. **JSON files migration**: All existing JSON files in `docs/data/` have been converted to Git LFS pointers

## Current Status

The configuration is complete locally, but **Git LFS is currently disabled on the GitHub repository**. This prevents pushing the LFS objects to GitHub.

## Required Action: Enable Git LFS on GitHub

To complete the setup, a repository administrator needs to enable Git LFS:

### Option 1: Enable via GitHub Web Interface (Recommended)

1. Go to the repository on GitHub: `https://github.com/fbnrst/Github-Self-Hosted-Runners-Disk-Space`
2. Click on **Settings** (you must be a repository admin)
3. In the left sidebar, click on **Data Services**
4. Under **Git LFS**, toggle the switch to **Enable Git LFS**
5. Confirm the action

### Option 2: Enable via GitHub CLI

```bash
# Note: This requires the gh CLI tool and appropriate permissions
gh api repos/fbnrst/Github-Self-Hosted-Runners-Disk-Space \
  -X PATCH \
  -f has_downloads=true
```

### Option 3: Contact GitHub Support

If Git LFS cannot be enabled through the settings, contact GitHub support to enable it for the repository.

## After Enabling Git LFS

Once Git LFS is enabled on GitHub, you can push the changes:

```bash
git push origin copilot/use-git-lfs-for-json-files
```

The JSON files will be stored in Git LFS, which:
- Keeps the repository size small
- Improves clone and fetch performance
- Handles large files efficiently

## Verifying Git LFS

After pushing, you can verify Git LFS is working:

```bash
# Check which files are tracked by Git LFS
git lfs ls-files

# Expected output:
# 2006208209 * docs/data/aarch64-22.04.json
# bd2c8363ee * docs/data/aarch64.json
# a6387d952f * docs/data/x86_64-22.04.json
# e7f1a5824c * docs/data/x86_64-slim.json
# 37ac45cb0d * docs/data/x86_64.json
```

## Benefits of Git LFS for JSON Files

The JSON files in this repository range from 8.3MB to 73MB (total ~200MB), which makes them ideal candidates for Git LFS:

- **Reduced repository size**: Only LFS pointers are stored in git history
- **Faster cloning**: LFS files are downloaded on-demand
- **Better workflow performance**: Git operations are faster with smaller repositories
- **Efficient storage**: Large files are deduplicated and stored efficiently

## Troubleshooting

If you encounter issues after enabling Git LFS:

1. **Ensure Git LFS is installed locally**:
   ```bash
   git lfs version
   ```

2. **Re-initialize Git LFS if needed**:
   ```bash
   git lfs install
   ```

3. **Check Git LFS status**:
   ```bash
   git lfs status
   ```

4. **Force push if necessary** (only if this is a feature branch):
   ```bash
   git push --force origin copilot/use-git-lfs-for-json-files
   ```
