<?php
$url = "https://www1.x-feeder.info/lo18bx2n/rss.xml"; // 実際のRSS URLに合わせてな

$raw = file_get_contents($url);
// </rss> でRSSが終わるのでそこまでを強制的に切り出す
$pos = strpos($raw, '</rss>');
if ($pos !== false) {
    $xml_clean = substr($raw, 0, $pos + 6); // '</rss>' の6文字まで
} else {
    die("RSS終端が見つからねぇ");
}

$xml = simplexml_load_string($xml_clean);
if (!$xml) die("XML解析死んだ");

foreach ($xml->channel->item as $item) {
    echo (string)$item->title . "\n";
}
