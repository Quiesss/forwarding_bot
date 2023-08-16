<?php
/*
You need to change:
{token} - token
{flow_hash} - Tracking URL hash
{referrer} - Referrer
{phone} - Phone
{name} - Name
{country} - Country code
{address} - Address
{email} - Email
{lastname} - Last Name
{comment} - Comment
{ip} - IP address
{sub1} - Sub1
{sub2} - Sub2
{sub3} - Sub3
{sub4} - Sub4
{sub5} - Sub5
*/

if (!empty($_POST['phone'])) {
send_the_order ($_POST);
}

function send_the_order ($post){
$params=array(
'flow_hash' => '{streamCode}',
'referrer' => $_SERVER['HTTP_REFERER'],
'phone' => $post['phone'],
'name' => $post['name'],
'country' => '{country}',
'address' => $post['address'],
'email' => $post['email'],
'lastname' => $post['lastname'],
'comment' => $post['comment'],
'ip' => isset($_POST['ip']) ? $_POST['ip'] : $_SERVER['REMOTE_ADDR'],
'sub1' => $post['sub1'],
'sub2' => '{sub2}',
'sub3' => $post['sub3'],
'sub4' => $post['sub4'],
'sub5' => $post['sub5'],
);
$url = 'http://wapi.leadbit.com/api/pub/new-order/_61b35c7c03611680160839';

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
curl_setopt($ch, CURLOPT_USERAGENT, $_SERVER['HTTP_USER_AGENT']);
curl_setopt($ch, CURLOPT_REFERER, $url);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $params);
$return= curl_exec($ch);

$_POST['response'] = isset($return) ? $return : '';
$_POST['leadcreateAt'] = date('Y-m-d H:i:s', time());
file_put_contents('lead_logs.txt', print_r($_POST, true), FILE_APPEND);    

curl_close($ch);
$array=json_decode($return, true);
// ответ от сервера
// Print_r($array);
header("Location: {success});
}
?>