#!/bin/bash

kubectl create secret generic mariadb --from-env-file kube/mariadb.secret
kubectl create secret generic django --from-env-file kube/django.secret

kubectl apply -f kube/mariadb-pv.yaml
kubectl apply -f kube/media-pv.yaml
kubectl apply -f kube/rabbitmq-controller-service.yaml
kubectl apply -f kube/mariadb-deployment-service.yaml
kubectl apply -f kube/celery-deployment.yaml
kubectl apply -f kube/gunicorn-deployment-service.yaml
kubectl apply -f kube/nginx-deployment-service.yaml
