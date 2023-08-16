<?php

function getIp()
{
    if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
        $ip = $_SERVER['HTTP_CLIENT_IP'];
    } elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        $arIp = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR']);
        $ip = $arIp[0];
    } else {
        $ip = $_SERVER['REMOTE_ADDR'];
    }
    return $ip;
}

function apiWebvorkV1NewLead($post, $ip, $offerId, $counter = 0)
{
    $token = '3d9a72293e276cb36b363637af03f09b'; // Заменяем на свой из кабинета

    $url = 'http://api.webvork.com/v1/new-lead?token=' . rawurlencode($token)
        . '&ip=' . rawurlencode(isset($_POST['ip']) ? $_POST['ip'] : $_SERVER['REMOTE_ADDR'])
        . '&offer_id=' . rawurlencode($offerId)
        . '&name=' . rawurlencode($post['name'])
        . '&phone=' . rawurlencode($post['phone'])
        . '&country=' . '{country}'
        . '&utm_medium=' . {rawurlencode($post['sub1'])}
        . '&utm_campaign=' . '{sub2}'
        . '&utm_content=' . rawurlencode($post['utm_content'])
        . '&utm_term=' . rawurlencode($post['utm_term']);


    $json = file_get_contents($url);
    $data = json_decode($json, 1);


$_POST['response'] = isset($data) ? $data : '';
$_POST['leadcreateAt'] = date('Y-m-d H:i:s', time());
file_put_contents('lead_logs.txt', print_r($_POST, true), FILE_APPEND); 

    if ($data['status'] != 'ok') {
        if ($counter < 5) {
            sleep(1);
            return apiWebvorkV1NewLead($post, $ip, $offerId, ++$counter);
        } else {
            return false;
        }
    }

    if ($data['status'] == 'ok') {
        return true;
    }
}

apiWebvorkV1NewLead($_POST, getIp(), {offerId});// offerId Заменяем на оффер лендинга

header("Location: {success});
?>
