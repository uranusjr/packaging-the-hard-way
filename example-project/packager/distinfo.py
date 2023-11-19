import argparse
import base64
import csv
import email.message
import hashlib
import pathlib
import tempfile


def create_dist_info_dir(container, name, version):
    dist_info = container.joinpath(f"{name}-{version}.dist-info")
    dist_info.mkdir()
    return dist_info


def write_metadata(dist_info, name, version):
    m = email.message.EmailMessage()  # RFC 822.
    m["Metadata-Version"] = "2.1"
    m["Name"] = name
    m["Version"] = version
    dist_info.joinpath("METADATA").write_bytes(bytes(m))


def _record_row_from_path(path, relative):
    file_data = path.read_bytes()
    file_hash = base64.urlsafe_b64encode(hashlib.sha256(file_data).digest()).decode().rstrip('=')
    return [relative.as_posix(), f"sha256={file_hash}", str(len(file_data))]


def iter_files(roots):
    for root in roots:
        for path in root.glob("**/*"):
            if not path.is_file():
                continue
            if path.suffix == ".pyc" or path.parent.name == "__pycache__":
                continue
            yield path, path.relative_to(root.parent)


def write_record(dist_info, package):
    with dist_info.joinpath("RECORD").open("w") as f:
        w = csv.writer(f, lineterminator="\n")
        for path, relative in iter_files((package, dist_info)):
            w.writerow(_record_row_from_path(path, relative))
        w.writerow([f"{dist_info.name}/RECORD", "", ""])


def write_installer(dist_info):
    installer = dist_info.joinpath("INSTALLER")
    installer.write_text("home-grown-packager/distinfo.py")


def _parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=pathlib.Path)
    return parser.parse_args(argv)


_NAME = "my_package"

_VERSION = "0"

_PACKAGE = pathlib.Path("my_package")


def main(argv=None):
    options = _parse_args(argv)

    with tempfile.TemporaryDirectory() as td:
        dist_info = create_dist_info_dir(pathlib.Path(td), _NAME, _VERSION)
        write_metadata(dist_info, _NAME, _VERSION)
        write_installer(dist_info)
        write_record(dist_info, _PACKAGE)

        for path, relative in iter_files((_PACKAGE, dist_info)):
            target = options.target.joinpath(relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(path.read_bytes())


if __name__ == "__main__":
    main()
