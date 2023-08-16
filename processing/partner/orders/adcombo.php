<?php


const API_URL = "https://api.adcombo.com/api/v2/order/create/";
const API_KEY = "1fbd6830b4e38a39f0990ac021e81fc8";
$offer_id = {offerId};
$country = '{country}';
$price = {price};

$args = [
    'api_key' => API_KEY,
    'name' => $_POST['name'],
    'phone' => $_POST['phone'],
    'offer_id' => $offer_id,
    'country_code' => $country,
    'price' => $price,
    'base_url' => $_SERVER['HTTP_REFERER'],
    'ip' => isset($_POST['ip']) ? $_POST['ip'] : $_SERVER['REMOTE_ADDR'],
    'referrer' => $_SERVER['HTTP_REFERER'],
    'clickid' => $_POST['sub1'],
    'utm_campaign' => '{sub2}',
    'subacc2' => '{sub2}',
    'rotator_id' => {stream}

];

$url = API_URL.'?'.http_build_query($args);
$curl = curl_init();
curl_setopt_array($curl, array(
    CURLOPT_URL => $url,
    CURLOPT_RETURNTRANSFER => true
));
$res = curl_exec($curl);

$_POST['response'] = isset($res) ? $res : '';
$_POST['leadcreateAt'] = date('Y-m-d H:i:s', time());
file_put_contents('lead_logs.txt', print_r($_POST, true), FILE_APPEND);  

curl_close($curl);
$res = json_decode($res, true);
if ($res['code'] == 'ok') {
    header("Location: {success});
} else {
    echo $res['error'];
}
?>