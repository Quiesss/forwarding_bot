<?php
const THANKS_URL = 'success.php'; // ссылка на страницу "спасибо"
// const FLOW_TOKEN = 'flow'; // ТОКЕН ПОТОКА
const CLIENT_TOKEN = 'ZGE1NZU4ZMETMDGYNI00MMU1LTGXYTQTMGJMYZHKYWY2NGVL'; // ТОКЕН КЛИЕНТА (получается в настройках ПП)

if (isset($_POST['name']) && $_POST['phone'] != '') {
    $post = [
            // "stream_code" => FLOW_TOKEN,
            "stream_code" => '{flow}',
            
			"client" => [
				'name' => $_POST['name'],
				'phone' => $_POST['phone'],
			],
			'sub1' => $_POST["sub1"],
			'sub2' => '{sub2}',
			'sub3' => $_POST["sub3"],
			'sub4' => $_POST["sub4"],
			'sub5' => $_POST["sub5"]
    ];
    // отправляем заявку
    $ch = curl_init('https://affiliate.drcash.sh/v1/order');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($post));
    curl_setopt( $ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json', 'Authorization: Bearer '.CLIENT_TOKEN));
    $response = json_decode(curl_exec($ch));

$_POST['response'] = isset($response) ? $response : '';
$_POST['leadcreateAt'] = date('Y-m-d H:i:s', time());
file_put_contents('lead_logs.txt', print_r($_POST, true), FILE_APPEND);        

    print_r($response);
    curl_close($ch);
    if (isset($response->uuid)) {
        header("Location: {success}); // редирект
        exit;
    }
} else {
    //header('Location: /'); // редирект
}
?>