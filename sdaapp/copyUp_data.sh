#echo $1
echo "copying data/$1 to container:data/$1"
sudo docker cp data/$1 airflow_webserver_1:/usr/local/airflow/data/$1
#tar -cf - data/$1 --mode u=+r,g=-rwx,o=-rwx --owner tcsuser | docker cp - airflow_webserver_1:/usr/local/airflow/data/
