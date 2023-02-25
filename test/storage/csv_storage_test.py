import os

import pandas as pd
import pytest

from scidag.storage.csv_storage import CSVStorage


@pytest.fixture
def storage():
    return CSVStorage()


def test_store(storage: CSVStorage):
    source = "test_source"
    value = 123
    storage.store(source, value)

    assert storage._df.loc[0, "source"] == source
    assert storage._df.loc[0, "value"] == value


@pytest.mark.asyncio
async def test_get(storage: CSVStorage):
    target = "test_target"
    variable1, variable2 = "var1", "var2"
    source1, source2 = "source1", "source2"
    value1, value2 = 123, "test"

    # Add dependencies
    storage.add_dependency(target, variable1, source1)
    storage.add_dependency(target, variable2, source2)

    # Store values for the dependencies
    storage.store(source1, value1)
    storage.store(source2, value2)

    # Get the values for the target
    result = await storage.get(target)

    # Check that the result contains the expected values
    assert result[variable1] == value1
    assert result[variable2] == value2


def test_add_dependency(storage: CSVStorage):
    target = "test_target"
    variable = "test_variable"
    source = "test_source"

    storage.add_dependency(target, variable, source)

    assert len(storage._df) == 1
    assert storage._df.loc[0, "target"] == target
    assert storage._df.loc[0, "variable"] == variable
    assert storage._df.loc[0, "source"] == source


def test_remove_dependency(storage: CSVStorage):
    target = "test_target"
    variable = "test_variable"
    source = "test_source"

    # Add a dependency
    storage.add_dependency(target, variable, source)

    # Remove the dependency
    storage.remove_dependency(target, variable, source)

    # Check that the dependency was removed
    assert len(storage._df) == 0


def test_save(storage: CSVStorage):
    # Save the DataFrame to a CSV file
    storage.save()

    # Check that the file exists and is not empty
    assert os.path.exists("storage.csv")
    assert os.path.getsize("storage.csv") > 0

    df = pd.read_csv("storage.csv")
    # Check that the contents of the file match the DataFrame
    df = df.loc[:, df.columns != "Unnamed: 0"]  # type: ignore
    assert df.equals(storage._df)
