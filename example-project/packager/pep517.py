import pathlib
import tempfile

from .wheel import create_dist_info, create_wheel


_NAME = "my_package"

_VERSION = "2"

_TAG = "py3-none-any"

_PACKAGE = pathlib.Path("my_package")


def build_wheel(
    wheel_directory,
    config_settings=None,
    metadata_directory=None,
):
    with tempfile.TemporaryDirectory() as td:
        if metadata_directory is None:
            td_path = pathlib.Path(td)
            dist_info = create_dist_info(
                _NAME,
                _VERSION,
                _TAG,
                _PACKAGE,
                td_path,
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
