```
docker run \
  -u root \
  --rm \
  -d \
  -p 7001:8080 \
  -p 7002:50000 \
  -v jenkins-data:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkinsci/blueocean
```

