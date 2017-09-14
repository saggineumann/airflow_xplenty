# Airflow Xplenty

Airflow plugin wrappers for the Xplenty API.

## Usage

```python
from airflow_xplenty.operators import XplentyJobOperator

dag = DAG('test', default_args={}, schedule_interval='@daily')

XplentyJobOperator(task_id='run_test',
    package_name='test_package',
    dag=dag)
```
