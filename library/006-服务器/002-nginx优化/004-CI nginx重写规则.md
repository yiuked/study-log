#### CI nginx重写规则
```
server {
 listen 80;
 server_name ttlsa.com www.ttlsa.com;
root /data/site/www.ttlsa.com;
 index index.php;
 error_log log/error.log;
# set expiration of assets to MAX for caching
 location ~* .(ico|css|js|gif|jpe?g|png)(?[0-9]+)?$ {
 expires max;
 log_not_found off;
 }
# main codeigniter rewrite rule
 location / {
 try_files $uri $uri/ /index.php;
 }
# php parsing
 location ~ .php$ {
 root /data/site/ttlsa.com/;
 try_files $uri =404;
 fastcgi_pass unix:/tmp/php5-fpm.sock; # 改成对应的FastCGI
 fastcgi_index index.php;
 fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
 include fastcgi_params;
 fastcgi_buffer_size 128k;
 fastcgi_buffers 256 4k;
 fastcgi_busy_buffers_size 256k;
 fastcgi_temp_file_write_size 256k;
 }
}
```
修改`CI(CodeIgniter )`配置文件`config.php`  
```
$config['base_url'] = "http://www.ttlsa.com/";
$config['index_page'] = "";
$config['uri_protocol'] = "REQUEST_URI";
```
