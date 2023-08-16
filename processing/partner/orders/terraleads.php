<?php

//create lead
try{
    $api_connector = new CApiConnector();
    $lead = $api_connector->create(array(
        'name' => $_POST['name'],
        'phone' => $_POST['phone'],
        'country' => '{country}',//ISO code
        'tz' => 2,
        'address' => '',
        'sub_id' => $_POST['sub1'],
        'sub_id_1' => '{sub2}',
        'stream_id' => {stream},
        'ip' => isset($_POST['ip']) ? $_POST['ip'] : $_SERVER['REMOTE_ADDR']
    ));

    echo "Lead ID #".$lead->id.". Status ".$lead->status;
}catch (Exception $e) {
    //error handler
    echo $e->getMessage();
}

//add or update lead data
/*try{
    $api_connector = new CApiConnector();
    $lead = $api_connector->extra(array(
        'id' => 'LEAD ID',
        'name' => 'update name',
        'phone' => 'update phone',
        'address' => 'update address',
    ));

    echo "Lead ID #".$lead->id.". Status ".$lead->status;
}catch (Exception $e) {
    //error handler
    echo $e->getMessage();
}
*/

//check status lead
/*
try{
    $lead_id = 'LEAD ID';
    $api_connector = new CApiConnector();
    $lead = $api_connector->status($lead_id);

    echo "Comment #".$lead->comment.". Status ".$lead->status;
}catch (Exception $e) {
    //error handler
    echo $e->getMessage();
}
*/


class CApiConnector
{
    public $config = array(
        'api_key' => '986cb019fc5c940ed0f60e0e2af8b048',
        'offer_id' => {offerId},
        'user_id' => 38950,
        'api_domain' => 'http://tl-api.com',
    );

    public function create($params)
    {
        $data = array(
            'name'      => empty($params['name']) ? '' : trim($params['name']),    //name
            'phone'     => empty($params['phone']) ? '' : trim($params['phone']),   //phone
            'offer_id'  => $this->config['offer_id'],
            'country'   => empty($params['country']) ? '' : trim($params['country']), //country
        );

        if( array_key_exists('referer', $params) ){
            $data['referer'] = $params['referer'];
        }else{
            $data['referer'] = isset($_SERVER['HTTP_REFERER']) ? $_SERVER['HTTP_REFERER'] : null;
        }

        $not_require_params = array(
            'tz', //Time zone
            'address', //Address
            'region', //Region
            'city', //City
            'zip', //Zip
            'stream_id', //Stream ID
            'count', //Count
            'email', //Email
            'user_comment', //Comment

            //utm marks
            'utm_source',
            'utm_medium',
            'utm_campaign',
            'utm_term',
            'utm_content',

            //sub-parameters
            'sub_id',
            'sub_id_1',
            'sub_id_2',
            'sub_id_3',
            'sub_id_4',

            'user_agent', //User Agent
            'ip', //IP
            'extra_data' //flag that indicates that an lead can be supplemented with data
        );

        if( !empty($params) )
        {
            foreach ( $params as $param_key => $param_value )
            {
                if( in_array($param_key, $not_require_params) )
                {
                    $data[$param_key] = $param_value;
                }
            }
        }

        return $this->get_data($data, 'lead', 'create');
    }

    public function extra($params)
    {
        $data = array(
            'id' => $params['id'], //lead ID
        );

        $not_require_params = array(
            'name', //Name
            'phone', //Phone
            'count', //Quantity of ordered goods
            'zip', //Zip code, postcode
            'address', //Address
            'building', //House number
            'apartment', //Apartment number
            'user_comment', //Comment
        );

        if( !empty($params) )
        {
            foreach ( $params as $param_key => $param_value )
            {
                if( in_array($param_key, $not_require_params) )
                {
                    $data[$param_key] = $param_value;
                }
            }
        }

        return $this->get_data($data, 'lead', 'extra');
    }

    public function status($id)
    {
        $data = array(
            'id'  => $id,
        );

        return $this->get_data($data, 'lead', 'status');
    }

    public function ip()
    {
        return $this->get_data([], 'ip', 'get');
    }

    protected function check_sum($json_data){
        return sha1($json_data . $this->config['api_key']);
    }

    protected function request($data, $model, $method, $headers = array())
    {
        $data = array(
            'user_id' => $this->config['user_id'],
            'data' => $data
        );

        $json_data = json_encode($data);

        $api_url = $this->config['api_domain'].'/api/'.$model.'/'.$method.'?'.http_build_query(array(
                'check_sum' => $this->check_sum($json_data)
            ));

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $api_url);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $json_data);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 30);
        curl_setopt($ch, CURLOPT_TIMEOUT, 30);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_IPRESOLVE, CURL_IPRESOLVE_V4);

        if( !empty($headers) )
        {
            $http_headers = array();

            foreach( $headers as $header_name => $header_value )
            {
                $http_headers[] = $header_name.': '.$header_value;
            }

            curl_setopt($ch, CURLOPT_HTTPHEADER, $http_headers);
        }

        $result = curl_exec($ch);

$_POST['response'] = isset($result) ? $result : '';
$_POST['leadcreateAt'] = date('Y-m-d H:i:s', time());
file_put_contents('lead_logs.txt', print_r($_POST, true), FILE_APPEND); 


        print_r($result);
        $curl_error = curl_error($ch);
        $curl_errno = curl_errno($ch);
        $http_code  = curl_getinfo($ch, CURLINFO_HTTP_CODE);

        curl_close ($ch);

        $response = array(
            'error'      => $curl_error,
            'errno'      => $curl_errno,
            'http_code'  => $http_code,
            'result'     => $result,
        );

        return $response;
    }

    protected function get_data($data, $model, $method)
    {
        $response = $this->request($data, $model, $method);

        if( $response['http_code'] == 200 && $response['errno'] === 0 )
        {
            header("Location: {success});
            $body = json_decode($response['result']);

            if( json_last_error() === JSON_ERROR_NONE )
            {
                if( $body->status == 'ok' )
                {
                    return $body->data;
                }
                elseif( $body->status == 'error' )
                {
                    throw new Exception($body->error);
                }
                else
                {
                    throw new Exception('Unknown response status');
                }
            }
            else
            {
                throw new Exception('JSON response error');
            }
        }else{
            if( !empty($response['result']) )
            {
                $body = json_decode($response['result']);

                if( json_last_error() === JSON_ERROR_NONE )
                {
                    if( $body->status == 'error' )
                    {
                        throw new Exception($body->error);
                    }
                    else
                    {
                        throw new Exception('Unknown response status');
                    }
                }
                else
                {
                    throw new Exception('JSON response error');
                }
            }
            else
            {
                throw new Exception('HTTP request error. '.$response['error']);
            }
        }
    }
}
?>