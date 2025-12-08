<?php

$context = stream_context_create([
    "http" => [
        "method" => "GET",
        "header" => "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
    ]
]);

$url = "https://www1.x-feeder.info/lo18bx2n/rss.php";

$rss = @simplexml_load_file($url, null, LIBXML_NOCDATA, "", true, $context);

if (!$rss) {
    echo "RSS読み込み失敗（UA偽装も無理）\n";
    exit;
}

print_r($rss);
