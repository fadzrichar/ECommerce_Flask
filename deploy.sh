 
#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&
cd /var/www/backend #helloworld
git pull

source ~/.profile
echo "$DOCKERHUB_PASS" | docker login --username $DOCKERHUB_USER --password-stdin
docker stop backend
docker rm backend
docker rmi fadzricharisma/containerd:be2
docker run -d --name backend -p 5000:5000 fadzricharisma/containerd:be2
