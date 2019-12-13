sudo docker rm -f hurb-challenge
sudo docker rmi -f hurb-image:1.0
sudo docker build -t hurb-image:1.0 .
sudo docker run -d -p 5001:5000 --name hurb-challenge hurb-image:1.0
sudo docker image ls -a
sudo docker ps -a
sleep 1
curl -X GET http://localhost:5001/healthcheck
