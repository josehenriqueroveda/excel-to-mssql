# excel-to-mssql
`excel2mssql` is a Python library that provides functionality to read data from Excel and CSV files and insert it into a Microsoft SQL Server database.

## Installation
```bash
pip install excel2mssql
```

## Usage
### CsvToMssql
To use `CsvToMssql`, you need to create an instance of the class and pass in the path to the CSV file, the name or IP address of the SQL Server, the name of the database to connect to, the name of the table to insert the data into, and the username and password to use for authentication.

```python
from excel2mssql.worker import CsvToMssql

csv_path = "path/to/csv/file.csv"

# This is just an example, preferably you would store these in environment variables
server = "localhost"
database = "mydatabase"
schema = "myschema"
table_name = "mytable"
username = "myusername"
password = "mypassword"

csv_to_mssql = CsvToMssql(
    csv_path=csv_path,
    server=server,
    database=database,
    schmea=schema,
    table_name=table_name,
    username=username,
    password=password,
)

columns = ["column1", "column2", "column3"]

csv_to_mssql.csv_to_mssql(columns=columns, sep=",", encoding="utf-8", action="replace")
```

### ExcelToMssql
To use `ExcelToMssql`, you need to create an instance of the class and pass in the path to the Excel file, the name or IP address of the SQL Server, the name of the database to connect to, the name of the table to insert the data into, and the username and password to use for authentication.

```python
from excel2mssql.worker import ExcelToMssql

excel_path = "path/to/excel/file.xlsx"

# This is just an example, preferably you would store these in environment variables
server = "localhost"
database = "mydatabase"
schema = "myschema"
table_name = "mytable"
username = "myusername"
password = "mypassword"

excel_to_mssql = ExcelToMssql(
    excel_path=excel_path,
    server=server,
    database=database,
    schmea=schema,
    table_name=table_name,
    username=username,
    password=password,
)

sheet_name = "Sheet1"
columns = ["column1", "column2", "column3"]

excel_to_mssql.excel_to_mssql(sheet_name=sheet_name, columns=columns, action="replace")
```

## License
This package is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing
If you find a bug or have a feature request, please open an issue on the repository. If you would like to contribute code, please fork the repository and submit a pull request.

Before submitting a pull request, please make sure that your code adheres to the following guidelines:
 - Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide.
 - Write docstrings for all functions and classes.
 - Write unit tests for all functions and classes.
 - Make sure that all tests pass by running pytest.
 - Keep the code simple and easy to understand.

