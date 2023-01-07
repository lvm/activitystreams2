import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="activitystreams2",
    version="0.0.1",
    description="A library that allows creation of ActivityStreams 2.0 Types",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/lvm/activitystreams2",
    author="Mauro Lizaur",
    author_email="mauro@sdf.org",
    license="BSD 3-Clause License",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["activitystreams2"],
    include_package_data=True,
    install_requires=[],
    entry_points={},
)
