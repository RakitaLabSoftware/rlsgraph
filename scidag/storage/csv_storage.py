import asyncio
from typing import Any

# try:
import pandas as pd

from scidag.storage.base import Storage

# except ImportError:
# raise ModuleNotFoundError(f"Dask not found try to install scidag[dask]")


class CSVStorage(Storage):
    def __init__(self) -> None:
        self.df = pd.DataFrame(columns=["target", "variable", "source", "value"])

    def store(self, source: str, value: Any) -> None:
        self.df.loc[self.df.source == source, "value"] = value

    async def get(self, target: str) -> Any:
        while True:
            df = self.df[self.df["target"] == target]
            if df["value"].isnull().sum() == 0:
                ret = {
                    row["variable"]: row["value"]
                    for row in df[["variable", "value"]].to_dict("records")
                }
                # If all values in the column are non-None, return the DataFrame
                return ret

            # Wait for a short time before checking again
            await asyncio.sleep(1)

    def add_dependency(
        self,
        target: str,
        variable: str,
        source: str,
    ) -> None:
        row = pd.DataFrame(
            [
                {
                    "target": target,
                    "variable": variable,
                    "source": source,
                    "value": None,
                }
            ]
        )
        df = pd.concat([self.df, row])
        self.df = df.reset_index(drop=True)

    def remove_dependency(self, target: str, variable: str, source: str) -> None:
        df = self.df
        index = df[
            (df.source == source) & (df.target == target) & (df.variable == variable)
        ].index[0]
        self.df = df.drop(index=index)

    def save(self):
        self.df.to_csv("storage.csv")


async def task_a(storage: Storage):
    await asyncio.sleep(1)
    storage.store("A", "a")


async def task_b(storage: Storage):
    val = await storage.get("B")
    val = val["b"] + "b"
    await asyncio.sleep(1)
    storage.store("B", val)


async def task_c(storage: Storage):
    val = await storage.get("C")
    val = val["c"] + "c"
    await asyncio.sleep(1)
    storage.store("C", val)


async def task_d(storage: Storage):
    values = await storage.get("D")
    res = "d"
    for val in values.values():
        res += val
    await asyncio.sleep(1)
    storage.store("D", res)


async def task_e(storage: Storage):
    val = await storage.get("E")
    await asyncio.sleep(2)


async def main(storage):
    await asyncio.gather(
        task_a(storage),
        task_b(storage),
        task_c(storage),
        task_d(storage),
        task_e(storage),
    )


if __name__ == "__main__":
    storage = CSVStorage()
    storage.add_dependency("B", "b", "A")
    storage.add_dependency("D", "d1", "A")
    storage.add_dependency("C", "c", "B")
    storage.add_dependency("D", "d2", "B")
    storage.add_dependency("D", "d3", "C")
    storage.add_dependency("E", "e", "D")
    storage.add_dependency("X", "X", "X")
    print(storage.df.head(10))
    storage.remove_dependency("X", "X", "X")
    asyncio.run(main(storage))
    print(storage.df.head(6))
