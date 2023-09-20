import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyctf_lite", 
    version="1.0",
    author="Tom Holroyd",
    author_email="holroydt@mail.nih.gov",
    description="Lite version of pyctf to open/save CTF datasets in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nih-megcore/pyctf-lite",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0",
        "Operating System :: Linux/Unix",
    ],
    install_requires=['numpy'],
    scripts=['addMarker/addMarker.py', 'addMarker/delMarker.py'],
)
