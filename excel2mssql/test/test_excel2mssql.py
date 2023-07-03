import sys

sys.path.append("../")

import pytest
import pandas as pd
from sqlalchemy.engine.base import Engine

from worker import CsvToMssql, ExcelToMssql
from data.constants import SERVER, DATABASE, SCHEMA, TABLE_NAME, USERNAME, PASSWORD


@pytest.fixture
def csv_to_mssql():
    return CsvToMssql(
        csv_path="../data/csv_data_test.csv",
        server=SERVER,
        database=DATABASE,
        schema=SCHEMA,
        table_name=TABLE_NAME,
        username=USERNAME,
        password=PASSWORD,
    )


def test_read_csv(csv_to_mssql):
    df = csv_to_mssql.read_csv(columns=["col1", "col2"], sep=",", encoding="utf-8")
    assert isinstance(df, pd.DataFrame)
    assert set(df.columns) == set(["col1", "col2"])


def test_create_engine(csv_to_mssql):
    engine = csv_to_mssql.create_engine()
    assert isinstance(engine, Engine)


def test_insert_csv_data(csv_to_mssql):
    df = pd.DataFrame({"col1": [2, 6, 4, 9], "col2": [5, 2, 2, 0]})
    engine = csv_to_mssql.create_engine()
    csv_to_mssql.insert_data(df, engine, action="replace", chunksize=len(df))
    result = pd.read_sql_table(TABLE_NAME, engine)
    print(result)
    print("#########")
    print(df)
    assert result.equals(df)


def test_csv_to_mssql(csv_to_mssql):
    assert csv_to_mssql.csv_to_mssql(
        columns=["col1", "col2"], sep=",", encoding="utf-8", action="replace"
    )
    engine = csv_to_mssql.create_engine()
    result = pd.read_sql_table(TABLE_NAME, engine)
    assert set(result.columns) == set(["col1", "col2"])


@pytest.fixture
def excel_to_mssql():
    return ExcelToMssql(
        excel_path="../data/excel_data_test.xlsx",
        server=SERVER,
        database=DATABASE,
        schema=SCHEMA,
        table_name=TABLE_NAME,
        username=USERNAME,
        password=PASSWORD,
    )


def test_read_excel(excel_to_mssql):
    df = excel_to_mssql.read_excel(sheet=0, columns=["col1", "col2"])
    assert isinstance(df, pd.DataFrame)
    assert set(df.columns) == set(["col1", "col2"])


def test_insert__excel_data(excel_to_mssql):
    df = pd.DataFrame({"col1": [2, 6, 4, 9], "col2": [5, 2, 2, 0]})
    engine = excel_to_mssql.create_engine()
    excel_to_mssql.insert_data(df, engine, action="replace", chunksize=len(df))
    result = pd.read_sql_table(TABLE_NAME, engine)
    assert result.equals(df)


def test_excel_to_mssql(excel_to_mssql):
    assert excel_to_mssql.excel_to_mssql(
        sheet=0, columns=["col1", "col2"], action="replace"
    )
    engine = excel_to_mssql.create_engine()
    result = pd.read_sql_table(TABLE_NAME, engine)
    assert set(result.columns) == set(["col1", "col2"])
