import tarfile
import pathlib
import tempfile

from .distinfo import iter_files
from .wheel import create_dist_info, create_wheel


_NAME = "my_package"

_VERSION = "2"

_TAG = "py3-none-any"

_PACKAGE = pathlib.Path("my_package")


def build_wheel(
    wheel_directory, config_settings=None, metadata_directory=None,
):
    with tempfile.TemporaryDirectory() as td:
        if metadata_directory is None:
            td_path = pathlib.Path(td)
            dist_info = create_dist_info(
                _NAME, _VERSION, _TAG, _PACKAGE, td_path,
            )
        else:
            dist_info = pathlib.Path(metadata_directory)

        wheel_path = create_wheel(
            _NAME,
            _VERSION,
            _TAG,
            _PACKAGE,
            dist_info,
            pathlib.Path(wheel_directory),
        )

    return wheel_path.name


def build_sdist(sdist_directory, config_settings=None):
    packager = pathlib.Path(__file__).resolve().parent
    sdist_path = pathlib.Path(sdist_directory, f"{_NAME}-{_VERSION}.tar.gz")
    with tarfile.open(sdist_path, "w:gz", format=tarfile.PAX_FORMAT) as tf:
        for path, relative in iter_files((_PACKAGE, packager)):
            tf.add(path, relative.as_posix())
        tf.add("pyproject.toml")
    return sdist_path.name
