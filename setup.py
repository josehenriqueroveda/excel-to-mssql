from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="excel2mssql",
    version="0.0.1",
    description="A package to insert data from Excel or CSV to MSSQL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jose Henrique Roveda",
    author_email="josehenriqueroveda.dev@gmail.com",
    url="https://github.com/josehenriqueroveda/excel-to-mssql",
    packages=find_packages(),
    install_requires=["pandas", "tqdm", "pyodbc", "sqlalchemy", "openpyxl"],
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
)