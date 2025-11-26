#!/bin/bash
# Cleanup minikube deployments and services for this project
set -e
kubectl delete namespace devops --ignore-not-found
helm uninstall prometheus -n monitoring || true
kubectl delete namespace monitoring --ignore-not-found
echo "Cleanup finished."
