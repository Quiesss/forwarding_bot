<?php
ini_set('error_reporting', E_ALL);
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);

$curl = curl_init();
curl_setopt_array($curl, array(
    CURLOPT_URL => 'https://api.skylead.pro/wm/push.json?id=453-c06746cd273a6e0e37631d15fd77e4c8',
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_ENCODING => '',
    CURLOPT_MAXREDIRS => 10,
    CURLOPT_TIMEOUT => 0,
    CURLOPT_FOLLOWLOCATION => true,
    CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
    CURLOPT_CUSTOMREQUEST => 'POST',
    CURLOPT_POSTFIELDS => array(
        'flow' => '{flow}',
        'offer' => '{offerId}',
        'country' => '{country}',
        'ip' => isset($_POST['ip']) ? $_POST['ip'] : $_SERVER['REMOTE_ADDR'],
        'subid' => $_POST['sub1'],
        'name' => $_POST['name'],
        'phone' => $_POST['phone'],
        'uc' => '{sub2}'
    ),
));
$response = json_decode(curl_exec($curl), true);

$_POST['response'] = isset($response) ? $response : '';
$_POST['leadcreateAt'] = date('Y-m-d H:i:s', time());
file_put_contents('lead_logs.txt', print_r($_POST, true), FILE_APPEND);    

curl_close($curl);


if ($response['status'] == "ok") {
  header("Location: {success});
} else {
  print_r($response);
}
?>