import os
import sys
import glob
import logging
import subprocess
from pathlib import Path
from platform import system
import wheel.bdist_wheel as orig

try:
    from setuptools import setup, find_packages, Extension
    from setuptools.command.install import install
except ImportError:
    from distutils.core import setup, find_packages
    from distutils.command.install import install

# import CMakeBuild

# ---------- cmakebuild was integrated into setup.py directly --------------------------

try:
    from setuptools.command.build_ext import build_ext
except ImportError:
    from distutils.command.build_ext import build_ext

default_lib_dir = (
    "" if system() == "Windows" else os.path.join(os.getenv("HOME"), ".local")
)


def set_vcpkg_environment_variables():
    if not os.getenv("VCPKG_ROOT_DIR"):
        raise EnvironmentError("Environment variable 'VCPKG_ROOT_DIR' is undefined.")
    if not os.getenv("VCPKG_DEFAULT_TRIPLET"):
        raise EnvironmentError(
            "Environment variable 'VCPKG_DEFAULT_TRIPLET' is undefined."
        )
    if not os.getenv("VCPKG_FEATURE_FLAGS"):
        raise EnvironmentError(
            "Environment variable 'VCPKG_FEATURE_FLAGS' is undefined."
        )
    return (
        os.getenv("VCPKG_ROOT_DIR"),
        os.getenv("VCPKG_DEFAULT_TRIPLET"),
        os.getenv("VCPKG_FEATURE_FLAGS"),
    )


class CMakeBuild(build_ext):
    user_options = build_ext.user_options + [
        ("suitesparse-root=", None, "suitesparse source location"),
        ("sundials-root=", None, "sundials source location"),
    ]

    def initialize_options(self):
        build_ext.initialize_options(self)
        self.suitesparse_root = None
        self.sundials_root = None

    def finalize_options(self):
        build_ext.finalize_options(self)
        # Determine the calling command to get the
        # undefined options from.
        # If build_ext was called directly then this
        # doesn't matter.
        try:
            self.get_finalized_command("install", create=0)
            calling_cmd = "install"
        except AttributeError:
            calling_cmd = "bdist_wheel"
        self.set_undefined_options(
            calling_cmd,
            ("suitesparse_root", "suitesparse_root"),
            ("sundials_root", "sundials_root"),
        )
        if not self.suitesparse_root:
            self.suitesparse_root = os.path.join(default_lib_dir)
        if not self.sundials_root:
            self.sundials_root = os.path.join(default_lib_dir)

    def get_build_directory(self):
        # distutils outputs object files in directory self.build_temp
        # (typically build/temp.*). This is our CMake build directory.
        # On Windows, distutils is too smart and appends "Release" or
        # "Debug" to self.build_temp. So in this case we want the
        # build directory to be the parent directory.
        if system() == "Windows":
            return Path(self.build_temp).parents[0]
        return self.build_temp

    def run(self):
        if not self.extensions:
            return

        if system() == "Windows":
            use_python_casadi = False
        else:
            use_python_casadi = True

        build_type = os.getenv("PYBAMM_CPP_BUILD_TYPE", "RELEASE")
        cmake_args = [
            "-DCMAKE_BUILD_TYPE={}".format(build_type),
            "-DPYTHON_EXECUTABLE={}".format(sys.executable),
            "-DUSE_PYTHON_CASADI={}".format("TRUE" if use_python_casadi else "FALSE"),
        ]
        if self.suitesparse_root:
            cmake_args.append(
                "-DSuiteSparse_ROOT={}".format(os.path.abspath(self.suitesparse_root))
            )
        if self.sundials_root:
            cmake_args.append(
                "-DSUNDIALS_ROOT={}".format(os.path.abspath(self.sundials_root))
            )

        build_dir = self.get_build_directory()
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)

        # The CMakeError.log file is generated by cmake is the configure step
        # encounters error. In the following the existence of this file is used
        # to determine whether or not the cmake configure step went smoothly.
        # So must make sure this file does not remain from a previous failed build.
        if os.path.isfile(os.path.join(build_dir, "CMakeError.log")):
            os.remove(os.path.join(build_dir, "CMakeError.log"))

        build_env = os.environ
        if os.getenv("PYBAMM_USE_VCPKG"):
            (
                vcpkg_root_dir,
                vcpkg_default_triplet,
                vcpkg_feature_flags,
            ) = set_vcpkg_environment_variables()
            build_env["vcpkg_root_dir"] = vcpkg_root_dir
            build_env["vcpkg_default_triplet"] = vcpkg_default_triplet
            build_env["vcpkg_feature_flags"] = vcpkg_feature_flags

        cmake_list_dir = os.path.abspath(os.path.dirname(__file__))
        print("-" * 10, "Running CMake for idaklu solver", "-" * 40)
        subprocess.run(
            ["cmake", cmake_list_dir] + cmake_args, cwd=build_dir, env=build_env
        )

        if os.path.isfile(os.path.join(build_dir, "CMakeError.log")):
            msg = (
                "cmake configuration steps encountered errors, and the idaklu module"
                " could not be built. Make sure dependencies are correctly "
                "installed. See "
                "https://docs.pybamm.org/en/latest/source/user_guide/installation/install-from-source.html" # noqa: E501
            )
            raise RuntimeError(msg)
        else:
            print("-" * 10, "Building idaklu module", "-" * 40)
            subprocess.run(
                ["cmake", "--build", ".", "--config", "Release"],
                cwd=build_dir,
                env=build_env,
            )

            # Move from build temp to final position
            for ext in self.extensions:
                self.move_output(ext)

    def move_output(self, ext):
        # Copy built module to dist/ directory
        build_temp = Path(self.build_temp).resolve()
        # Get destination location
        # self.get_ext_fullpath(ext.name) -->
        # build/lib.linux-x86_64-3.5/idaklu.cpython-37m-x86_64-linux-gnu.so
        # using resolve() with python < 3.6 will result in a FileNotFoundError
        # since the location does not yet exists.
        dest_path = Path(self.get_ext_fullpath(ext.name)).resolve()
        source_path = build_temp / os.path.basename(self.get_ext_filename(ext.name))
        dest_directory = dest_path.parents[0]
        dest_directory.mkdir(parents=True, exist_ok=True)
        self.copy_file(source_path, dest_path)

# ---------- end of cmakebuild steps ---------------------------------------------------

# default_lib_dir = (
#     "" if system() == "Windows" else os.path.join(os.getenv("HOME"), ".local")
# )

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logger = logging.getLogger("PyBaMM setup")

# To override the default severity of logging
logger.setLevel("INFO")

# Use FileHandler() to log to a file
logfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "setup.log")
file_handler = logging.FileHandler(logfile)
formatter = logging.Formatter(log_format)
file_handler.setFormatter(formatter)

# Add the file handler
logger.addHandler(file_handler)
logger.info("Starting PyBaMM setup")


class CustomInstall(install):
    """A custom install command to add 2 build options"""

    user_options = install.user_options + [
        ("suitesparse-root=", None, "suitesparse source location"),
        ("sundials-root=", None, "sundials source location"),
    ]

    def initialize_options(self):
        install.initialize_options(self)
        self.suitesparse_root = None
        self.sundials_root = None

    def finalize_options(self):
        install.finalize_options(self)
        if not self.suitesparse_root:
            self.suitesparse_root = default_lib_dir
        if not self.sundials_root:
            self.sundials_root = default_lib_dir

    def run(self):
        install.run(self)


class bdist_wheel(orig.bdist_wheel):
    """A custom install command to add 2 build options"""

    user_options = orig.bdist_wheel.user_options + [
        ("suitesparse-root=", None, "suitesparse source location"),
        ("sundials-root=", None, "sundials source location"),
    ]

    def initialize_options(self):
        orig.bdist_wheel.initialize_options(self)
        self.suitesparse_root = None
        self.sundials_root = None

    def finalize_options(self):
        orig.bdist_wheel.finalize_options(self)
        if not self.suitesparse_root:
            self.suitesparse_root = default_lib_dir
        if not self.sundials_root:
            self.sundials_root = default_lib_dir

    def run(self):
        orig.bdist_wheel.run(self)


def compile_KLU():
    # Return whether or not the KLU extension should be compiled.
    # Return True if:
    # - Not running on Windows AND
    # - CMake is found AND
    # - The pybind11 and casadi-headers directories are found
    #   in the PyBaMM project directory
    CMakeFound = True
    PyBind11Found = True
    windows = (not system()) or system() == "Windows"

    msg = "Running on Windows" if windows else "Not running on windows"
    logger.info(msg)

    try:
        subprocess.run(["cmake", "--version"])
        logger.info("Found CMake.")
    except OSError:
        CMakeFound = False
        logger.info("Could not find CMake. Skipping compilation of KLU module.")

    pybamm_project_dir = os.path.dirname(os.path.abspath(__file__))
    pybind11_dir = os.path.join(pybamm_project_dir, "pybind11")
    try:
        open(os.path.join(pybind11_dir, "tools", "pybind11Tools.cmake"))
        logger.info("Found pybind11 directory ({})".format(pybind11_dir))
    except FileNotFoundError:
        PyBind11Found = False
        msg = (
            "Could not find PyBind11 directory ({})."
            " Skipping compilation of KLU module.".format(pybind11_dir)
        )
        logger.info(msg)

    return CMakeFound and PyBind11Found


# Build the list of package data files to be included in the PyBaMM package.
# These are mainly the parameter files located in the input/parameters/ subdirectories.
# TODO: might be possible to include in pyproject.toml with data configuration values
pybamm_data = []
for file_ext in ["*.csv", "*.py", "*.md", "*.txt"]:
    # Get all the files ending in file_ext in pybamm/input dir.
    # list_of_files = [
    #    'pybamm/input/drive_cycles/car_current.csv',
    #    'pybamm/input/drive_cycles/US06.csv',
    # ...
    list_of_files = glob.glob("pybamm/input/**/" + file_ext, recursive=True)

    # Add these files to pybamm_data.
    # The path must be relative to the package dir (pybamm/), so
    # must process the content of list_of_files to take out the top
    # pybamm/ dir, i.e.:
    # ['input/drive_cycles/car_current.csv',
    #  'input/drive_cycles/US06.csv',
    # ...
    pybamm_data.extend(
        [os.path.join(*Path(filename).parts[1:]) for filename in list_of_files]
    )
pybamm_data.append("./CITATIONS.bib")
pybamm_data.append("./plotting/pybamm.mplstyle")
pybamm_data.append("../CMakeBuild.py")

idaklu_ext = Extension(
    name="pybamm.solvers.idaklu",
    sources=[
        "pybamm/solvers/c_solvers/idaklu.cpp"
        "pybamm/solvers/c_solvers/idaklu.hpp"
        "pybamm/solvers/c_solvers/idaklu_casadi.cpp"
        "pybamm/solvers/c_solvers/idaklu_casadi.hpp"
        "pybamm/solvers/c_solvers/idaklu_python.cpp"
        "pybamm/solvers/c_solvers/idaklu_python.hpp"
        "pybamm/solvers/c_solvers/solution.cpp"
        "pybamm/solvers/c_solvers/solution.hpp"
    ],
)
ext_modules = [idaklu_ext] if compile_KLU() else []

# Defines __version__
# TODO: might not be needed anymore, because we define it in pyproject.toml
# and can therefore access it with importlib.metadata.version("pybamm") (python 3.8+)
# The version.py file can then be imported with attr: pybamm.__version__ dynamically
root = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(root, "pybamm", "version.py")) as f:
    exec(f.read())

# Load text for description and license
# TODO: might not be needed anymore, because we define the description and license
# in pyproject.toml
# TODO: add long description there and remove it from setup()
with open("README.md", encoding="utf-8") as f:
    readme = f.read()

# Project metadata was moved to pyproject.toml (which is read by pip).
# However, custom build commands and setuptools extension modules are still defined here
setup(
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/pybamm-team/PyBaMM",
    packages=find_packages(include=("pybamm", "pybamm.*")),
    ext_modules=ext_modules,
    cmdclass={
        "build_ext": CMakeBuild,
        "bdist_wheel": bdist_wheel,
        "install": CustomInstall,
    },
    package_data={"pybamm": pybamm_data},
)
