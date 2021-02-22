# Filebeat 详解

Filebeat是本地文件的日志数据采集器，可监控日志目录或特定日志文件（tail file），并将它们转发给Elasticsearch或Logstatsh进行索引、kafka等。带有内部模块（auditd，Apache，Nginx，System和MySQL），可通过一个指定命令来简化通用日志格式的收集，解析和可视化。

## 工作原理

Filebeat涉及两个组件：查找器prospector和采集器harvester，来读取文件(tail file)并将事件数据发送到指定的输出。

查找器prospector查找符合条件的文件，采集器harvester负责读取找到的文件内容发送到output。

## 配置

```

filebeat.inputs:
#　输入类型，支持 log\stdin\filestream
- type: log
  # 为true则表示当前输入成立
  enabled: true

  # 日志路径，不支持网络路径，只支持本地绝对路径.
  paths:
    - D:\wamp64\logs\*.log
    #- c:\programdata\elasticsearch\logs\*

  # 排除日志中特定的行，支持正则表达式
  #exclude_lines: ['^DBG']

  # 排除日志中特定的行，支持正则表达式
  #include_lines: ['^ERR', '^WARN']

  # 排除日志中特定的文件，支持正则表达式
  #exclude_files: ['.gz$']

  # 附加字段
  #fields:
  #  level: debug
  #  review: 1

  # 多行匹配
  # 开始匹配字符 
  # multiline.pattern: ^\[

  # 是否以开始匹配字符取反来结束匹配
  #multiline.negate: false
  #multiline.match: after

# ====== 模块 =========
filebeat.config.modules:
  # 模块配置文件
  path: ${path.config}/modules.d/*.yml

  # 配置文件自动重载时间
  #reload.period: 10s

# ====== Elasticsearch template setting ======

setup.template.settings:
  index.number_of_shards: 1
  #index.codec: best_compression
  #_source.enabled: false


# ===== 常规 ======

# The name of the shipper that publishes the network data. It can be used to group
# all the transactions sent by a single shipper in the web interface.
#name:

# The tags of the shipper are included in their own field with each
# transaction published.
#tags: ["service-X", "web-tier"]

# Optional fields that you can specify to add additional information to the
# output.
#fields:
#  env: staging

# ====== Dashboards =========
# These settings control loading the sample dashboards to the Kibana index. Loading
# the dashboards is disabled by default and can be enabled either by setting the
# options here or by using the `setup` command.
#setup.dashboards.enabled: false

# The URL from where to download the dashboards archive. By default this URL
# has a value which is computed based on the Beat name and version. For released
# versions, this URL points to the dashboard archive on the artifacts.elastic.co
# website.
#setup.dashboards.url:

# ========= Kibana ========

# Starting with Beats version 6.0.0, the dashboards are loaded via the Kibana API.
# This requires a Kibana endpoint configuration.
setup.kibana:

  # Kibana Host
  # Scheme and port can be left out and will be set to the default (http and 5601)
  # In case you specify and additional path, the scheme is required: http://localhost:5601/path
  # IPv6 addresses should always be defined as: https://[2001:db8::1]:5601
  #host: "localhost:5601"

  # Kibana Space ID
  # ID of the Kibana Space into which the dashboards should be loaded. By default,
  # the Default Space will be used.
  #space.id:

# ======== Elastic Cloud =======

# These settings simplify using Filebeat with the Elastic Cloud (https://cloud.elastic.co/).

# The cloud.id setting overwrites the `output.elasticsearch.hosts` and
# `setup.kibana.host` options.
# You can find the `cloud.id` in the Elastic Cloud web UI.
#cloud.id:

# The cloud.auth setting overwrites the `output.elasticsearch.username` and
# `output.elasticsearch.password` settings. The format is `<user>:<pass>`.
#cloud.auth:

# ========= Outputs ==========
# 日志输出，可选择输入到Elasticsearch或者Logstash

# -------- Elasticsearch Output -----------
#output.elasticsearch:
  # Array of hosts to connect to.
  #hosts: ["localhost:9200"]

  # Protocol - either `http` (default) or `https`.
  #protocol: "https"

  # Authentication credentials - either API key or username/password.
  #api_key: "id:api_key"
  #username: "elastic"
  #password: "changeme"

# --------- Logstash Output ----------
output.logstash:
  # The Logstash hosts
  hosts: ["localhost:5044"]

  # Optional SSL. By default is off.
  # List of root certificates for HTTPS server verifications
  #ssl.certificate_authorities: ["/etc/pki/root/ca.pem"]

  # Certificate for SSL client authentication
  #ssl.certificate: "/etc/pki/client/cert.pem"

  # Client Certificate Key
  #ssl.key: "/etc/pki/client/cert.key"

# ======== Processors =============
processors:
  - add_host_metadata:
      when.not.contains.tags: forwarded
  - add_cloud_metadata: ~
  - add_docker_metadata: ~
  - add_kubernetes_metadata: ~

# ============== Logging =================

# 日志级别，默认为info,可用日志类型有：error, warning, info, debug
#logging.level: debug

# 调试选择器，可以选择输出哪些组件的日志，使用 ["*"]表示输出所有日志，选择器有"beat""publish", "service"
#logging.selectors: ["*"]

# ========= X-Pack Monitoring =========
# Filebeat can export internal metrics to a central Elasticsearch monitoring
# cluster.  This requires xpack monitoring to be enabled in Elasticsearch.  The
# reporting is disabled by default.

# Set to true to enable the monitoring reporter.
#monitoring.enabled: false

# Sets the UUID of the Elasticsearch cluster under which monitoring data for this
# Filebeat instance will appear in the Stack Monitoring UI. If output.elasticsearch
# is enabled, the UUID is derived from the Elasticsearch cluster referenced by output.elasticsearch.
#monitoring.cluster_uuid:

# Uncomment to send the metrics to Elasticsearch. Most settings from the
# Elasticsearch output are accepted here as well.
# Note that the settings should point to your Elasticsearch *monitoring* cluster.
# Any setting that is not set is automatically inherited from the Elasticsearch
# output configuration, so if you have the Elasticsearch output configured such
# that it is pointing to your Elasticsearch monitoring cluster, you can simply
# uncomment the following line.
#monitoring.elasticsearch:

# ========== Instrumentation =========

# Instrumentation support for the filebeat.
#instrumentation:
    # Set to true to enable instrumentation of filebeat.
    #enabled: false

    # Environment in which filebeat is running on (eg: staging, production, etc.)
    #environment: ""

    # APM Server hosts to report instrumentation results to.
    #hosts:
    #  - http://localhost:8200

    # API Key for the APM Server(s).
    # If api_key is set then secret_token will be ignored.
    #api_key:

    # Secret token for the APM Server(s).
    #secret_token:


# ========== Migration =============

# This allows to enable 6.7 migration aliases
#migration.6_to_7.enabled: true

```

## 启动

```
./filebeat -e -c filebeat.yml -d "publish"
```



## 延伸

* logstash 无法收集filebeat中的全部日志

  > 删除 data/registry 与 data/registry.old，这两个文件记录了数据的偏移量

* 采集docker日志是报错

  ```
  2021-02-22T16:41:29.812+0800	INFO	[crawler]	beater/crawler.go:71	Loading Inputs: 3
  2021-02-22T16:41:29.812+0800	WARN	[cfgwarn]	docker/input.go:49	DEPRECATED: 'docker' input deprecated. Use 'container' input instead. Will be removed in version: 8.0.0
  ```

  > 从7.2.0版本开始，已取取消docker类型，可以使用以下格式采集
  >
  > ```
  > filebeat.inputs:
  > - type: container
  >   paths: 
  >     - '/var/lib/docker/containers/*/*.log'
  > ```
  >
  > 