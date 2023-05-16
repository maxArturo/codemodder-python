from pathlib import Path


DEFAULT_INCLUDE = ["*.py"]


def match_files(parent_path, exclude_paths=None, include_paths=None):
    """
    Find pattern-matching files starting at the parent_path, recursively.

    :param parent_path: str name for starting directory
    :param exclude_paths: comma-separated set of UNIX glob patterns to exclude
    :param include_paths: comma-separated set of UNIX glob patterns to exclude

    :return: list of <pathlib.PosixPath> files found within (including recursively) the parent directory
    that match the criteria of both exclude and include patterns.
    """
    exclude_patterns = exclude_paths.split(",") if exclude_paths else ""
    # _ = include_paths.split(",") if include_paths else ""

    matching_files = []
    for file_path in Path(parent_path).rglob(DEFAULT_INCLUDE[0]):
        # Exclude patterns take precedence over include patterns.
        if any([file_path.match(exclude) for exclude in exclude_patterns]):
            # if a file matches any excluded pattern, do not include it
            continue

        # For now we can implement include paths without any additional code.
        matching_files.append(file_path)
    return matching_files
