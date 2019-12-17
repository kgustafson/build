docker cp deployment.yaml kube-master:deployment.yaml
docker exec -it kube-master kubectl apply -f deployment.yaml
docker exec -it kube-master kubectl describe deployment nginx-deployment

