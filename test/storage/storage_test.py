import asyncio

import pandas as pd
import pytest

from scidag.storage.build import _build_storage


@pytest.fixture
def storage():
    storage_type = _build_storage("CSV")
    storage = storage_type()

    storage.add_dependency("B", "b", "A")
    storage.add_dependency("D", "d1", "A")
    storage.add_dependency("C", "c", "B")
    storage.add_dependency("D", "d2", "B")
    storage.add_dependency("D", "d3", "C")
    storage.add_dependency("E", "e", "D")
    storage.add_dependency("X", "X", "X")

    return storage


@pytest.mark.asyncio
async def test_storage(storage):
    async def task_a(storage):
        await asyncio.sleep(1)
        storage.store("A", "a")

    async def task_b(storage):
        val = (await storage.get("B"))["b"] + "b"
        await asyncio.sleep(1)
        storage.store("B", val)

    async def task_c(storage):
        val = (await storage.get("C"))["c"] + "c"
        await asyncio.sleep(1)
        storage.store("C", val)

    async def task_d(storage):
        values = await storage.get("D")
        res = "d" + "".join(values.values())
        await asyncio.sleep(1)
        storage.store("D", res)

    async def task_e(storage):
        await asyncio.sleep(2)
        await storage.get("E")

    tasks = [
        task_a(storage),
        task_b(storage),
        task_c(storage),
        task_d(storage),
        task_e(storage),
    ]
    await asyncio.gather(*tasks)
    assert storage.show() == pd.DataFrame(["target", "variable", "source", "value"])
