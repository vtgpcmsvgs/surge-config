# 阿里云香港 IPv4 规则

这组规则仿照 AWS 区域 IPv4 规则链路实现，但数据源改为阿里云官方 VPC OpenAPI：

- 官方接口：`DescribePublicIpAddress`
- 官方文档：<https://help.aliyun.com/zh/eip/developer-reference/api-vpc-2016-04-28-describepublicipaddress-eips>
- 香港地域：`cn-hongkong`
- 区域 Endpoint：`vpc.cn-hongkong.aliyuncs.com`

同步链路如下：

1. `.github/workflows/sync-upstream-rules.yml` 每日运行 `tools/sync_upstream_rules.py`
2. `tools/sync_upstream_rules.py` 使用阿里云官方 OpenAPI 拉取 `cn-hongkong` 的公网 IPv4 前缀
3. 快照写入 `rules/upstream/alicloud/hk_ipv4.txt` 与 `rules/upstream/alicloud/hk_ipv4.json`
4. `rules/region/hk/alicloud_ipv4.list` 只保留单一 `INCLUDE`
5. `tools/build_rules.py` 统一生成 `dist/surge/rules/` 与 `dist/mihomo/classical/`

## 首次启用

阿里云这条链路和 AWS 不同，不能匿名下载，首次同步需要可用凭证。

本仓库工作流现在固定引用 GitHub Environment `upstream-sync`。

请在 GitHub 仓库后台进入：

`Settings -> Environments -> upstream-sync -> Environment secrets`

然后添加这些 secret：

- `RULEMESH_ALICLOUD_ACCESS_KEY_ID`
- `RULEMESH_ALICLOUD_ACCESS_KEY_SECRET`
- `RULEMESH_ALICLOUD_SECURITY_TOKEN`（可选，使用 STS 时再配）

推荐给一个只读 RAM 用户或 STS 临时凭证，具备 `DescribePublicIpAddress` 对应读取权限即可。

如果你愿意用 GitHub Environment 的保护规则，可以继续给 `upstream-sync` 加 `required reviewers`，这样工作流在真正拿到这些 secret 前还会过一层审批。

## 可直接使用的链接

Surge：

- 香港：`https://raw.githubusercontent.com/vtgpcmsvgs/rulemesh/main/dist/surge/rules/region/hk/alicloud_ipv4.list`

Mihomo / Clash Verge Rev：

- 香港：`https://raw.githubusercontent.com/vtgpcmsvgs/rulemesh/main/dist/mihomo/classical/region/hk/alicloud_ipv4.yaml`

## 示例

Surge：

```ini
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/rulemesh/main/dist/surge/rules/region/hk/alicloud_ipv4.list,HK-AUTO,no-resolve
```

Mihomo / Clash Verge Rev：

```yaml
rule-providers:
  alicloud-hk-classical:
    type: http
    behavior: classical
    format: yaml
    path: ./rule-providers/region/alicloud_hk_ipv4.yaml
    url: https://raw.githubusercontent.com/vtgpcmsvgs/rulemesh/main/dist/mihomo/classical/region/hk/alicloud_ipv4.yaml
    interval: 86400

rules:
  - RULE-SET,alicloud-hk-classical,HK-AUTO,no-resolve
```
