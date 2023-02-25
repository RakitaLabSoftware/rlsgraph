import asyncio
from typing import Any
import numpy as np
import pandas as pd

from scidag.storage.base import Storage


class CSVStorage(Storage):
    def __init__(self, data: pd.DataFrame | None = None) -> None:
        self._df = (
            data
            if data is not None
            else pd.DataFrame(columns=["target", "variable", "source", "value"])
        )

    @classmethod
    def from_config(cls, cfg) -> "CSVStorage":
        data = build_csv_data(cfg)
        return cls(data=data)

    def store(self, source: str, value: Any) -> None:
        self._df.loc[self._df["source"] == source, "value"] = value

    async def get(self, target: str) -> Any:
        # TODO: cycle only if diff in the target
        while True:
            df = self._df[self._df["target"] == target]
            if df["value"].isnull().sum() == 0:
                ret = {
                    row["variable"]: row["value"]
                    for row in df[["variable", "value"]].to_dict("records")
                }
                # If all values in the column are non-None, return the DataFrame
                return ret

            # Wait for a short time before checking again
            await asyncio.sleep(0.1)

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
                    "value": np.NaN,
                }
            ]
        )
        df = pd.concat([self._df, row])
        self._df = df.reset_index(drop=True)

    def remove_dependency(self, target: str, variable: str, source: str) -> None:
        df = self._df
        index = df[
            (df.source == source) & (df.target == target) & (df.variable == variable)
        ].index[0]
        self._df = df.drop(index=index)

    def save(self):
        self._df.to_csv("storage.csv")

    def show(self) -> Any:
        return self._df.head()


def build_csv_data(cfg) -> pd.DataFrame:
    df = pd.DataFrame(columns=["target", "variable", "source", "value"])
    for name, node in cfg.dag.items():
        for edge in node.edges:
            tgt, vr = edge.split(".")
            row = pd.DataFrame(
                [{"target": tgt, "variable": vr, "source": name, "value": None}]
            )
            df = pd.concat([df, row], ignore_index=True)
    return df


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
    print(storage)
    storage.remove_dependency("X", "X", "X")
    asyncio.run(main(storage))
    print(storage._df.head())
