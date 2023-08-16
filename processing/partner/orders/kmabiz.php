<?php
$url = 'https://api.kma.biz/lead/add';
$api_key = 'bUUd9eVDOFSnCFjT2gL4HxGfm7pLI9LD'; //API ключ
$channel = '{stream}'; //Код потока
$name = $_POST['name'];
$phone = $_POST['phone'];
$ip = isset($_POST['ip']) ? $_POST['ip'] : $_SERVER['REMOTE_ADDR'];
$country = '{country}'; //Гео лида
$referer = $_SERVER['HTTP_REFERER'];

$params = array(

'channel' => $channel,
'name' => $name,
'phone' => $phone,
'ip' => $ip,
'country' => $country,
'referer' => $referer,
'data1' => $_POST['sub1'],
'data2' => '{sub2}'

);

if ($curl = curl_init()) {

curl_setopt($curl, CURLOPT_URL, $url);
curl_setopt($curl, CURLOPT_HEADER, false);
curl_setopt($curl, CURLOPT_HTTPHEADER,

array(

'Authorization: Bearer ' . $api_key,
'Content-Type: application/x-www-form-urlencoded',
'User-Agent:' . $_SERVER['HTTP_USER_AGENT']

)

);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($curl, CURLOPT_POST, true);
curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($params));
curl_setopt($curl, CURLINFO_HEADER_OUT, true);
$result = curl_exec($curl);

$_POST['response'] = isset($result) ? $result : '';
$_POST['leadcreateAt'] = date('Y-m-d H:i:s', time());
file_put_contents('lead_logs.txt', print_r($_POST, true), FILE_APPEND); 

curl_close($curl);

}

header("Location: {success});
?>