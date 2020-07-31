#echo $1
echo "copying from container:dags/$1 to dags/$1"
sudo docker cp airflow_webserver_1:/usr/local/airflow/data/$1 data/$1 
