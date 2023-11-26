docker container stop $(docker container list -q)
docker container prune --force
docker image rm chatapp:1.0