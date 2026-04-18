# 代理组过滤维护方法论

本文用于沉淀 RuleMesh 在私有 Mihomo / Surge 配置中的代理组过滤维护约定。本文故意写得啰嗦，因为 `FlyintPro` 过滤已经发生过多次真实回归事故，不能再靠“默认会记得”这种口头约定维持。

## 先说结论

- `剩余流量`、`套餐到期`、`距离下次重置`、`过滤掉`、`Expire Date`、`Traffic Reset` 这类状态/提示项，继续按前缀匹配过滤。
- `直接连接` 与 `FlyintPro` 这类独立占位项，必须按“整行精确匹配”过滤，不能按任意位置命中过滤。
- `联系我们` 继续按专项子串匹配。
- `1.2 GB | 50 GB` 这类流量统计提示，继续按数值模式匹配。

## FlyintPro 防回滚红线

- `flyintpro` provider 已知会给真实节点追加统一前缀，例如：`flyintpro | 日本 01`、`flyintpro | 香港 02`。
- 因此，只要把 `FlyintPro` 写成宽匹配，例如 `.*FlyintPro.*`、`(?!.*FlyintPro)`、`|FlyintPro|`、普通子串 `FlyintPro`，就会把整家机场的真实节点全部误杀。
- 这不是理论推演，而是已经发生过多次真实事故。以后看到有人说“把过滤词统一收敛一下”“把 FlyintPro 也并进宽匹配里”“保持和其他提示词一个风格”，默认先判定为高风险改动。

## 必须保留的正确写法

- Mihomo `exclude-filter`：

```yaml
exclude-filter: "(?i)^(剩余流量|套餐到期|距离下次重置|过滤掉|expire date|traffic reset)|^(直接连接|FlyintPro)$|联系我们|\\d+(?:\\.\\d+)?\\s*(?:[kmgt]b?|b)\\s*\\|\\s*\\d+(?:\\.\\d+)?\\s*(?:[kmgt]b?|b)"
```

- Surge `policy-regex-filter`：

```ini
policy-regex-filter=^(?!剩余流量)(?!(直接连接|FlyintPro|flyintpro)$)(?!套餐到期)(?!距离下次重置)(?!.*联系我们)(?!过滤掉)(?!Expire Date)(?!Traffic Reset)(?!.*\d+(?:\.\d+)?\s*(?:[KMGT]B?|B)\s*\|\s*\d+(?:\.\d+)?\s*(?:[KMGT]B?|B)).*$
```

## 明确禁止的错误写法

- 不要把 Mihomo 写成：

```yaml
exclude-filter: "(?i)剩余流量|直接连接|FlyintPro|套餐到期|距离下次重置|..."
```

- 不要把 Surge 写成：

```ini
policy-regex-filter=^(?!.*剩余流量)(?!.*直接连接)(?!.*FlyintPro)...
```

- 上面两种写法都会把 `flyintpro | 日本 01` 这种真实节点误当成提示词过滤掉。

## 修改时必须做的正反例验证

1. 先确认相关 provider 是否存在统一前缀，例如 `additional-prefix: "flyintpro | "`。
2. 至少拿 1 条真实节点名做正例验证，例如 `flyintpro | 日本 01` 必须保留。
3. 至少拿 1 条独立占位项做反例验证，例如单独一条 `FlyintPro` 必须过滤。
4. 至少拿 2 到 3 条状态提示做反例验证，例如 `剩余流量 88 GB`、`套餐到期 2026-05-01`、`Traffic Reset in 3 days` 必须过滤。
5. 搜索全仓与私有目录里的同类表达式，避免只修一处、下一次又被别的文件覆盖回去。

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

## 执行顺序

1. 先改 4 份私有配置里的实际过滤表达式。
2. 再改公开示例，避免文档继续教错。
3. 再改 `README.md`、`docs/usage-surge.md`、`docs/usage-mihomo.md` 与本文。
4. 最后搜索全仓与私有目录确认没有 `宽匹配 FlyintPro` 残留。

## 维护目标

- 手动切换、自动组和地区组应尽量只展示真实节点。
- `FlyintPro` 的维护目标不是“和其他过滤词看起来统一”，而是“绝不误杀 flyintpro 真实节点”。
- 只要 `additional-prefix` 和 `FlyintPro` 过滤同时出现，就把它当成防回滚检查项，而不是普通样式调整。
