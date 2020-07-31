#echo $1
echo "copying dags/$1 to container:dags/$1"
sudo docker cp dags/$1 airflow_webserver_1:/usr/local/airflow/dags/$1
