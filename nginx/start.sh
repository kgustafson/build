docker run --name nginx -v content:/usr/share/nginx/html:rw -d -p 8080:80 nginx
docker cp ./content/. nginx:/usr/share/nginx/html/
