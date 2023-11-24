#!/bin/bash
if [ -z $1 ] || [ -z $2 ];
  then
   echo "Usage: $0 <container_name> <container_tag>";
   exit 1;
fi

echo "Building container image $1:$2";
docker build -t $1:$2 .

#echo "Next actions for DockerHub:";
#echo "docker tag $1:$2 wbaldowski/$1:$2";
#echo "docker push wbaldowski/$1:$2";
#echo "docker logout";

echo "Next actions for GitHub Container Registry:";
echo "docker login https://ghcr.io";
echo "docker tag $1:$2 ghcr.io/glb-atos-mscc/$1:$2";
echo "docker push ghcr.io/glb-atos-mscc/$1:$2";
echo "docker logout";

echo "";
echo "Available images on localhost:";
docker images | grep -i $1

# end.