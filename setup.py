from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="pymt",
    version="0.0.1",
    author="Stavros Filosidis",
    author_email="stavrosfil@gmail.com",
    description="A universal framework for means of mass transportation telematics scraping",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv2",
    # keywords="",
    # url="http://packages.python.org/an_example_pypi_project",
    packages=['pymt'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)"
    ],
    python_requires='>=3.6',
)
