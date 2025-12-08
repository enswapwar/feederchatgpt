<?php
$url = "https://www1.x-feeder.info/lo18bx2n/rss.php";

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);

// ブラウザ偽装
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "User-Agent: Mozilla/5.0"
]);

$raw = curl_exec($ch);
if ($raw === false) die("取得死");

// RSS 部分だけ抽出（正規表現）
if (!preg_match('/(<rss[\s\S]*?<\/rss>)/', $raw, $m)) {
    die("RSS終端がねぇ（正規もヒットしねぇ）");
}

$pure = $m[1];  // 正しいRSSだけがここに入る

$xml = simplexml_load_string($pure);
if (!$xml) die("XML parse死");

foreach ($xml->channel->item as $item) {
    echo $item->title . "<br>";
}
