# TODO: Place your code here
from os import remove, sep, walk
from os.path import basename, getsize, join, normpath


def delete_dir_report(report_file_path: str = "dir-report.txt") -> None:
    remove("dir-report.txt")


def print_dir_report(report_file_path: str = "dir-report.txt") -> None:
    with open(report_file_path, "r") as f:
        print(f.read())


def get_path_depth(path):
    path = normpath(path)
    return len(path.split(sep))


def show_dirs(path, report):
    parent = path["parent"]
    path_name = path["name"]
    spaces = path["spaces"]
    depth = path["depth"]
    parent_depth = get_path_depth(parent)
    indent = spaces * (parent_depth - depth - 1)
    if parent == path_name:
        report.write(f"+ {basename(parent)}\n")
    else:
        report.write(f"{indent}|-+ {basename(parent)}\n")


def show_dirs_and_file_count(path, report):
    files = path["files"]
    parent = path["parent"]
    path_name = path["name"]
    spaces = path["spaces"]
    parent_depth = get_path_depth(parent)
    depth = path["depth"]
    file_count = f"({len(list(files))} files)"
    indent = spaces * (parent_depth - depth - 1)
    if parent == path_name:
        report.write(f"+ {basename(parent)} {file_count}\n")
    else:
        report.write(f"{indent}|-+ {basename(parent)} {file_count}\n")


def file_name_matches_highlight(file_name, highlight):
    if file_name.split(".")[1] == highlight:
        return True
    else:
        return False


def show_file_list(path, report):
    files = path["files"]
    parent = path["parent"]
    spaces = path["spaces"]
    parent_depth = get_path_depth(parent)
    depth = path["depth"]
    highlight = path["highlight"]
    indent = spaces * (parent_depth - depth)
    for f in sorted(files):
        if (highlight != None) and (file_name_matches_highlight(f, highlight)):
            report.write(f"{indent}|-- {basename(f)} <--\n")
        else:
            report.write(f"{indent}|-- {basename(f)}\n")


def show_file_list_and_file_sizes(path, report):
    files = path["files"]
    parent = path["parent"]
    spaces = path["spaces"]
    parent_depth = get_path_depth(parent)
    depth = path["depth"]
    parent_depth = get_path_depth(parent)
    indent = spaces * (parent_depth - depth)
    highlight = path["highlight"]
    for f in sorted(files):
        size = f"({getsize(join(parent, f))} bytes)"
        if (highlight != None) and (file_name_matches_highlight(f, highlight)):
            report.write(f"{indent}|-- {basename(f)} {size} <--\n")
        else:
            report.write(f"{indent}|-- {basename(f)} {size}\n")


def generate_dir_report(
    path: str = "data/dir-top",
    report_file_path: str = "dir-report.txt",
    show_files: bool = True,
    num_files: bool = False,
    file_size: bool = False,
    hl: str = None,
):
    depth = get_path_depth(path)
    level = -1
    with open(report_file_path, "w") as report:
        for parent, children, files in sorted(walk(path)):
            # create a dictionary containing:
            path = {
                "name": path,  # the main arg passed
                "depth": depth,  # depth of main arg passed
                "parent": parent,  # a folder within of the original arg passed
                "files": files,  # files within the folder
                "spaces": "  ",  # spaces
                "highlight": hl,  # what file to highlight
            }
            # show num files within a folder if "num_files" parameter is true
            if num_files:
                show_dirs_and_file_count(path, report)
            else:
                show_dirs(path, report)
            if file_size:
                show_file_list_and_file_sizes(path, report)
            elif show_files:
                show_file_list(path, report)
        level += 1


if __name__ == "__main__":
    generate_dir_report("data/dir-top", "dir-report.txt", file_size=True, hl="log")
    print_dir_report()
