# 代理组过滤维护方法论

本文用于沉淀 RuleMesh 在私有 Mihomo / Surge 配置中的代理组过滤维护约定，重点是避免把真实节点误判成“提示项”“占位项”后整批过滤掉。

## 典型风险

- 风险不是出在“提示项太多”，而是出在“把供应商名当成宽泛子串过滤”。
- 一旦某个 provider 开了统一前缀，例如把真实节点名改写成 `provider | 香港 01`，那么 `FlyintPro` 这类供应商名如果继续按“任意位置命中就过滤”处理，就会把整家机场的真实节点全部误杀。
- 这类错误最容易在扩充过滤词、复制正则到其他代理组、或者把一段过滤规则“统一收敛”时再次发生。

## 强制约束

- 状态/提示项按前缀匹配。
  - 例如：`剩余流量`、`套餐到期`、`距离下次重置`、`过滤掉`、`Expire Date`、`Traffic Reset`
- 独立占位项按全名精确匹配。
  - 例如：`直接连接`、`FlyintPro`
- 固定提示语按专项匹配。
  - 例如：`联系我们`
- 流量统计提示按数值模式匹配。
  - 例如：`1.2 GB | 50 GB`
- 只要某个 provider 或订阅聚合链路会给真实节点额外注入统一前缀，就严禁把供应商名写成宽泛子串过滤。

## 明确禁止

- 不要把 `FlyintPro` 写成 `.*FlyintPro.*`、`(?!.*FlyintPro)`、`|FlyintPro|` 这类“任意位置命中”的宽匹配。
- 不要因为想“一次性统一所有过滤词”，就把“状态项前缀匹配”和“供应商占位项精确匹配”重新揉回同一类写法。
- 不要只改一个客户端文件；Mihomo、Surge、公开示例、使用说明必须同步更新。

## 推荐写法

- Mihomo `exclude-filter`：

```yaml
exclude-filter: "(?i)^(剩余流量|套餐到期|距离下次重置|过滤掉|expire date|traffic reset)|^(直接连接|FlyintPro)$|联系我们|\\d+(?:\\.\\d+)?\\s*(?:[kmgt]b?|b)\\s*\\|\\s*\\d+(?:\\.\\d+)?\\s*(?:[kmgt]b?|b)"
```

- Surge `policy-regex-filter`：

```ini
policy-regex-filter=^(?!剩余流量)(?!(直接连接|FlyintPro)$)(?!套餐到期)(?!距离下次重置)(?!.*联系我们)(?!过滤掉)(?!Expire Date)(?!Traffic Reset)(?!.*\d+(?:\.\d+)?\s*(?:[KMGT]B?|B)\s*\|\s*\d+(?:\.\d+)?\s*(?:[KMGT]B?|B)).*$
```

## 每次修改前必须做的检查

1. 先确认相关 provider 是否带统一前缀，例如 `additional-prefix`。
2. 至少拿 1 条真实节点名做正例验证，例如 `provider | 香港 01` 应保留。
3. 至少拿 1 条独立占位项做反例验证，例如 `FlyintPro` 应过滤。
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

- 手动切换、自动组和地区组应尽量只展示真实节点。
- 过滤逻辑宁可多写几段显式约束，也不要为了“看起来更统一”退回到宽匹配。
- 只要看到“供应商名”和“统一前缀”同时出现，就默认先怀疑会不会误杀真实节点。
