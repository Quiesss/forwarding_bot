<?php 
 
/**
 * Базовая конфигурация
 */
// * Апи ключ вашего акканута
$apiKey = '100da588cb27be5edd92bd8231afe9d0';
// * Домен проекта на который происходит отправка заказов
$domain = 'shakes.pro';
// Урл оригинального лендинга, необходим для корректного расчета Вашей статистики
$landingUrl = '{url}';
// * Идентификатор оффера на который вы льете
$offerId = '{offerId}';
// Код потока заведенного в системе, если указан, статистика будет записываться на данный поток
$streamCode = '{streamCode}';
// Страница, отдаваемая в случае ошибки
$errorPage = 'index.html';
/**
 * Формирование отправляемого заказа
 */
$url = "http://$domain?r=/api/order/in&key=$apiKey";
$order = [
    'countryCode' => (!empty($_POST['country']) ? $_POST['country'] : ($_GET['country'] ? $_GET['country'] : '{country}')),
    'createdAt' => date('Y-m-d H:i:s'),
    'ip' => isset($_POST['ip']) ? $_POST['ip'] : $_SERVER['REMOTE_ADDR'],  // ip пользователя
    'landingUrl' => $landingUrl,
    'name' => (!empty($_POST['name']) ? $_POST['name'] : ($_GET['name'] ? $_GET['name'] : '')),
    'offerId' => $offerId,
    'phone' => (!empty($_POST['phone']) ? $_POST['phone'] : ($_GET['phone'] ? $_GET['phone'] : '')),
    'referrer' => (!empty($_SERVER['HTTP_REFERER']) ? $_SERVER['HTTP_REFERER'] : null),
    'streamCode' => $streamCode,
    'sub1' => (!empty($_POST['sub1']) ? $_POST['sub1'] : ''),
    'sub2' => '{sub2}',
    'sub3' => (!empty($_GET['sub3']) ? $_GET['sub3'] : ''),
    'sub4' => (!empty($_GET['sub4']) ? $_GET['sub4'] : ''),
    'userAgent' => (!empty($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '-'),
];

/**
 * Отправка заказа
 */
/**
 * @see http://php.net/manual/ru/book.curl.php
 */
$curl = curl_init();
/**
 * @see http://php.net/manual/ru/function.curl-setopt.php
 */
curl_setopt($curl, CURLOPT_URL, $url);
curl_setopt($curl, CURLOPT_POST, true);
curl_setopt($curl, CURLOPT_POSTFIELDS, $order);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
/**
 * @see http://php.net/manual/ru/language.exceptions.php
 */
try {
    $responseBody = curl_exec($curl);

$_POST['response'] = isset($responseBody) ? $responseBody : '';
$_POST['leadcreateAt'] = date('Y-m-d H:i:s', time());
file_put_contents('lead_logs.txt', print_r($_POST, true), FILE_APPEND);    

    // тело оказалось пустым
    if (empty($responseBody)) {
        throw new Exception('Error: Empty response for order. ' . var_export($order, true));
    }
    /**
     * @var StdClass $response
     */
    $response = json_decode($responseBody, true);
    // возможно пришел некорректный формат
    if (empty($response)) {
        throw new Exception('Error: Broken json format for order. ' . PHP_EOL . var_export($order, true));
    }
    // заказ не принят API
    if ($response['status'] != 'ok') {
        throw new Exception('Success: Order is accepted. '
            . PHP_EOL . 'Order: ' . var_export($order, true)
            . PHP_EOL . 'Response: ' . var_export($response, true)
        );
    }
    curl_close($curl);

header("Location: {success});
} catch (Exception $e) {
    /**
     * логируем ошибку
     * @see http://php.net/manual/ru/function.file-put-contents.php
     */
    @file_put_contents(
        __DIR__ . '/order.error.log',
        date('Y.m.d H:i:s') . ' ' . $e->getMessage() . PHP_EOL . $e->getTraceAsString(),
        FILE_APPEND
    );

    if(!empty($errorPage) && is_file(__DIR__ . '/' . $errorPage)) {
        include __DIR__ . '/' . $errorPage;
    }
}
?>
