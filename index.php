<?php

$url = "https://www1.x-feeder.info/lo18bx2n/rss.php";

$context = stream_context_create([
    "http" => [
        "method" => "GET",
        "header" => "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
    ],
    "ssl" => [
        "verify_peer" => false,
        "verify_peer_name" => false
    ]
]);

$raw = @file_get_contents($url, false, $context);

if ($raw === false) {
    echo "RSS取得失敗（UA偽装でも無理）\n";
    exit;
}

$rss = @simplexml_load_string($raw);

if (!$rss) {
    echo "XML解析失敗（アクセスはできたが中身が読めない）\n";
    exit;
}

echo "=== RSS取得成功 ===\n";
print_r($rss);
