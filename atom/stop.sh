docker ps --format '{{.Names}}' | grep "^atom-" | awk '{print $1}' | xargs -I {} docker stop {}
