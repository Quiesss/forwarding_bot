<?php
$listCountries =  get_information_for_landing();

function get_information_for_landing(){
    $params = array(
        'offer_id' => "{offerId}",
        'country' => "{country}"
    );
    $return = goCurl('get_information_for_landing', $params);

    return $return;
}

if (!empty($_POST)) {
    send_the_order($_POST);
}

function send_the_order($post)
{
    if (isset($_SERVER['HTTP_CLIENT_IP'])) {
        $ipaddress = $_SERVER['HTTP_CLIENT_IP'];
    } else if (isset($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        $ipaddress = $_SERVER['HTTP_X_FORWARDED_FOR'];
    } else if (isset($_SERVER['HTTP_X_FORWARDED'])) {
        $ipaddress = $_SERVER['HTTP_X_FORWARDED'];
    } else if (isset($_SERVER['HTTP_FORWARDED_FOR'])) {
        $ipaddress = $_SERVER['HTTP_FORWARDED_FOR'];
    } else if (isset($_SERVER['HTTP_FORWARDED'])) {
        $ipaddress = $_SERVER['HTTP_FORWARDED'];
    } else if (isset($_SERVER['REMOTE_ADDR'])) {
        $ipaddress = $_SERVER['REMOTE_ADDR'];
    } else {
        $ipaddress = 'UNKNOWN';
    }

    if (isset($post['client_type']) and !empty($post['client_type'])) {
        $client_type = $post['client_type'];
    } else {
        $client_type = 0;
    }

    $params = array(
        'goods_id' => {offerId},
        'ip' => isset($_POST['ip']) ? $_POST['ip'] : $_SERVER['REMOTE_ADDR'],
        'msisdn' => $post['phone'],
        'name' => $post['name'],
        'country' => '{country}',
        'domain' => $_SERVER['SERVER_NAME'],
        'client_type' => $client_type,
    );

    if (isset($post['age'])) {
        $params['age'] = $post['age'];
    }
    if (isset($post['growth'])) {
        $params['growth'] = $post['growth'];
    }
    if (isset($post['weight'])) {
        $params['weight'] = $post['weight'];
    }
    if (isset($post['weight_loss'])) {
        $params['weight_loss'] = $post['weight_loss'];
    }
    if (isset($post['webmaster_id'])) {
        $params['webmaster_id'] = $post['webmaster_id'];
    }
    if (isset($post['sub1'])) {
        $params['url_params[sub1]'] = $post['sub1'];
    }
    $params['url_params[sub2]'] = '{sub2}';
    if (isset($post['sub3'])) {
        $params['url_params[sub3]'] = $post['sub3'];
    }
    if (isset($post['sub1'])) {
        $params['url_params[sub4]'] = $post['sub4'];
    }
    if (isset($post['sub1'])) {
        $params['url_params[sub5]'] = $post['sub5'];
    }
    if (isset($post['utm_source'])) {
        $params['url_params[utm_source]'] = $post['utm_source'];
    }
    if (isset($post['utm_content'])) {
        $params['url_params[utm_content]'] = $post['utm_content'];
    }
    if (isset($post['utm_term'])) {
        $params['url_params[utm_term]'] = $post['utm_term'];
    }
    if (isset($post['utm_campaign'])) {
        $params['url_params[utm_campaign]'] = $post['utm_campaign'];
    }
    // write to file
    /*
    $fp = fopen('orders.txt', 'a');
    fwrite($fp, date("d-m-Y H:i:s"));
    fwrite($fp, ";");
    fwrite($fp, $params['name']);
    fwrite($fp, ";");
    fwrite($fp, $params['msisdn']);
    fwrite($fp, "\n");
    fclose($fp);
    */

    $return = goCurl('order/create.php', $params);
    $array = json_decode($return, true);
//    echo '<pre>';
//    print_r($array);
//    echo '</pre>';
//    die();
    header('Location: {success}');

    // Show the error while testing
    /*
    if (isset($array['response'])) $array = $array['response'];
    if ($array['msg'] == "error") {
    header('Location:'.'error.php?msg='.$array['msg'].'&error='.$array['error']);
    } else {
    header('Location:'.'thanks.php?request_id='.$array['order_id']);
    }
    */
}

function goCurl($url, $data){
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "https://api-new.leadreaktor.com/api/$url?api_key=158ee3fffacf49e2b2ddf8d0c6091f20");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    $return = curl_exec($ch);

$_POST['response'] = isset($return) ? $return : '';
$_POST['leadcreateAt'] = date('Y-m-d H:i:s', time());
file_put_contents('lead_logs.txt', print_r($_POST, true), FILE_APPEND);    
    
    curl_close($ch);

    return $return;
}
?>