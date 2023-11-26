param($instances, $startingport, $dockerport)
$argList = "-NoExit D:\GitHub\cse138asgn3\Scripts\makeacontainer.ps1"
for (($i = 0),($address = 2), ($port = $startingport); $i -lt $instances; ($i++), ($address++),($port++))
{
    Start-Process powershell -ArgumentList "$argList -port $port -address 10.10.0.$address -dockerport $dockerport -id $i"
}