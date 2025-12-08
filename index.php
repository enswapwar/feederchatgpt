<?php
$url = "https://www1.x-feeder.info/lo18bx2n/rss.xml";

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);

// ブラウザ偽装
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    ."Chrome/127.0.0.1 Safari/537.36"
]);

$raw = curl_exec($ch);

if ($raw === false) die("403か通信エラー");

$pos = strpos($raw, '</rss>');
if ($pos === false) die("RSS終端がねぇ");

$xml_clean = substr($raw, 0, $pos + 6);
$xml = simplexml_load_string($xml_clean) or die("XML parse死");

foreach ($xml->channel->item as $item) {
    echo $item->title . "\n";
}
