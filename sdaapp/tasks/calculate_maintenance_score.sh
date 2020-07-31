for file in /usr/local/airflow/processed_data/*.csv; do
    python /usr/local/airflow/tasks/calculate_maintenance_score.py "$file"
done
