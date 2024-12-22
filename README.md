# WorkWeChat_NotifyAPI - 企业微信通知API

是一个简单的 Flask 应用，提供企业微信应用通知服务，通过 API 将消息推送到指定的企业微信用户。支持文本消息、图文消息以及 MPNews 类型消息的发送。

## 特性

- 通过 API 发送企业微信通知
- 支持文本消息、图文消息、MPNews 类型消息
- 配置灵活，可以根据不同 `num` 发送不同的消息配置
- 支持 `GET` 和 `POST` 请求方式

## 部署与配置

使用以下命令启动Docker：

```
docker run -d --name qywx_api \
  -e QYWX_SECRET_KEY=your_secret_key \
  -e QYWX_CORPID=your_corp_id \
  -e QYWX_AGENTID=your_agent_id \
  -e QYWX_SECRET=your_agent_secret \
  -p 5005:5005 \
  --restart=always \
  yin26287903/WorkWeChat_NotifyAPI  
```


- **QYWX_SECRET_KEY**: 自定义请求的验证密钥。
- **QYWX_CORPID**: 企业微信的 CorpID。
- **QYWX_AGENTID**: 企业微信的 AgentID。
- **QYWX_SECRET**: 企业微信的应用 Secret。

## API 说明

### `GET /wechat`

- 用于通过 URL 参数发送通知。

**请求示例**：

```
GET http://localhost:5005/wechat?num=1&msgtype=1&key=your_key&touser=your_user&title=通知标题&content=通知内容
```

**参数说明**：

- `num`: 选择通知配置的编号。
- `msgtype`: 消息类型，`1` 为文本消息，`2` 为图文消息，`3` 为 MPNews。
- `key`: 用于验证请求的密钥。
- `touser`: 接收通知的用户。
- `title`: 消息标题（可选）。
- `content`: 消息内容。
- `redirect_url`: 图文消息中的 URL（可选）。
- `picurl`: 图文消息中的图片 URL（可选）。
- `media_id`: MPNews 类型消息的媒体 ID（可选）。

### `POST /wechat`

- 用于通过 JSON 数据发送通知。

**请求示例**：

```json
{
  "num": 1,
  "msgtype": "1",
  "key": "your_key",
  "touser": "your_user",
  "title": "通知标题",
  "content": "通知内容",
  "redirect_url": "http://example.com",
  "picurl": "http://example.com/image.jpg",
  "media_id": "your_media_id"
}
```

**参数说明**与 `GET` 请求相同。