# Introduction
The motivation behind creating this library is to provide a flexible and scalable way to manage Directed Acyclic Graphs (DAGs) in Python. DAGs are widely used in scientific and machine learning workflows for tasks such as data cleaning, feature engineering, model training, and inference.

However, managing a complex DAG can quickly become a daunting task as the number of nodes and their dependencies grow. This library aims to simplify the management of DAGs by providing a high-level API for building, connecting, and running nodes in a DAG. It also provides a configurable storage system that allows users to persist the DAG and its dependencies across multiple runs.

Moreover, this library is designed to be flexible and extensible, allowing users to define their own custom nodes and storage systems. It is built on top of asyncio, enabling asynchronous execution of nodes in the DAG, which can significantly speed up the execution of complex DAGs.

Overall, this library aims to provide a robust and scalable solution for managing DAGs in Python, making it easier for scientists and machine learning engineers to build and manage complex workflows.

## Key features

* Easy to run and configure
* Сonfigs are self explanatory and you don't need anything except one .yaml file.
* SciDAG is distributed with minimal dependencies

## Quick start guide

This guide highlights some of the most crucial features that users can leverage. For a more detailed understanding, please refer to the more comprehensive [user guide](/docs/user-guide/index.md). Additionally, you cold check out th the SciDAG [API reference](/docs/api-reference). By utilizing SciDAG, users can streamline their application development process and build efficient, reliable, and scalable applications. Comprehensive documentation is provided to facilitate the integration of SciDAG into your project, and to ensure that users can fully leverage the features offered by the library.

### Installation

```bash
pip install scidag
```

*Additional information about installation could be found [here](user-guide/installation.md).*


### Basic Usage

#### Config

```yaml
info: ''
dag:
  node_a:
    name: node_a
    content:
      _target_: func_a
      _partial_: true
    variables: null
    edges:
    - node_b.x
    - node_c.x
  node_b:
    name: node_b
    content:
      _target_: func_b
      _partial_: true
    variables:
      x:
        type: None
        value: 0.5787140071322371
    edges:
    - node_d.x
  node_c:
    name: node_c
    content:
      _target_: func_c
      _partial_: true
    variables:
      x:
        type: None
        value: 0.5787140071322371
    edges:
    - node_d.y
  node_d:
    name: node_d
    content:
      _target_: func_d
      _partial_: true
    variables:
      x:
        type: None
        value: 0.6533319952665975
      y:
        type: None
        value: 0.8371667129334884
```

#### Application

```python
import scidag as sd

cfg = cd.load_config("/path/to/config.yaml")
dag = sd.DAG.from_config(cfg)
dag.run()
```
*For more detailed overview please see [user guide](/user-guide/index.md).*