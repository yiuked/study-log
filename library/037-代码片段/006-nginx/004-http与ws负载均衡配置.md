```
upstream eth_http_elb {  
   server 172.25.0.5:8545;  
   server 172.25.0.2:8545 ;  
}  
  
upstream eth_ws_elb {  
   server 172.25.0.5:8546;  
   server 172.25.0.2:8546 ;  
}  
  
map $http_upgrade $connection_upgrade {  
    default upgrade;  
    '' close;  
}  
  
server {  
   listen 9315;  
   location / {  
       proxy_set_header Host $host;  
       proxy_pass http://eth_http_elb;  
   }  
}  
  
server {  
   listen 9316;  
   location / {  
       proxy_set_header Host $host;  
       proxy_pass http://eth_ws_elb;  
       proxy_http_version 1.1;  
       proxy_set_header Upgrade $http_upgrade;  
       proxy_set_header Connection $connection_upgrade;  
   }  
}

stream {
	upstream aws_mysql {
		hash $remote_addr consistent;
		server 127.0.0.1:8523; 
	}
    
	server {
		listen 53306;
		proxy_pass aws_mysql;
	}
}


server {
	listen 8503 http2;
	location / {
		grpc_pass grpc://127.0.0.1:8502;
	}
}
```