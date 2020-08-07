import argparse
import email.message
import pathlib
import tempfile
import zipfile

from distinfo import (
    copy_directory,
    create_dist_info,
    write_metadata,
    write_record,
)


def _parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=pathlib.Path)
    parser.add_argument("output", type=pathlib.Path)
    return parser.parse_args(argv)


def _write_wheel_metadata(dist_info, tag):
    m = email.message.EmailMessage()
    m["Wheel-Version"] = "1.0"
    m["Generator"] = "home-grown-packager/wheel.py"
    m["Root-Is-Purelib"] = "true"
    m["Tag"] = tag
    dist_info.joinpath("WHEEL").write_bytes(bytes(m))


def _create_zip(directory, target):
    with zipfile.ZipFile(target, "w") as zf:
        for path in directory.glob("**/*"):
            zf.write(path, path.relative_to(directory).as_posix())


_NAME = "my_package"

_VERSION = "1"

_TAG = "py3-none-any"


def main(argv=None):
    options = _parse_args(argv)

    options.output.mkdir(parents=True, exist_ok=True)
    wheel_name = f"{_NAME}-{_VERSION}-{_TAG}.whl"

    with tempfile.TemporaryDirectory() as td:
        copy_directory(options.package, pathlib.Path(td))
        dist_info = create_dist_info(pathlib.Path(td), _NAME, _VERSION)
        write_metadata(dist_info, _NAME, _VERSION)
        _write_wheel_metadata(dist_info, _TAG)
        write_record(dist_info, options.package)
        _create_zip(td, options.output.joinpath(wheel_name))


if __name__ == "__main__":
    main()
