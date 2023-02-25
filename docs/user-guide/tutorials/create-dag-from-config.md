---
title: Create From Config
sidebar_label: Create From Config
---

### Specify config.yaml

``` yaml title="cfg.yaml"
info: "some yaml metadata"
dag:
  node_a:
    name: node_a
    content:
      _target_: fn_a
      _partial_: true
    edges:
      - node_b1.a
  node_b:
    name: node_c
    content:
      _target_: fn_b
      _partial_: true
```

### Load DAG
```python title="create_from_config.py"
import DAG
cfg = DAG.load_cfg("/path/to/cfg.yaml")
dag = DAG.from_config(cfg)
dag.run()
```

### Output
```bash title="output"
foo:bar
```
