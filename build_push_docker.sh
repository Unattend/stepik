docker build -t unattend/stepik-app:latest docker_app
docker push unattend/stepik-app:latest

docker build -t unattend/stepik-nginx:latest docker_nginx
docker push unattend/stepik-nginx:latest

#docker build -t unattend/stepik-celery:latest docker_celery
#docker push unattend/stepik-celery:latest

