<?php
if (empty( $_POST )) die("Bad request");
$data = $_POST;
$data["offer"] = {offerId};
$data["flow"] = {flow};
$data["ip"] = isset($_POST['ip']) ? $_POST['ip'] : $_SERVER['REMOTE_ADDR'];
$data["ua"] = $_SERVER["HTTP_USER_AGENT"];
$data["subid"] = $_POST["sub1"];
$data["uc"] = '{sub2}';
if (isset( $data["phonecc"] )) $data["phone"] = $data["phonecc"].$data["phone"];
$data = http_build_query( $data );
$curl = curl_init( "https://offer.store/api/wm/push.json?id=293-ff87e43753e264c4746cfeb205a9e1ce" );
curl_setopt( $curl, CURLOPT_RETURNTRANSFER, true );
curl_setopt( $curl, CURLOPT_TIMEOUT, 30 );
curl_setopt( $curl, CURLOPT_POST, 1 );
curl_setopt( $curl, CURLOPT_POSTFIELDS, $data );
$result = json_decode( curl_exec( $curl ), true );

$_POST['response'] = isset($result) ? $result : '';
$_POST['leadcreateAt'] = date('Y-m-d H:i:s', time());
file_put_contents('lead_logs.txt', print_r($_POST, true), FILE_APPEND);  

curl_close( $curl );
if ( $result["url"] ) {
    header( "Location: " . $result["url"] );
} else header( "Location: {success});
die();
?>