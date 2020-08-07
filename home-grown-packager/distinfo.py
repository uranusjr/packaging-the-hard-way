import argparse
import base64
import csv
import email.message
import hashlib
import pathlib
import shutil
import tempfile


def create_dist_info(container, name, version):
    dist_info = container.joinpath(f"{name}-{version}.dist-info")
    dist_info.mkdir()
    return dist_info


def write_metadata(dist_info, name, version):
    m = email.message.EmailMessage()
    m["Metadata-Version"] = "2.1"
    m["Name"] = name
    m["Version"] = version
    dist_info.joinpath("METADATA").write_bytes(bytes(m))


def _record_row_from_path(path, root):
    file_path = path.relative_to(root.parent).as_posix()
    file_data = path.read_bytes()
    file_hash = base64.urlsafe_b64encode(hashlib.md5(file_data).digest())
    return [file_path, str(len(file_data)), f"md5={file_hash}"]


def write_record(dist_info, package):
    with dist_info.joinpath("RECORD").open("w") as f:
        w = csv.writer(f, lineterminator="\n")
        for root in (package, dist_info):
            for path in root.glob("**/*"):
                if not path.is_file():
                    continue
                if path.suffix == ".pyc" or path.parent.name == "__pycache__":
                    continue
                w.writerow(_record_row_from_path(path, root))
        w.writerow([f"{dist_info.name}/RECORD", "", ""])


def write_installer(dist_info):
    installer = dist_info.joinpath("INSTALLER")
    installer.write_text("home-grown-packager/distinfo.py")


def _parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=pathlib.Path)
    parser.add_argument("target", type=pathlib.Path)
    return parser.parse_args(argv)


def _ignore_pycache(directory, names):
    if pathlib.Path(directory).name == "__pycache__":
        return names
    return []


def copy_directory(directory, container):
    target = container.joinpath(directory.name)
    if target.is_dir():
        shutil.rmtree(target)
    shutil.copytree(directory, target, ignore=_ignore_pycache)


_NAME = "my_package"

_VERSION = "0"


def main(argv=None):
    options = _parse_args(argv)

    with tempfile.TemporaryDirectory() as td:
        dist_info = create_dist_info(pathlib.Path(td), _NAME, _VERSION,)
        write_metadata(dist_info, _NAME, _VERSION)
        write_installer(dist_info)
        write_record(dist_info, options.package)
        copy_directory(dist_info, options.target)
    copy_directory(options.package, options.target)


if __name__ == "__main__":
    main()
