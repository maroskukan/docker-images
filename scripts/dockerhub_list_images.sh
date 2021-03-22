#!/bin/bash

set -e

# Load username and access token
[[ ! -z ${DOCKER_HUB_USER} ]] \
    && UNAME=${DOCKER_HUB_USER} \
    || (echo "Error: DOCKER_HUB_USER is empty. Use export DOCKER_HUB_USER=\"<username>\""; exit 1)

[[ ! -z ${DOCKER_HUB_ACCESS_TOKEN} ]] \
    && UPASS=${DOCKER_HUB_ACCESS_TOKEN} \
    || (echo "Error: DOCKER_HUB_ACCESS_TOKEN is empty. Use export DOCKER_HUB_ACCESS_TOKEN=\"<token>\""; exit 2)

echo "Credentials Loaded Sucessfully"

# get token to be able to talk to Docker Hub
TOKEN=$(curl -s -H "Content-Type: application/json" -X POST -d '{"username": "'${UNAME}'", "password": "'${UPASS}'"}' https://hub.docker.com/v2/users/login/ | jq -r .token)

# get list of namespaces accessible by user (not in use right now)
#NAMESPACES=$(curl -s -H "Authorization: JWT ${TOKEN}" https://hub.docker.com/v2/repositories/namespaces/ | jq -r '.namespaces|.[]')

# get list of repos for that user account
REPO_LIST=$(curl -s -H "Authorization: JWT ${TOKEN}" https://hub.docker.com/v2/repositories/${UNAME}/?page_size=10000 | jq -r '.results|.[]|.name')
echo "Repository List Loaded Sucessfully"

# build a list of all images & tags
for i in ${REPO_LIST}
do
  # get tags for repo
  IMAGE_TAGS=$(curl -s -H "Authorization: JWT ${TOKEN}" https://hub.docker.com/v2/repositories/${UNAME}/${i}/tags/?page_size=10000 | jq -r '.results|.[]|.name')

  # build a list of images from tags
  for j in ${IMAGE_TAGS}
  do
    # add each tag to list
    FULL_IMAGE_LIST="${FULL_IMAGE_LIST} ${UNAME}/${i}:${j}"
  done
done

# output list of all docker images
echo 
echo "User ${UNAME} has following Docker Images"
for i in ${FULL_IMAGE_LIST}
do
  echo ${i}
done