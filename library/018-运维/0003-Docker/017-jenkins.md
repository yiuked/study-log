```console
docker run -p 8080:8080 -p 50000:50000 -v /your/home:/var/jenkins_home jenkins
```

```
  jenkins:
    image: jenkins:2.60.3
    container_name: jenkins
    ports:
      - 8080:8080
      - 50000:50000
    volumes:
      - ./jenkins:/var/jenkins_home
    privileged: true
    restart: always
```

```

password: 352727e690df4f598e431e75a9616569
```