#### 1.配置clone时展示的地址

```
vim /opt/gitlab/embedded/service/gitlab-rails/config/gitlab.yml
```

找到以下部分

```
  ## GitLab settings
  gitlab:
    ## Web server settings (note: host is the FQDN, do not include http://)
    host: example.com
    port: 8080
    https: false

```

修改后保存,并重启`gitlab`

```
gitlab-ctl restart
```

