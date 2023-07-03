import pandas as pd
from typing import Literal, List
from tqdm import tqdm
from urllib.parse import quote_plus
from sqlalchemy import create_engine


def chunker(seq, size):
    """
    Splits a sequence into chunks of a specified size.

    Args:
        seq (sequence): The sequence to be chunked.
        size (int): The size of each chunk.

    Returns:
        generator: A generator that yields the chunks of the sequence.
    """
    if size == 0:
        raise ValueError("Chunk size must be greater than zero")
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


class CsvToMssql:
    """
    A class that provides functionality to read a CSV file and insert its data into a Microsoft SQL Server database.

    Attributes:
        csv_path (str): The path to the CSV file.
        server (str): The name or IP address of the SQL Server.
        database (str): The name of the database to connect to.
        schema (str | None): The name of the schema to use. If None, the default schema is used.
        table_name (str): The name of the table to insert the data into.
        username (str): The username to use for authentication.
        password (str): The password to use for authentication.
        conn (str): The connection string to use for connecting to the database.

    Methods:
        read_csv(columns: List[str], sep: str, encoding: str) -> pd.DataFrame:
            Reads the CSV file and returns a pandas DataFrame with the specified columns.

        create_engine() -> sqlalchemy.engine.base.Engine:
            Creates and returns a SQLAlchemy engine object for connecting to the database.

        insert_data(df: pd.DataFrame, engine, action: Literal["fail", "replace", "append"], chunksize: int) -> None:
            Inserts the data from the DataFrame into the database using the specified action and chunk size.

        csv_to_mssql(columns: List[str], sep: str = ",", encoding: str = "utf-8", action: Literal["fail", "replace", "append"] = "replace") -> bool:
            Reads the CSV file, inserts its data into the database, and returns True if successful.
    """
    def __init__(
        self,
        csv_path: str,
        server: str,
        database: str,
        schema: str | None,
        table_name: str,
        username: str,
        password: str,
    ):
        self.csv_path = csv_path
        self.server = server
        self.database = database
        self.schema = schema
        self.table_name = table_name
        self.username = username
        self.password = password
        self.conn = quote_plus(
            "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
            + self.server
            + ";DATABASE="
            + self.database
            + ";UID="
            + self.username
            + ";PWD="
            + self.password
        )

    def read_csv(self, columns: List[str], sep: str, encoding: str) -> pd.DataFrame:
        return pd.read_csv(self.csv_path, usecols=columns, sep=sep, encoding=encoding)

    def create_engine(self):
        return create_engine(
            f"mssql+pyodbc:///?odbc_connect={self.conn}", fast_executemany=True
        )

    def insert_data(
        self,
        df: pd.DataFrame,
        engine,
        action: Literal["fail", "replace", "append"],
        chunksize: int,
    ) -> None:
        with tqdm(total=len(df)) as pbar:
            for _, cdf in enumerate(chunker(df, chunksize)):
                cdf.to_sql(
                    name=self.table_name,
                    schema=self.schema,
                    if_exists=action,
                    index=False,
                    method="multi",
                    con=engine,
                )
                pbar.update(chunksize)

    def csv_to_mssql(
        self,
        columns: List[str],
        sep: str = ",",
        encoding: str = "utf-8",
        action: Literal["fail", "replace", "append"] = "replace",
    ) -> bool:
        df = self.read_csv(columns, sep, encoding)
        engine = self.create_engine()
        chunksize = int(len(df) / 10) if len(df) > 10000 else len(df)
        self.insert_data(df, engine, action, chunksize)
        return True


class ExcelToMssql:
    """
    A class for reading data from an Excel file and inserting it into a Microsoft SQL Server database.

    Args:
        excel_path (str): The path to the Excel file to read.
        server (str): The name or IP address of the SQL Server.
        database (str): The name of the database to connect to.
        schema (str | None): The name of the schema to use. If None, the default schema is used.
        table_name (str): The name of the table to insert the data into.
        username (str): The username to use for authentication.
        password (str): The password to use for authentication.

    Methods:
        read_excel(sheet_name: str, columns: List[str], skiprows: int, encoding: str) -> pd.DataFrame:
            Reads the specified sheet from the Excel file and returns a pandas DataFrame with the specified columns.

        create_engine() -> sqlalchemy.engine.base.Engine:
            Creates and returns a SQLAlchemy engine object for connecting to the database.

        insert_data(df: pd.DataFrame, engine, action: Literal["fail", "replace", "append"], chunksize: int) -> None:
            Inserts the data from the DataFrame into the database using the specified action and chunk size.

        excel_to_mssql(sheet_name: str, columns: List[str], skiprows: int = 0, encoding: str = "utf-8", action: Literal["fail", "replace", "append"] = "replace") -> bool:
            Reads the specified sheet from the Excel file, inserts its data into the database, and returns True if successful.
    """
    def __init__(
        self,
        excel_path: str,
        server: str,
        database: str,
        schema: str | None,
        table_name: str,
        username: str,
        password: str,
    ):
        self.excel_path = excel_path
        self.server = server
        self.database = database
        self.schema = schema
        self.table_name = table_name
        self.username = username
        self.password = password
        self.conn = quote_plus(
            "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
            + self.server
            + ";DATABASE="
            + self.database
            + ";UID="
            + self.username
            + ";PWD="
            + self.password
        )

    def read_excel(self, sheet: str | int, columns: List[str] | None) -> pd.DataFrame:
        return pd.read_excel(self.excel_path, sheet_name=sheet, usecols=columns)

    def create_engine(self):
        return create_engine(
            f"mssql+pyodbc:///?odbc_connect={self.conn}", fast_executemany=True
        )

    def insert_data(
        self,
        df: pd.DataFrame,
        engine,
        action: Literal["fail", "replace", "append"],
        chunksize: int,
    ) -> None:
        with tqdm(total=len(df)) as pbar:
            for _, cdf in enumerate(chunker(df, chunksize)):
                cdf.to_sql(
                    name=self.table_name,
                    schema=self.schema,
                    if_exists=action,
                    index=False,
                    method="multi",
                    con=engine,
                )
                pbar.update(chunksize)

    def excel_to_mssql(
        self,
        sheet: str | int = 0,
        columns: List[str] | None = None,
        action: Literal["fail", "replace", "append"] = "replace",
    ) -> bool:
        df = self.read_excel(sheet=sheet, columns=columns)
        engine = self.create_engine()
        chunksize = int(len(df) / 10) if len(df) > 10000 else len(df)
        self.insert_data(df, engine, action, chunksize)
        return True
