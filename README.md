# Airflow Xplenty

Airflow plugin wrappers for the Xplenty API.

## Operators

### `XplentyJobOperator`

This operator runs a package as a job on a cluster. The cluster will be lazily
started, i.e. if a cluster is running that one will be used, otherwise a new
cluster will be spun up.

#### Arguments

In addition to the standard (BaseOperator arguments)[https://airflow.incubator.apache.org/code.html#baseoperator], the following are exposed in the `XplentyJobOperator`

|   Argument   |   Type   | Required | Description |
|:------------ |:-------- |:-------- |:----------- |
| account_id   | `String` | False    | The Xplenty account ID (defaults to the environment variable `XPLENTY_ACCOUNT_ID`) |
| api_key      | `String` | False    | The Xplenty API key (defaults to the environment variable `XPLENTY_API_KEY`) |
| env          | `String` | False    | The environment the cluster will be lazily started (default `sandbox`) |
| package_name | `String` | True     | The name of the package to run |

#### Example

```python
from airflow_xplenty.operators import XplentyJobOperator

dag = DAG('test', schedule_interval='@daily')

XplentyJobOperator(task_id='run_test',
    accont_id='TestAccount',
    api_key='TestKey',
    env='production',
    package_name='test_package',
    dag=dag)
```
