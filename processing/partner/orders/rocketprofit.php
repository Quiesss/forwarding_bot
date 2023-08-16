<?php

$order = array (
	'campaign_id' => {stream},
	'name' => $_POST['name'],
	'phone' => $_POST['phone'],
	'sid5' => $_POST['sub1'],
	'sid2' => '{sub2}'
);

// Define ip
if (!empty($_SERVER['HTTP_CF_CONNECTING_IP'])) {
	$ip =  $_SERVER['HTTP_CF_CONNECTING_IP'];
}  elseif (!empty($_SERVER['HTTP_X_REAL_IP'])) {
	$ip =  $_SERVER['HTTP_X_REAL_IP'];
} elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
	$ip =  $_SERVER['HTTP_X_FORWARDED_FOR'];
} else {
	$ip =  $_SERVER['REMOTE_ADDR'];
}

$order['ip'] = isset($_POST['ip']) ? $_POST['ip'] : $_SERVER['REMOTE_ADDR'];

$parsed_referer = parse_url($_SERVER['HTTP_REFERER'], PHP_URL_QUERY);
parse_str($parsed_referer, $referer_query);

$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, "https://tracker.rocketprofit.com/conversion/new" );
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1 );
curl_setopt($ch, CURLOPT_POST,           1 );
curl_setopt($ch, CURLOPT_POSTFIELDS,     http_build_query(array_merge($referer_query, $order)) );
curl_setopt($ch, CURLOPT_HTTPHEADER,     array('Content-Type: application/x-www-form-urlencoded'));

$result=curl_exec ($ch);

$_POST['response'] = isset($result) ? $result : '';
$_POST['leadcreateAt'] = date('Y-m-d H:i:s', time());
file_put_contents('lead_logs.txt', print_r($_POST, true), FILE_APPEND);


if ($result === 0) {
	echo "Timeout! RocketProfit API didn't respond within default period!";
} else {
	$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
	if ($httpCode === 200) {
		header("Location: {success});
		echo "Good! Order accepted!";
	} else if ($httpCode === 400) {
		echo "Order data is invalid! Order is not accepted!";
	} else {
		echo "Unknown error happened! Order is not accepted! Check campaign_id, probably no landing exists for your campaign!";
	}
}
?>