param($port, $address, $dockerport, $id)
Write-Host "${port}:$dockerport $address $id"
#uncomment below to actually run the docker container
docker run --publish ${port}:$dockerport --net=kv_subnet --ip=$address --name="node$id" --env ADDRESS="${address}:$dockerport" --env PYTHONUNBUFFERED=1 chatapp:1.0