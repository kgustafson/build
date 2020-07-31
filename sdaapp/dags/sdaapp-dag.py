# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
### Tutorial Documentation
Documentation that goes along with the Airflow tutorial located
[here](https://airflow.incubator.apache.org/tutorial.html)
"""
from datetime import datetime
from datetime import timedelta

import airflow
from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash_operator import BashOperator

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(0),
    'email': ['alex.stimpson@assett.net'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'adhoc':False,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'trigger_rule': u'all_success'
}

dag = DAG(
    'sdaapp_dag',
    default_args=default_args,
    catchup=False,
    description='DAG for wrangling, processing, and updating display for SDA app',
    schedule_interval=timedelta(minutes=5),
)

# Operator Definition

t1 = BashOperator(
    task_id='create_snippets',
    bash_command='python /usr/local/airflow/tasks/pytail.py ',
    dag=dag,
)

t2 = BashOperator(
    task_id='subset_data',
    bash_command='bash /usr/local/airflow/tasks/subset.sh ',
    dag=dag,
)

t3 = BashOperator(
    task_id='calculate_maintenance_score',
    bash_command='bash /usr/local/airflow/tasks/calculate_maintenance_score.sh ',
    dag=dag,
)


t1 >> t2 >> t3
