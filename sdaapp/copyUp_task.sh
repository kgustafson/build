#echo $1
echo "copying tasks/$1 to container:tasks/$1"
sudo docker cp tasks/$1 sdaapp_webserver_1:/usr/local/airflow/tasks/$1
