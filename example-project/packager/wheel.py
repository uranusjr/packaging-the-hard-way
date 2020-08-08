import argparse
import email.message
import pathlib
import tempfile
import zipfile

from .distinfo import (
    create_dist_info_dir,
    iter_files,
    write_metadata,
    write_record,
)


def _write_wheel_metadata(dist_info, tag):
    m = email.message.EmailMessage()
    m["Wheel-Version"] = "1.0"
    m["Generator"] = "home-grown-packager/wheel.py"
    m["Root-Is-Purelib"] = "true"
    m["Tag"] = tag
    dist_info.joinpath("WHEEL").write_bytes(bytes(m))


def create_dist_info(name, version, tag, package, output_dir):
    dist_info = create_dist_info_dir(output_dir, name, version)
    write_metadata(dist_info, name, version)
    _write_wheel_metadata(dist_info, tag)
    write_record(dist_info, package)
    return dist_info


def create_wheel(name, version, tag, package, dist_info, output_dir):
    wheel_path = output_dir.joinpath(f"{name}-{version}-{tag}.whl")
    with zipfile.ZipFile(wheel_path, "w") as zf:
        for path, relative in iter_files((package, dist_info)):
            zf.write(path, relative.as_posix())
    return wheel_path


def _parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=pathlib.Path)
    return parser.parse_args(argv)


_NAME = "my_package"

_VERSION = "1"

_TAG = "py3-none-any"

_PACKAGE = pathlib.Path("my_package")


def main(argv=None):
    options = _parse_args(argv)
    options.output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        td_path = pathlib.Path(td)
        dist_info = create_dist_info(_NAME, _VERSION, _TAG, _PACKAGE, td_path)
        create_wheel(
            _NAME, _VERSION, _TAG, _PACKAGE, dist_info, options.output,
        )


if __name__ == "__main__":
    main()
