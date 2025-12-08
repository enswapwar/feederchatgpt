<?php
$url="https://www1.x-feeder.info/lo18bx2n/rss.php";

$ch=curl_init($url);
curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);
curl_setopt($ch,CURLOPT_FOLLOWLOCATION,true);
curl_setopt($ch,CURLOPT_HTTPHEADER,["User-Agent: Mozilla/5.0"]);

$raw=curl_exec($ch);

file_put_contents("last_response.html",$raw ?: "EMPTY");

echo "dumped";
