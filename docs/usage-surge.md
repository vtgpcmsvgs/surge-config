# Surge 使用说明

## 推荐入口

- 完整公开参考模板：[`docs/examples/surge-public.conf`](examples/surge-public.conf)
- 规则产物入口：`dist/surge/rules/`

这个模板是基于本地长期使用的 Surge 配置整理出来的公开版，保留了总开关、区域自动切换、拒绝规则、直连规则与 IP 规则的完整结构，但移除了不适合公开仓库的个人化部分。

## 模板保留了什么

- 总开关 + 手动切换 + 自动测速切换
- 香港、台湾、日本、新加坡、美国、韩国的区域自动组
- `reject`、`direct`、`proxy`、`region` 四类 RuleMesh 产物接入
- `skip-proxy`、`always-real-ip`、基础 DNS 与测速参数

## 模板刻意移除了什么

- 按局域网源 IP 的设备分流（`SRC-IP` + `AND/OR`）
- 私有 `policy-path` 地址与真实机场命名
- 整个 `[MITM]` 段及证书参数

## 使用前只需要替换两处

1. 把模板里所有 `https://example.com/subs/surge/all?target=Surge` 替换成你自己的 Surge 聚合订阅入口。
2. 如果你不希望最终兜底走总开关，可以把 `FINAL,🚀 节点选择` 改成你想固定兜底的区域组。

## 规则顺序建议

1. 拒绝规则
2. 区域精确规则
3. 代理优先规则
4. 直连规则
5. IP 规则
6. `FINAL`

注意：

- `region/tw/google_tw.list` 必须放在 `region/hk/global_media.list` 等广谱区域规则前。
- `proxy/gfw.list` 建议放在 `direct/cn_direct.list` 前，减少广谱直连误伤。
- 浏览器明文 HTTP 拦截推荐直接接 `plain_http_reject.list`，不要再手写重复规则。

## 使用原则

- 客户端只引用 `dist/surge/rules/`
- `rules/` 是源规则层，不建议在 Surge 配置中直接引用
- 不要在客户端继续引用第三方原始规则 URL
- 不要手改 `dist/`，应先改 `rules/` 后重新构建
