<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

// POSTで送られてきたRSSを受け取る
$raw = file_get_contents("php://input");
$data = json_decode($raw, true);

if (!$data || !isset($data["rss"])) {
    echo json_encode(["ok"=>false,"error"=>"RSSなし"]);
    exit;
}

// XML解析
$xml = simplexml_load_string($data["rss"]);
if (!$xml) {
    echo json_encode(["ok"=>false,"error"=>"XML解析失敗"]);
    exit;
}

// 最新アイテムタイトルだけ返す例
$items = $xml->channel->item;
echo json_encode([
    "ok"=>true,
    "latest_title" => (string)$items[0]->title
]);
