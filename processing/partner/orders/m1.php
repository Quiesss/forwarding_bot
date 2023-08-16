<?php

$url = 'http://m1.top/send_order/';
$data = [
'ref' => 818636,
'api_key' => 'ff16fe1fdecb6c7d94fb9ceef5578a83',
'product_id' => {offerId},
'phone' => $_REQUEST['phone'],
'name' => $_REQUEST['name'],
'ip' => isset($_POST['ip']) ? $_POST['ip'] : $_SERVER['REMOTE_ADDR'],
's' => $_POST['sub1'],
'w' => '{sub2}',
't' => 'test_t',
'p' => 'test_p',
'm' => 'test_m'
];

/** 
 * Язык лендинга (для бурж лендингов)
 * 
 * Указывается для того, чтобы все заказы, независимо от IP юзера приходили на ГЕО,
 * связанное с лендом.
 * 
 * Пример: $data['langCode'] = 'es';
 * 
 * Таким образом, даже если пользователь зайдет на лендинг с российского IP,
 * и у оффера есть при этом RU ГЕО, то заказ все равно уйдет на Испанию (ES)
 */
$data['langCode'] = '{country}';

$process = curl_init();
curl_setopt($process, CURLOPT_HEADER, 0);
curl_setopt($process, CURLOPT_USERAGENT, "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0)");
curl_setopt($process, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($process, CURLOPT_FOLLOWLOCATION, 0);
curl_setopt($process, CURLOPT_TIMEOUT, 20);
curl_setopt($process, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($process, CURLOPT_POST, true);
curl_setopt($process, CURLOPT_POSTFIELDS, $data);
curl_setopt($process, CURLOPT_URL, $url);

echo $return = curl_exec($process);


$_POST['response'] = isset($return) ? $return : '';
$_POST['leadcreateAt'] = date('Y-m-d H:i:s', time());
file_put_contents('lead_logs.txt', print_r($_POST, true), FILE_APPEND);

curl_close($process);
if (json_decode($return, true)['result'] == 'ok') {
  header("Location: {success});
}
?>