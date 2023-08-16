<?php
const API_URL = "https://api.aray.com/api/v2/order/create/";
const API_KEY = "242387e913a5ad6c4b1b0c5c1e95ef86";
$isCurlEnabled = function(){
    return function_exists('curl_version');
};
if (!$isCurlEnabled) {
    echo "<pre>";
    echo "pls install curl\n";
    echo "For *unix open terminal and type this:\n";
    echo 'sudo apt-get install curl && apt-get install php-curl';
    die;
}
$args = [
    'api_key' => '242387e913a5ad6c4b1b0c5c1e95ef86',
    'name' => $_POST['name'],
    'phone' => $_POST['phone'],
    'offer_id' => {offerId}, //ID ОФФЕРА (ОБЯЗАТЕЛЬНО!!!)
    'country_code' => '{country}', //КОД СТРАНЫ ЗАГЛАВНЫМИ БУКВАМИ (ОБЯЗАТЕЛЬНО!!!)
    'price' => {price}, //ЦЕНА (ОБЯЗАТЕЛЬНО!!!)
    'base_url' => isset($_SERVER['HTTP_REFERER']) ? $_SERVER['HTTP_REFERER'] : $_SERVER['HTTP_HOST'],  //URL ОФФЕРА (ОБЯЗАТЕЛЬНО!!!)
    'ip' => isset($_POST['ip']) ? $_POST['ip'] : $_SERVER['REMOTE_ADDR'],
    'referrer' => isset($_SERVER['HTTP_REFERER']) ? $_SERVER['HTTP_REFERER'] : $_SERVER['HTTP_HOST'],
    'subacc' => $_POST['sub1'],
    'subacc2' => {sub2},
    'clickid' => $_POST['sub1'],
    'rotator_id' => {stream},
    ];
$url = API_URL.'?'.http_build_query($args);
$curl = curl_init();
curl_setopt_array($curl, array(
    CURLOPT_URL => $url,
    CURLOPT_RETURNTRANSFER => true
));
$res = curl_exec($curl);

// print_r($res);
// // exit();

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
