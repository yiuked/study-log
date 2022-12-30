
```mermaid
graph LR
A[可观测性] --> B[检测 instrumented]-->C[信号]
    C --> D[追踪 traces]
    C --> E[指标 metrics]
    C --> F[日志 logs]
    C --> G[上下文 Baggage]
    D --> D1[日志]
    D --> D2[Span]
```

围绕着平台的可观测性，催生了一系列开源用于观测的平台，如 ([Jaeger](https://www.jaegertracing.io/) 和 [Zipkin](https://zipkin.io/)),可每个平台对于数据的采集规则并不一样。于是为了统一业界标准，Opentelemtry(OTel)诞生了。
需要强调的是OpenTelemetry 不是像 Jaeger 或 Prometheus 那样提供可观察性的后端。相反，它支持将数据导出到各种开源和商业后端。它提供了一个可插入的架构，因此可以轻松添加额外的技术协议和格式。

```mermaid
graph LR
A[OpenTelemetry组成]
    A --> D[跨语言规范]
    A --> E[采集器]
    A --> F[每种语言的SDK]
    A --> G[每种语言的检测库]
    A --> H[每种语言的自动化检测]
    A --> I[K8S集成]
    E --> E1[可以接收处理以及导出监测数据]
```

#### 采集器
![[Pasted image 20221228173158.png]]

```mermaid
graph LR
A[应用]
    A --> B0[OTEL-SDK] --> B[OpenTelemetry Collector]
    A --> B1[Jeager-SDK]
    A --> B2[Zipkin-SDK]
    A --> B3[Jeager-agent]
    A --> B4[Zipkin-agent]
    B1 --> B
    B2 --> B
    B --> C1[OTLP]
    B --> C2[Jeager UI]
    B --> C3[Prometheus UI]
	B3 --> C2[Jeager UI]
	B4 --> C4[Zipkin UI]
	
```

```
                                          -----> Jaeger (trace)
App + SDK ---> OpenTelemetry Collector ---|
                                          -----> Prometheus (metrics)
```