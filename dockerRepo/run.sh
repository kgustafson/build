#sudo docker-compose up -d
sudo docker run -d -p 4444:5000 --name registry -v registry-store:/var/lib/registry registry:2
