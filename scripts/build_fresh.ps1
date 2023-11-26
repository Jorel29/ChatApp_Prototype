docker container stop $(docker container list -q)
docker container prune --force
docker image rm chatapp:1.0
docker build -t chatapp:1.0 . 