from scidag import DAG, Task


def test_get():
    task = Task()
    dag = DAG()
    dag.append(task, None)
    new_task = dag.get_task("task")
    assert task == new_task
