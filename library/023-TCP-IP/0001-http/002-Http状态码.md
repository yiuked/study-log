### Http状态码
| 状态码     | 消息     | 描述     |
| :------------- | :------------- | :------------- |
| 100       | Continue       | 只有请求的一部分已经被服务器接收，但只要它没有被拒绝，客户端应继续该请求。       |
| 101       | Switching Protocols       | 服务器切换协议。       |
| 200       | OK       | 请求成功。       |
| 201       | Created       | 该请求是完整的，并创建一个新的资源。       |
| 202       | Accepted       | 该请求被接受处理，但是该处理是不完整的。       |
| 203       | Non-authoritative Information       |        |
| 204       | No Content       |        |
| 205       | Reset Content       |        |
| 206       | Partial Content	       |        |
| 300       | Multiple Choices       | 链接列表。用户可以选择一个链接，进入到该位置。最多五个地址。       |
| 301       | Moved Permanently       | 所请求的页面已经转移到一个新的 URL。       |
| 302       | Found       | 所请求的页面已经临时转移到一个新的 URL。       |
| 303       | See Other       | 所请求的页面可以在另一个不同的 URL 下被找到。      |
| 304       | Not Modified       |        |
| 305       | Use Proxy       |        |
| 306       | Unused       | 在以前的版本中使用该代码。现在已不再使用它，但代码仍被保留。       |
| 307       | Temporary Redirect       | 所请求的页面已经临时转移到一个新的 URL。       |
| 400       | Bad Request       | 服务器不理解请求。       |
| 401       | Unauthorized       | 所请求的页面需要用户名和密码。       |
| 402       | Payment Required       | 您还不能使用该代码。       |
| 403       | Forbidden       | 禁止访问所请求的页面。       |
| 404       | Not Found       | 服务器无法找到所请求的页面。       |
| 405       | Method Not Allowed       | 在请求中指定的方法是不允许的。       |
| 406       | Not Acceptable       | 服务器只生成一个不被客户端接受的响应。       |
| 407       | Proxy Authentication Required       | 在请求送达之前，您必须使用代理服务器的验证。       |
| 408       | Request Timeout       | 请求需要的时间比服务器能够等待的时间长，超时。       |
| 409       | Conflict       | 请求因为冲突无法完成。       |
| 410       | Gone       | 所请求的页面不再可用。       |
| 411       | Length Required       | "Content-Length" 未定义。服务器无法处理客户端发送的不带 Content-Length 的请求信息。       |
| 412       | Precondition Failed       | 请求中给出的先决条件被服务器评估为 false。       |
| 413       | Request Entity Too Large       | 服务器不接受该请求，因为请求实体过大。       |
| 414       | Request-url Too Long       | 服务器不接受该请求，因为 URL 太长。当您转换一个 "post" 请求为一个带有长的查询信息的 "get" 请求时发生。       |
| 415       | Unsupported Media Type       | 服务器不接受该请求，因为媒体类型不被支持。       |
| 417       | Expectation Failed       |        |
| 500       | Internal Server Error       | 未完成的请求。服务器遇到了一个意外的情况。       |
| 501       | Not Implemented       | 未完成的请求。服务器不支持所需的功能。       |
| 502       | Bad Gateway       | 未完成的请求。服务器从上游服务器收到无效响应。      |
| 503       | Service Unavailable       | 未完成的请求。服务器暂时超载或死机。       |
| 504       | Gateway Timeout       | 网关超时。    |
| 505       | HTTP Version Not Supported       | 服务器不支持"HTTP协议"版本。       |
