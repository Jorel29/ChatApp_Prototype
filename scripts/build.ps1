param($i = 1,$sp = 13800,$dp = 13800)
Write-Host $i, $sp, $dp
& ".\Scripts\builddockercontainerPS.ps1"
& ".\\Scripts\runcontainersPS.ps1" -instances $i -startingport $sp -dockerport $dp
Start-Sleep -s 5
#python .\tests\test_assignment3.py 13800:10.10.0.2:13800 13801:10.10.0.3:13800
#curl --request PUT --header "Content-Type: application/json" --write-out "%{http_code}\n" --data '{"num_shards": 2,"nodes": ["address1:port1", "address2:port2", "address3:port3"]}' http://localhost:13800/kvs/admin/view