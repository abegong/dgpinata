from setuptools import setup, find_packages


def read_requirements(file):
    with open(file, "r") as f:
        return [line.strip() for line in f if not line.startswith("#")]


def get_version():
    with open("dgprincess/__init__.py", "r") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"')
        else:
            raise ValueError("No version found")


setup(
    name="dgprincess",
    version=get_version(),
    packages=find_packages(),
    url="",
    license="",
    author="",
    author_email="",
    description="",
    install_requires=read_requirements("requirements.txt"),
    extras_require={},
    classifiers=[],
    entry_points={},
)
