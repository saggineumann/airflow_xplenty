# Airflow Xplenty

Airflow plugin wrappers for the Xplenty API.

## Configuration

Add your Xplenty API credentials to `airflow.cfg` in an `xplenty` section, e.g.

```ini
[xplenty]
account_id = $XPLENTY_ACCOUNT_ID
api_key = $XPLENTY_API_KEY
```

In the example above, Airflow will read the `account_id` and `api_key` from the
environment variables `XPLENTY_ACCOUNT_ID` and `XPLENTY_API_KEY`, which
obviates the need to store these sensitive credentials in the app.

## Operators

### `XplentyJobOperator`

This operator runs a package as a job on a cluster. The cluster will be lazily
started, i.e. if a cluster is running that one will be used, otherwise a new
cluster will be spun up.

#### Arguments

In addition to the standard (BaseOperator arguments)[https://airflow.incubator.apache.org/code.html#baseoperator], the following are exposed in the `XplentyJobOperator`

|   Argument   |   Type   | Required | Description |
|:------------ |:-------- |:-------- |:----------- |
| env          | `String` | False    | The environment the cluster will be lazily started (default `sandbox`) |
| package_name | `String` | True     | The name of the package to run |

#### Example

```python
from airflow_xplenty.operators import XplentyJobOperator

dag = DAG('test', schedule_interval='@daily')

XplentyJobOperator(task_id='run_test', env='production',
    package_name='test_package', dag=dag)
```
