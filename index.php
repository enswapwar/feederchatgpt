<?php
// JSON受け取り
$raw = file_get_contents("php://input");
$data = json_decode($raw, true);

if (!$data || !isset($data["rss"])) {
    echo "RSSなし";
    exit;
}

$xml_raw = $data["rss"];

// XMLパース
$xml = simplexml_load_string($xml_raw);
if (!$xml) {
    echo "XML解析失敗";
    exit;
}

// 最新アイテムタイトルだけ返すテスト
$items = $xml->channel->item;
if (count($items) == 0) {
    echo "itemなし";
    exit;
}

echo "OK: " . (string)$items[0]->title;
