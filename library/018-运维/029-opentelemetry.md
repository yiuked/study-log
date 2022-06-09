可观测性一个很重要的领域`Trace`有两个业界标杆: 一个是[OpenTracing](https://opentracing.io/)，另一个[OpenCensus](https://opencensus.io/)，OpenTracing其实是一个规范，jeager就是基于opentracing实现的开源工具，而OpenCensus则是由google开源的度量工具，简单来说，这两者在可观测性领域功能高度重合，因此，在CNCF主导下进行了合并形成opentelemetry项目，OpenTracing跟penCensus共同推进opentelemetry，两者的官网也赫赫表达基本不再维护，同时opentelemetry也致力于trace、logging、metrics间的关联性.

### OpenTelemetry核心工作

> -   1.规范的制定和协议的统一，规范包含数据传输、API的规范，协议的统一包含：HTTP W3C的标准支持及GRPC等框架的协议标准
> -   2.多语言SDK的实现和集成，用户可以使用SDK进行代码自动注入和手动埋点，同时对其他三方库（Log4j、LogBack等）进行集成支持
> -   3.数据收集系统的实现，当前是基于OpenCensus Service的收集系统，包括Agent和Collector。

由此可见，OpenTelemetry的自身定位很明确：数据采集和标准规范的统一，对于数据如何去使用、存储、展示、告警，官方是不涉及的

### OpenTelemetry状态

OpenTelemetry要解决的**是对可观测性的大一统**，它提供了一组API和SDK来标准化遥测数据的采集和传输，opentelemetry并不想对所有的组件都进行重写，而是最大程度复用目前业界在各大领域常用工具，通过提供了一个安全，厂商中立的能用协议、组件，这样就可以按照需要形成pipeline将数据发往不同的后端。

由于opentelemetry提出时间并不长，大家可以从[status](https://opentelemetry.io/status/)中可以看到最新的状态，可以看到，目前只有Tracing实现了1.0的release，而Metrics处于[feature-freeze](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/document-status.md#feature-freeze)，这个状态说的是metrics目前暂不接受在metrics中添加新的功能，以便技术委员会优先实现其它功能，还未达到stable状态，而在Logging则还处于草案阶段，opentelemetry官方的解释是日志相对存在体量大，延时高的问题，相对棘手且优先级对比另两者不高。

tracing已经在2021上半年实现了stable,目前官方给出的时间线是在2021下半年实现metrics的stable，在2022实现logging的stable.

为什么tracing是首先stable的，作者个人感觉可能是tracing目前在业界普及度还不够吧，而像metrics方面，prometheus早已成了业务标准

