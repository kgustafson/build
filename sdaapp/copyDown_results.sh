#echo $1
echo "copying from container:dags/$1 to dags/$1"
sudo docker cp sdaapp_webserver_1:/usr/local/airflow/processed_data/$1 results/$1 
