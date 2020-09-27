import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

    setuptools.setup(
    name="mergeBams",
    version="0.13",
    author="Scott Furlan",
    author_email="scottfurlan@gmail.com",
    description="Merge sam/bam files with intelligent cell barcode preservation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scfurl/mergeBams.git",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.5',
    entry_points={'console_scripts': [
        'mergeBams = mergeBams.__main__:run_BamMerge',
    ]},
    )


"""
cd '/Users/sfurlan/OneDrive - Fred Hutchinson Cancer Research Center/computation/develop/mergeBams'
rm dist/*
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
scfurl



**At the FHCRC do the following... to install pipx**
sFH
ml Python
python3 -m pip install --user pipx
python3 -m pipx ensurepath


pipx uninstall mergeBams
pipx install git+https://github.com/scfurl/mergeBams --include-deps
pipx install --include-deps mergeBams
"""