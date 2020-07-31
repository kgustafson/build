if [ "$(ls -A /usr/local/airflow/ingest/)" ]; then
    for file in /usr/local/airflow/snippets/*.csv; do
        python /usr/local/airflow/tasks/subset.py "$file"
    done
else
    echo "Folder is empty"
fi
