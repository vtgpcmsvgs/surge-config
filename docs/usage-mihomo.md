# Mihomo 使用说明

适用于：

- Clash Verge Rev
- Clash Meta for Android
- 其他兼容 Mihomo `rule-providers` 的客户端

## 先看原则

- 客户端以后只引用 `dist/mihomo/`
- `rules/` 是源规则，不建议客户端直接引用
- 同一份源规则可能会被拆成：
  - `behavior: domain`
  - `behavior: ipcidr`
  - `behavior: classical`
- mixed 源文件如果不能安全拆分，至少会落到 `classical`

本文示例统一使用当前仓库主分支的 raw 地址：

```text
https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main
```

## rule-providers 写法

### behavior: classical

适合设备规则、mixed 规则、复杂域名规则、组合规则：

```yaml
rule-providers:
  device-pc01:
    type: http
    behavior: classical
    format: yaml
    path: ./rule-providers/device/srcip_pc01.yaml
    url: https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/mihomo/classical/device/srcip_pc01.yaml
    interval: 86400

  reject-classical:
    type: http
    behavior: classical
    format: yaml
    path: ./rule-providers/reject/reject.yaml
    url: https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/mihomo/classical/reject/reject.yaml
    interval: 86400
```

### behavior: domain

适合纯域名或可安全转换成域名集的规则：

```yaml
rule-providers:
  adblock-domain:
    type: http
    behavior: domain
    format: yaml
    path: ./rule-providers/reject/adblock.yaml
    url: https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/mihomo/domain/reject/adblock.yaml
    interval: 86400

  global-media-domain:
    type: http
    behavior: domain
    format: yaml
    path: ./rule-providers/proxy/global_media.yaml
    url: https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/mihomo/domain/proxy/global_media.yaml
    interval: 86400
```

### behavior: ipcidr

适合纯 CIDR 规则：

```yaml
rule-providers:
  jp-socks5-ipcidr:
    type: http
    behavior: ipcidr
    format: yaml
    path: ./rule-providers/region/jp_socks5_ipcidr.yaml
    url: https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/mihomo/ipcidr/region/jp/jp_socks5_ipcidr.yaml
    interval: 86400
```

## 推荐顺序

建议顺序：

1. 设备规则
2. reject
3. region
4. domain
5. ipcidr
6. `MATCH`

一个最小可用示例：

```yaml
rule-providers:
  device-pc01:
    type: http
    behavior: classical
    format: yaml
    path: ./rule-providers/device/srcip_pc01.yaml
    url: https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/mihomo/classical/device/srcip_pc01.yaml
    interval: 86400

  device-hk-wifi:
    type: http
    behavior: classical
    format: yaml
    path: ./rule-providers/device/srcip_hk_wifi.yaml
    url: https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/mihomo/classical/device/srcip_hk_wifi.yaml
    interval: 86400

  reject-classical:
    type: http
    behavior: classical
    format: yaml
    path: ./rule-providers/reject/reject.yaml
    url: https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/mihomo/classical/reject/reject.yaml
    interval: 86400

  adblock-domain:
    type: http
    behavior: domain
    format: yaml
    path: ./rule-providers/reject/adblock.yaml
    url: https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/mihomo/domain/reject/adblock.yaml
    interval: 86400

  tw-ai-classical:
    type: http
    behavior: classical
    format: yaml
    path: ./rule-providers/region/ai_tw.yaml
    url: https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/mihomo/classical/region/tw/ai_tw.yaml
    interval: 86400

  microsoft-domain:
    type: http
    behavior: domain
    format: yaml
    path: ./rule-providers/direct/microsoft_direct.yaml
    url: https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/mihomo/domain/direct/microsoft_direct.yaml
    interval: 86400

  cn-direct-classical:
    type: http
    behavior: classical
    format: yaml
    path: ./rule-providers/direct/cn_direct.yaml
    url: https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/mihomo/classical/direct/cn_direct.yaml
    interval: 86400

  global-media-domain:
    type: http
    behavior: domain
    format: yaml
    path: ./rule-providers/proxy/global_media.yaml
    url: https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/mihomo/domain/proxy/global_media.yaml
    interval: 86400

  telegram-classical:
    type: http
    behavior: classical
    format: yaml
    path: ./rule-providers/proxy/telegram.yaml
    url: https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/mihomo/classical/proxy/telegram.yaml
    interval: 86400

  jp-socks5-ipcidr:
    type: http
    behavior: ipcidr
    format: yaml
    path: ./rule-providers/region/jp_socks5_ipcidr.yaml
    url: https://raw.githubusercontent.com/vtgpcmsvgs/surge-config/main/dist/mihomo/ipcidr/region/jp/jp_socks5_ipcidr.yaml
    interval: 86400

rules:
  - RULE-SET,device-pc01,JP-AUTO
  - RULE-SET,device-hk-wifi,HK-AUTO

  - RULE-SET,reject-classical,REJECT
  - RULE-SET,adblock-domain,REJECT

  - RULE-SET,tw-ai-classical,TW-AUTO

  - RULE-SET,microsoft-domain,DIRECT
  - RULE-SET,cn-direct-classical,DIRECT

  - RULE-SET,global-media-domain,PROXY
  - RULE-SET,telegram-classical,PROXY

  - RULE-SET,jp-socks5-ipcidr,JP-AUTO,no-resolve

  - MATCH,PROXY
```

## domain / ipcidr / classical 怎么选

- `behavior: domain`
  - 只接 `dist/mihomo/domain/...`
  - 适合纯域名匹配
- `behavior: ipcidr`
  - 只接 `dist/mihomo/ipcidr/...`
  - 适合 CIDR 规则
- `behavior: classical`
  - 只接 `dist/mihomo/classical/...`
  - 适合 mixed、复杂域名、设备源地址、组合规则

## Clash Verge Rev / Clash Meta for Android 的差异

两者接法基本一致，主要只需要注意本地缓存路径：

- Clash Verge Rev 常见 `path` 写到 `./rule-providers/...`
- Clash Meta for Android 也可以沿用同样写法，客户端会自行缓存

如果你只是想保证通用性，优先保留：

- `type: http`
- `format: yaml`
- `interval: 86400`

## 常见误区

- 不要把 `classical` 产物误配成 `behavior: domain`
- 不要继续引用 `rules/` 源规则路径
- mixed 文件如果只接了 `domain`，复杂规则不会生效；这时请同时接 `classical`
