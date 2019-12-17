docker cp deployment-scale.yaml kube-master:deployment-scale.yaml
docker exec -it kube-master kubectl apply -f deployment-scale.yaml
docker exec -it kube-master kubectl get pods -l app=nginx
