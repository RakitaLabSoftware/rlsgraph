---
title: Merging Multiple Dags
sidebar_label: Merging Multiple Dags
---
```python
import DAG
cfg_1 = DAG.load_config(cfg_1)
dag_1 = DAG.from_config(cfg_1)


cfg_2 = DAG.load_config(cfg_2)
dag_2 = DAG.from_config(cfg_2)

dag1.extend(dag_2, "node_a", "node_b")
```