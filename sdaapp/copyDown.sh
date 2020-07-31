#echo $1
echo "copying from container:dags/$1 to dags/$1"
sudo docker cp airflow_webserver_1:/usr/local/airflow/dags/$1 dags/$1 
