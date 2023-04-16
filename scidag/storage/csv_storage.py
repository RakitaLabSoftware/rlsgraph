import asyncio
import os
import joblib
from typing import Any
import numpy as np
import pandas as pd
from scidag.utils.create_path import create_path
from scidag.storage.base import Storage

supported_types = (int, str, list, tuple, dict, np.ndarray)


class CSVStorage(Storage):
    def __init__(self, data: pd.DataFrame | None = None) -> None:
        self._df = (
            data
            if data is not None
            else pd.DataFrame(columns=["target", "variable", "source", "value"])
        )
        self.path_dir = create_path("outs")
        self._df["value"] = self._df["value"].astype(object)

    @classmethod
    def from_config(cls, cfg) -> "CSVStorage":
        data = build_csv_data(cfg)
        return cls(data=data)

    def store(self, source: str, value: Any) -> None:
        # TODO: Move path to init function so you could save the assets
        if type(value) not in supported_types:
            value = joblib.dump(
                value,
                os.path.join(self.path_dir, f"{source}.{type(value).__name__}.pkl"),
            )
        self._df.loc[self._df["source"] == source, "value"] = self._df.loc[
            self._df["source"] == source, "value"
        ].apply(lambda x: value)

    async def get(self, target: str) -> Any:
        # TODO: cycle only if diff in the target
        while True:
            df = self._df[self._df["target"] == target]

            def load_value(value: Any):
                if type(value) not in supported_types:
                    # TODO: Refactor
                    print(type(value))
                    return joblib.load(value[0])
                return value

            if df["value"].notna().all():
                ret = {
                    row["variable"]: load_value(row["value"])
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
        df = pd.concat([self._df, row])
        self._df = df.reset_index(drop=True)

    def remove_dependency(self, target: str, variable: str, source: str) -> None:
        df = self._df
        index = df[
            (df.source == source) & (df.target == target) & (df.variable == variable)
        ].index[0]
        self._df = df.drop(index=index)

    def save(self):
        save_path = self.path_dir if self.path_dir is not None else "./"
        self._df.to_csv(os.path.join(save_path, "storage.csv"))

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
