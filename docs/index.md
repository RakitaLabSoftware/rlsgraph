---
sidebar_position: 1
id: intro
title: Getting started
sidebar_label: Getting started
---

## Introduction

Bla bla bla

### Key features

* Easy to run and configure
* configs are self explanatory and you don't need anything except one .yaml file.
* This library is distributed with minimal dependencies

## Quick start guide

This guide will show you some of the most important features you get by writing your application as a Hydra app.
If you only want to use Hydra for config composition, check out Hydra's [compose API](advanced/compose_api.md) for an alternative.
Please also read the full [tutorial](tutorials/basic/your_first_app/1_simple_cli.md) to gain a deeper understanding.

### Installation

* Using PIP:

```bash
pip install scidag
```

* Using Poetry:

```bash
poetry add scidag
```

* From source

```bash
git clone https://github.com/RakitaLabSoftware/scidag.git scidag
cd scidag 
poetry install 
```

### Basic Usage

#### Config

```yaml
info: "
here should be your metadata
"
dag:
  node_a:
    content:
      _target_: fn_name_a
      _partial_: true
      start: 10
      finish: 30 
    edges:
      - node_b.b1
      - node_b.b2
  node_b:
    content:
      _target_: fn_name_b
      _partial_: true
    vars:
      b1: 
        type: int
        value: None
      b2:
        type: int
        value: None
    edges:
      - node_c.c
  node_c:
    content:
      _target_: fn_name_c
      _partial_: true
    vars:
      c:
        type: int
        value: None
```

For more detailed overview for how config works presented [here](https://github.com/RakitaLabSoftware/scidag/tree/main/examples).

#### Application

```python
import scidag as sd

cfg = cd.load_config("/path/to/config.yaml")
dag = sd.DAG.from_config(cfg)
dag.run()
```

### Other

More detailed examples could be found [here](https://github.com/RakitaLabSoftware/scidag/tree/main/examples).