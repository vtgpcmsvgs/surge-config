# GitHub 仓库 SSH 定向直连规则

这组规则用于把 GitHub 仓库 SSH 连接单独放到直连，同时保留 GitHub 网页、Raw 内容与其他 GitHub 站点流量继续走代理。

当前源规则文件：`rules/direct/github_ssh_direct.list`

匹配范围只有两条：

- `github.com:22`
- `ssh.github.com:443`

这样可以覆盖两种常见场景：

- 标准 SSH remote：`git@github.com:owner/repo.git`
- 显式启用 SSH over 443：通过 `ssh.github.com:443` 连接

## 为什么要放在 `proxy/gfw` 前

上游 `proxy/gfw` 当前已经包含 `.github.com` 与 `.githubusercontent.com`。

如果把 GitHub SSH 定向直连规则放在 `proxy/gfw` 后面，`github.com:22` 会先命中广谱代理规则，后面的直连规则就不会再生效。

因此客户端接入时应使用下面顺序：

1. 拒绝规则
2. 区域精确规则
3. `direct/github_ssh_direct`
4. 其他更细的专项 carve-out，例如 `direct/adspower_direct`、`proxy/adspower_proxy`、`proxy/polygon_rpc_proxy`
5. `proxy/gfw`
6. 其他普通 `direct/*`
7. IP 规则
8. 最终兜底

## 产物链接

Surge：

- `https://raw.githubusercontent.com/vtgpcmsvgs/rulemesh/main/dist/surge/rules/direct/github_ssh_direct.list`

Mihomo / Clash Verge Rev：

- `https://raw.githubusercontent.com/vtgpcmsvgs/rulemesh/main/dist/mihomo/classical/direct/github_ssh_direct.yaml`

## 示例

Surge：

```ini
# 必须放在 proxy/gfw.list 前；中间仍可继续插入 AdsPower / Polygon RPC 等更细专项规则
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/rulemesh/main/dist/surge/rules/direct/github_ssh_direct.list,DIRECT
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/rulemesh/main/dist/surge/rules/proxy/gfw.list,"🚀 节点选择"
```

Mihomo / Clash Verge Rev：

```yaml
rule-providers:
  direct_github_ssh:
    type: http
    behavior: classical
    format: yaml
    path: ./rule-providers/direct/github_ssh_direct.yaml
    url: https://raw.githubusercontent.com/vtgpcmsvgs/rulemesh/main/dist/mihomo/classical/direct/github_ssh_direct.yaml
    interval: 86400

rules:
  # 必须放在 proxy_gfw 前；中间仍可继续插入 AdsPower / Polygon RPC 等更细专项规则
  - RULE-SET,direct_github_ssh,DIRECT
  - RULE-SET,proxy_gfw,🚀 节点选择
```
