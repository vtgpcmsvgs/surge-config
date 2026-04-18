# 代理组过滤维护方法论

本文用于沉淀 RuleMesh 在私有 Mihomo / Surge 配置中的代理组过滤维护约定，重点是避免 Mihomo、Surge、公开示例与说明文档之间再次出现过滤口径漂移。

## 典型风险

- 风险不只在“提示项太多”，更在于不同客户端、不同代理组、不同文档各自维护一套过滤表达式，最后互相覆盖。
- 当前约定已经调整为：`直接连接` 与 `FlyintPro` 也按“任意位置命中即过滤”处理，不再保留旧的“独立占位项精确匹配”口径。
- 这类错误最容易在扩充过滤词、复制正则到其他代理组、或者只改 Mihomo / 只改 Surge 时再次发生。

## 强制约束

- 当前默认按任意位置命中即过滤。
  - 例如：`剩余流量`、`直接连接`、`FlyintPro`、`套餐到期`、`距离下次重置`、`联系我们`、`过滤掉`、`Expire Date`、`Traffic Reset`
- 流量统计提示继续按数值模式匹配。
  - 例如：`1.2 GB | 50 GB`
- Mihomo `exclude-filter` 与 Surge `policy-regex-filter` 必须保持语义等价，不能一边宽匹配、一边回退到旧的精确匹配。
- 如果未来要恢复保留带统一前缀的真实节点，必须先同时收窄 Mihomo / Surge 两侧表达式，再修改实际配置。

## 明确禁止

- 不要把 Mihomo、Surge、公开示例、README / usage 文档拆成不同口径维护。
- 不要只改一个代理组；手动切换、自动组、地区组必须一起改。
- 不要只改一个客户端文件；Mihomo、Surge、公开示例、使用说明必须同步更新。

## 推荐写法

- Mihomo `exclude-filter`：

```yaml
exclude-filter: "(?i)剩余流量|直接连接|FlyintPro|套餐到期|距离下次重置|联系我们|过滤掉|expire date|traffic reset|\\d+(?:\\.\\d+)?\\s*(?:[kmgt]b?|b)\\s*\\|\\s*\\d+(?:\\.\\d+)?\\s*(?:[kmgt]b?|b)"
```

- Surge `policy-regex-filter`：

```ini
policy-regex-filter=^(?!.*剩余流量)(?!.*直接连接)(?!.*FlyintPro)(?!.*套餐到期)(?!.*距离下次重置)(?!.*联系我们)(?!.*过滤掉)(?!.*Expire Date)(?!.*Traffic Reset)(?!.*\d+(?:\.\d+)?\s*(?:[KMGT]B?|B)\s*\|\s*\d+(?:\.\d+)?\s*(?:[KMGT]B?|B)).*$
```

## 每次修改前必须做的检查

1. 先确认相关 provider 是否带统一前缀，例如 `additional-prefix`。
2. 至少拿 1 条普通真实节点名做正例验证，例如 `日本 01` 应保留。
3. 至少拿 1 条包含供应商名的节点名做反例验证，例如 `FlyintPro 香港 01` 在当前约定下应过滤。
4. 至少拿 2 到 3 条状态提示做反例验证，例如 `剩余流量 88 GB`、`套餐到期 2026-05-01`、`Traffic Reset in 3 days` 应过滤。
5. 搜索全仓与私有目录同类过滤表达式，避免只修一处、另一处下次再覆盖回来。

## 同步范围

- `%USERPROFILE%\\Desktop\\rulemesh-local\\current\\rulemesh-substore-mihomo-clash-verge.yaml`
- `%USERPROFILE%\\Desktop\\rulemesh-local\\current\\rulemesh-substore-mihomo-clash-meta.yaml`
- `%USERPROFILE%\\Desktop\\rulemesh-local\\current\\rulemesh-substore-surge-personal.conf`
- `%USERPROFILE%\\Desktop\\rulemesh-local\\current\\rulemesh-substore-surge-work-whitelist.conf`
- `docs/examples/mihomo-public.yaml`
- `docs/examples/surge-public.conf`
- `docs/usage-mihomo.md`
- `docs/usage-surge.md`
- `README.md`

## 维护目标

- 当前优先级是“保持四份私有配置与公开示例完全同口径”，避免再出现客户端之间结果不一致。
- 手动切换、自动组和地区组应尽量只展示真实节点。
- 如果将来要重新保留带统一前缀的真实节点，必须把“同时收窄 Mihomo / Surge”当成一个任务整体处理。
