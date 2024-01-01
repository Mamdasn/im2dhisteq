import os
import platform


def get_dll_name():
    # Mapping of Python's platform strings to GOOS values
    goos_mapping = {"Linux": "linux", "Windows": "windows", "Darwin": "darwin"}
    dll_extension_mapping = {"linux": "so", "windows": "dll", "darwin": "dylib"}

    # Get the OS (similar to GOOS in Go)
    goos = goos_mapping.get(platform.system(), "unknown")

    # Get the architecture (similar to GOARCH in Go)
    arch = platform.machine()
    goarch = "unknown"
    if arch in ["x86_64", "AMD64"]:
        goarch = "amd64"
    elif arch == "i386":
        goarch = "386"
    elif "arm" in arch or "aarch64" in arch:
        goarch = "arm64" if "64" in arch else "arm"

    dll_name = f"lib-im2dhist-{goos}-{goarch}.{dll_extension_mapping[goos]}"

    return dll_name


def get_dll_in_sys_path(library_name):
    # Get the system PATH environment variable
    system_path = os.environ.get("PATH", "")

    # Split the PATH into individual directories
    directories = system_path.split(os.pathsep)

    # Check each directory for the existence of the library
    for directory in directories:
        library_path = os.path.join(directory, library_name)
        if os.path.exists(library_path):
            return library_path


def get_dll_path():
    dll_path = None
    dll_name = get_dll_name()
    if get_dll_in_sys_path(dll_name):
        dll_path = get_dll_in_sys_path(dll_name)
    else:
        file_path = os.path.realpath(__file__)
        src_dir = os.path.dirname(file_path)
        dll_dir = os.path.join(src_dir, "compiled-libs")
        dll_path = os.path.join(dll_dir, dll_name)

    if os.path.exists(dll_path):
        return dll_path
    return None
