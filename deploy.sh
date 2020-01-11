#!/bin/bash
echo "Start deployment"
gcloud functions deploy trainify --runtime python37 --trigger-http --allow-unauthenticated --entry-point=root --region=europe-west1
echo "Deployment finished"