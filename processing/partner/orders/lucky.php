<?php

define('TOKEN', '{apikey}');
define('CAMPAIGN_HASH', '{stream}');

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $ip = isset($_POST['ip']) ? $_POST['ip'] : $_SERVER['REMOTE_ADDR'];
    $name = $_POST['name'];
    $phone = $_POST['phone'];
    $userAgent = $_SERVER['HTTP_USER_AGENT'];
    $utm_source = $_POST['utm_source'];
    $utm_content = $_POST['utm_content'];
    $utm_campaign = $_POST['utm_campaign'];
    $utm_term = $_POST['utm_term'];
    $utm_medium = $_POST['utm_medium'];
    $subid = $_POST['sub1'];
    $subid1 = '{sub2}';
    $subid2 = $_POST['subid2'];
    $subid3 = $_POST['subid3'];
    $country = '{country}';

    $data = [
        'campaign_hash' => CAMPAIGN_HASH,
        'ip' => $ip,
        'name' => $name,
        'phone' => $phone,
        'user_agent' => $userAgent,
        'country' => $country,
        'subid'=> $subid,
        'subid1'=> $subid1,
        'subid2'=> $subid2,
        'subid3'=> $subid3,
        'utm_source' =>$utm_source,
        'utm_content' =>$utm_content,
        'utm_campaign' =>$utm_campaign,
        'utm_term' =>$utm_term,
        'utm_medium' =>$utm_medium

    ];

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'https://lucky.online/api/v1/lead-create/webmaster?api_key=' . TOKEN);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    $response = curl_exec($ch);

    $body = json_decode($response, true);

    //если ошибка создания лида, то раскоментить строчку НИЖЕ,сохранить этот файл,  отправить еще раз лид и посмотреть ошибку почему сервер не принимает заказ
    //var_dump($body);exit;

    $date = date("Y-m-d H:i:s");
    $message = $body['response']['status'] == 'success' ? "click_id: {$body['response']['content']['click_id']}" : $body['response']['message'];
    $string = "Date: {$date}, name: {$name}, phone: {$phone}, ip: {$ip}, hash: " . CAMPAIGN_HASH . ", status: {$body['response']['status']}, message: {$message}" . PHP_EOL;
    file_put_contents('./log.txt', $string, FILE_APPEND);

    //блок отправки лида в ПП
    if ($body['response']['status'] == 'success') {
        header("Location: {success});
        exit();
    } else {
        echo $body['response']['message'];;
        exit();
    }
}

?>
