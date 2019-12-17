docker cp deployment-update.yaml kube-master:deployment-update.yaml
docker exec -it kube-master kubectl apply -f deployment-update.yaml
docker exec -it kube-master kubectl get pods -l app=nginx
