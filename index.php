<?php
$url = "https://www1.x-feeder.info/lo18bx2n/rss.php";
$rss = simplexml_load_file($url);

if (!$rss) {
    echo "RSS取得失敗";
    exit;
}

$latest = $rss->channel->item[0];

$title = (string)$latest->title;     // "(123) 名前" 的なやつ
$desc  = (string)$latest->description;

echo "最新コメント\n";
echo "TITLE: $title\n";
echo "DESC: $desc\n";
