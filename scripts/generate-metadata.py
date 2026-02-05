#!/usr/bin/env python3
"""
Generate lightweight metadata files from full NCDU JSON reports.
These metadata files contain only essential information for quick page load.
"""

import json
import sys
from pathlib import Path


def extract_entry_info(entry, max_depth=1, current_depth=0):
    """Extract essential information from an NCDU entry, limiting depth."""
    if not isinstance(entry, list) or len(entry) < 2:
        return None

    size = entry[0]
    name = entry[1]

    result = [size, name]

    # Include children only up to max_depth
    if current_depth < max_depth and len(entry) > 2:
        # Indicate that children exist but don't include full data
        result.append({"has_children": True, "child_count": len(entry) - 2})

    return result


def get_entry_size(entry):
    """Calculate total size of an NCDU entry.

    In NCDU format, directory metadata contains only the inode size.
    We need to recursively sum all children to get the total size.
    """
    if isinstance(entry, dict):
        # File entry: just return asize + dsize
        return entry.get('asize', 0) + entry.get('dsize', 0)
    elif isinstance(entry, list) and len(entry) >= 1:
        # Entry is [metadata, children...]
        total_size = 0
        if isinstance(entry[0], dict):
            # Add the directory/file's own size (inode)
            total_size += entry[0].get('asize', 0) + entry[0].get('dsize', 0)

        # Recursively add all children's sizes
        for i in range(1, len(entry)):
            child = entry[i]
            total_size += get_entry_size(child)

        return total_size
    return 0


def generate_metadata(input_file, output_file, top_entries=20):
    """Generate metadata file with lightweight summary."""
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Extract metadata
    metadata = {
        "architecture": data.get("architecture"),
        "timestamp": data.get("timestamp"),
        "runner": data.get("runner"),
        "total_disk_size": data.get("total_disk_size"),
        "available_space": data.get("available_space"),
    }

    # Parse NCDU data structure: [version, timestamp, metadata, root_entry, ...children]
    ncdu_data = data.get("data", [])
    if len(ncdu_data) > 3:
        # ncdu_data[3] is the root directory entry (list with metadata and children)
        root_entry = ncdu_data[3]

        if isinstance(root_entry, list) and len(root_entry) > 0:
            # First element is metadata dict with name, asize, dsize
            root_meta = root_entry[0]
            if isinstance(root_meta, dict):
                # Calculate total from all children
                total_size = get_entry_size(root_entry)
                metadata["total_size"] = total_size

            # Get top N child entries (starting from index 1)
            top_level_entries = []
            count = 0
            for i in range(1, min(len(root_entry), top_entries + 1)):
                entry = root_entry[i]

                if isinstance(entry, list) and len(entry) > 0:
                    # Entry is [metadata, ...children]
                    entry_meta = entry[0]
                    if isinstance(entry_meta, dict):
                        name = entry_meta.get('name', 'unknown')
                        size = get_entry_size(entry)
                        has_children = len(entry) > 1
                        top_level_entries.append([size, name, has_children])
                        count += 1
                elif isinstance(entry, dict):
                    # Entry is just metadata (file, not directory)
                    name = entry.get('name', 'unknown')
                    size = entry.get('asize', 0) + entry.get('dsize', 0)
                    top_level_entries.append([size, name, False])
                    count += 1

            metadata["top_entries"] = top_level_entries
            metadata["total_entries"] = len(root_entry) - 1  # -1 for metadata

    # Write metadata file
    with open(output_file, 'w') as f:
        json.dump(metadata, f, separators=(',', ':'))

    print(f"Generated {output_file}")

    # Print size comparison
    input_size = Path(input_file).stat().st_size
    output_size = Path(output_file).stat().st_size
    reduction = (1 - output_size / input_size) * 100
    print(f"  Size: {input_size:,} → {output_size:,} bytes ({reduction:.1f}% reduction)")


def main():
    """Process all JSON files in docs/data directory."""
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    data_dir = repo_root / "docs" / "data"

    if not data_dir.exists():
        print(f"Error: Data directory not found: {data_dir}")
        sys.exit(1)

    json_files = list(data_dir.glob("*.json"))
    metadata_files = [f for f in json_files if not f.name.endswith("-metadata.json")]

    if not metadata_files:
        print("No JSON files found to process")
        sys.exit(1)

    for json_file in metadata_files:
        output_file = json_file.parent / f"{json_file.stem}-metadata.json"
        try:
            generate_metadata(json_file, output_file)
        except Exception as e:
            print(f"Error processing {json_file}: {e}", file=sys.stderr)
            sys.exit(1)

    print(f"\nSuccessfully generated {len(metadata_files)} metadata files")


if __name__ == "__main__":
    main()
