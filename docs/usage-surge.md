# Surge 使用说明

## 先看原则

- 客户端以后只引用 `dist/surge/`
- `rules/` 是源规则，不建议在 Surge 配置里直接引用
- `domainset/` 只放纯域名或可安全降级为域名集合的内容，适合 `DOMAIN-SET`
- `rules/` 放完整规则行，适合 `RULE-SET`
- 如果一个源文件是 mixed，请优先引用 `dist/surge/rules/...`

本文示例统一使用当前仓库主分支的 raw 地址：

```text
https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main
```

## DOMAIN-SET 示例

适合放在纯域名优先匹配的位置，例如广告、微软、国际流媒体：

```ini
DOMAIN-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/domainset/reject/adblock.list,REJECT
DOMAIN-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/domainset/direct/microsoft_direct.list,DIRECT
DOMAIN-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/domainset/proxy/global_media.list,PROXY
```

说明：

- `DOMAIN-SET` 只适合 `dist/surge/domainset/...`
- 不要把 `dist/surge/rules/...` 误当成 `DOMAIN-SET`

## RULE-SET 示例

适合 mixed 规则、IP 规则、设备源地址规则：

```ini
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/rules/device/srcip_pc01.list,JP-AUTO
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/rules/device/srcip_hk_wifi.list,HK-AUTO
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/rules/reject/reject.list,REJECT
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/rules/direct/cn_direct.list,DIRECT
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/rules/proxy/telegram.list,PROXY
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/rules/region/jp/jp_socks5_ipcidr.list,JP-AUTO,no-resolve
```

## 推荐顺序

建议顺序：

1. 设备规则
2. reject
3. region
4. direct / proxy 的 domain 规则
5. IP 规则
6. `FINAL`

一个最小可用的 `[Rule]` 片段可以写成：

```ini
[Rule]
# 1. device
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/rules/device/srcip_pc01.list,JP-AUTO
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/rules/device/srcip_pc02.list,JP-AUTO
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/rules/device/srcip_hk_wifi.list,HK-AUTO

# 2. reject
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/rules/reject/reject.list,REJECT
DOMAIN-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/domainset/reject/adblock.list,REJECT

# 3. region
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/rules/region/hk/domains_to_hk.list,HK-AUTO
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/rules/region/tw/ai_tw.list,TW-AUTO
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/rules/region/tw/crypto_tw.list,TW-AUTO
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/rules/region/tw/domains_to_tw.list,TW-AUTO
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/rules/region/jp/domains_to_jp.list,JP-AUTO

# 4. domain-first direct / proxy
DOMAIN-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/domainset/direct/microsoft_direct.list,DIRECT
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/rules/direct/cn_direct.list,DIRECT
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/rules/direct/direct.list,DIRECT
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/rules/proxy/google.list,PROXY
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/rules/proxy/telegram.list,PROXY
DOMAIN-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/domainset/proxy/global_media.list,PROXY

# 5. ip rules
RULE-SET,https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/surge/rules/region/jp/jp_socks5_ipcidr.list,JP-AUTO,no-resolve

# 6. final
FINAL,PROXY
```

## 什么时候用 domainset，什么时候用 rules

- 文件里大部分是 `DOMAIN` / `DOMAIN-SUFFIX` 时，可以优先用 `domainset`
- 文件里出现 `DOMAIN-KEYWORD`、`DOMAIN-WILDCARD`、`AND/OR`、`SRC-IP`、`GEOIP`、`IP-CIDR` 时，请用 `rules`
- mixed 文件就算构建出了 `domainset`，也通常应该保留 `rules` 作为完整兜底

## 常见误区

- 不要继续引用 `rules/reject/reject.list` 这类源文件路径
- 不要继续在客户端里直接引用 ACL4SSR / Loyalsoldier / blackmatrix7 的原始 URL
- `region/tw/google_tw` 这类历史源文件，在 `dist/` 里会变成带扩展名的产物路径
