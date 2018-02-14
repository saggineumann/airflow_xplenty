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

### `XplentyFindOrStartClusterOperator`

This operator finds or starts a cluster in the given environment. It will only
find clusters that are `pending`, `starting`, or `available`. It pushes the
cluster ID into the XComs.

#### Arguments

In addition to the standard [BaseOperator arguments](https://airflow.incubator.apache.org/code.html#baseoperator), the following are exposed

|   Argument   |   Type    | Required | Description |
|:------------ |:--------- |:-------- |:----------- |
| env          | `String`  | False    | The environment for the cluster (either `production` or `sandbox`, default is `sandbox`) |


### `XplentyWaitForClusterSensor`

This sensor operator waits for a cluster to be `available` or in a terminating
state. It finds the cluster ID from the XComs.

#### Arguments

In addition to the standard [BaseOperator arguments](https://airflow.incubator.apache.org/code.html#baseoperator), the following are exposed

|       Argument        |   Type    | Required | Description |
|:--------------------- |:--------- |:-------- |:----------- |
| start_cluster_task_id | `String`  | True     | The task ID of a XplentyFindOrStartClusterOperator  |


### `XplentyFindOrStartJobOperator`

This operator finds an already runnin job or starts a new job for a package on
an Xplenty cluster. It finds the cluster ID from the XComs.

#### Arguments

In addition to the standard [BaseOperator arguments](https://airflow.incubator.apache.org/code.html#baseoperator), the following are exposed

|       Argument        |   Type     | Required | Description |
|:--------------------- |:---------- |:-------- |:----------- |
| start_cluster_task_id | `String`   | True     | The task ID of a XplentyFindOrStartClusterOperator  |
| package_id            | `Integer`  | True*    | The ID of the package to run |
| package_name          | `String`   | True*    | The name of the package to run |
| variables_fn          | `Function` | False    | Optional function that takes the context from #execute and returns a dict of variables to pass to the package |

 * Either `package_id` or `package_name` (but not both) must be supplied to the
 constructor.

### `XplentyWaitForJobSensor`

This sensor operator waits for a job to complete (either successfully or
failing). It finds the job ID from the XComs.

#### Arguments

In addition to the standard [BaseOperator arguments](https://airflow.incubator.apache.org/code.html#baseoperator), the following are exposed

|     Argument      |   Type    | Required | Description |
|:----------------- |:--------- |:-------- |:----------- |
| start_job_task_id | `String`  | True     | The task ID of a XplentyStartJobOperator  |


#### Example

```python
from airflow_xplenty.operators import XplentyFindOrStartClusterOperator
from airflow_xplenty.operators import XplentyWaitForClusterSensor
from airflow_xplenty.operators import XplentyStartJobOperator
from airflow_xplenty.operators import XplentyWaitForJobSensor

dag = DAG('test', schedule_interval='@daily')

start_cluster = XplentyFindOrStartClusterOperator(task_id='start_cluster',
    env='production', dag=dag)

wait_for_cluster = XplentyWaitForClusterSensor(task_id='wait_for_cluster',
    start_cluster_task_id=start_cluster.task_id, dag=dag)

wait_for_cluster.set_upstream(start_cluster)

start_job = XplentyStartJobOperator(task_id='start_job', package_id=314,
    start_cluster_task_id=start_cluster.task_id, dag=dag)

start_job.set_upstream(wait_for_cluster)

wait_for_job = XplentyWaitForJobSensor(task_id='wait_for_job',
    start_job_task_id=start_job.task_id, dag=dag)

wait_for_job.set_upstream(start_job)
```
