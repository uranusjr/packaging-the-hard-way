import argparse
import csv
import email.message
import pathlib
import shutil
import tempfile


DIST_NAME = "my_package"

DIST_VERSION = "0"


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=pathlib.Path)
    parser.add_argument("target", type=pathlib.Path)
    return parser.parse_args()


def _write_metadata(dist_info):
    m = email.message.EmailMessage()
    m["Metadata-Version"] = "2.1"
    m["Name"] = DIST_NAME
    m["Version"] = DIST_VERSION
    dist_info.joinpath("METADATA").write_bytes(bytes(m))


def _write_record(dist_info, package):
    with dist_info.joinpath("RECORD").open("w") as f:
        w = csv.writer(f)
        for path in package.glob("**/*"):
            if not path.is_file():
                continue
            if path.suffix == ".pyc" or path.parent.name == "__pycache__":
                continue
            w.writerow([path.relative_to(package.parent), "", ""])


def _write_installer(dist_info):
    dist_info.joinpath("INSTALLER").write_text("direct-install")


def _create_dist_info(package, container):
    dist_info = container.joinpath(f"{DIST_NAME}-{DIST_VERSION}.dist-info")
    dist_info.mkdir()
    _write_metadata(dist_info)
    _write_record(dist_info, package)
    _write_installer(dist_info)
    return dist_info


def _install(directory, container):
    target = container.joinpath(directory.name)
    if target.is_dir():
        shutil.rmtree(target)
    shutil.copytree(directory, target)


def main():
    ns = _parse_args()
    with tempfile.TemporaryDirectory() as td:
        dist_info = _create_dist_info(ns.package, pathlib.Path(td))
        _install(ns.package, ns.target)
        _install(dist_info, ns.target)


if __name__ == "__main__":
    main()
