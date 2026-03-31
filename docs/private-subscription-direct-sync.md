# 私有订阅域名同步约定

本文只记录本地私有“订阅域名同步块”的维护方式，避免后续把真实订阅域名重新散落回多个配置文件，或误写进公开仓库。

## 适用范围

- `%USERPROFILE%\Desktop\rulemesh-local\current\private_subscription_direct.list`
- `%USERPROFILE%\Desktop\rulemesh-local\current\sync_private_subscription_direct.ps1`
- `%USERPROFILE%\Desktop\rulemesh-local\current\rulemesh-substore-surge-personal.conf`
- `%USERPROFILE%\Desktop\rulemesh-local\current\rulemesh-substore-surge-work-whitelist.conf`
- `%USERPROFILE%\Desktop\rulemesh-local\current\rulemesh-substore-mihomo-clash-verge.yaml`
- `%USERPROFILE%\Desktop\rulemesh-local\current\rulemesh-substore-mihomo-clash-meta.yaml`

## 设计目标

- 真实机场订阅更新域名只在私有目录维护，不回写公开仓库
- 由单一源文件统一维护，避免 `Surge personal`、`Surge work whitelist`、`Mihomo Clash Verge`、`Mihomo Clash Meta` 四处重复手改
- 同一组规则同时服务 Surge 与 Mihomo，因此源文件只写双方都支持的规则语法
- Chrome 浏览器访问这些域名时仍可先走 `🚀 节点选择`，不再被订阅更新直连误伤
- 整个同步块必须位于 `proxy/gfw` 前；其中 Chrome 例外在前，订阅更新直连在后；在工作白名单里则属于显式放行入口

## 源文件写法

- `private_subscription_direct.list` 每行只写规则本体，不要附带 `,DIRECT`
- 允许空行与中文注释
- 优先使用 `DOMAIN`、`DOMAIN-SUFFIX`、`DOMAIN-WILDCARD` 这类 Surge / Mihomo 都能直接复用的语法
- 如果某条规则只被单一客户端支持，不要写进这份共享源文件

## 同步方式

1. 修改 `private_subscription_direct.list`
2. 运行 `powershell -ExecutionPolicy Bypass -File "%USERPROFILE%\Desktop\rulemesh-local\current\sync_private_subscription_direct.ps1"`
3. 脚本会自动刷新四份本地私有配置中的“Chrome 访问节点选择例外 + 订阅更新直连”规则块
4. 如需人工确认，可检查四份目标文件中的 `PRIVATE_SUBSCRIPTION_DIRECT_START` 与 `PRIVATE_SUBSCRIPTION_DIRECT_END` 标记段

## 编码防回滚提醒

- 这条链路的真实故障案例是：在 `sync_private_subscription_direct.ps1` 里直接写入中文或 emoji 策略组名字面量后，Windows PowerShell 5.1 可能把 UTF-8 无 BOM 的脚本按本地代码页误读，最终把 `🚀 节点选择` 之类的策略组名写成乱码
- 乱码一旦进入 Mihomo / Surge 私有配置，典型症状就是重新载入时报 `proxy not found`；报错通常出现在新插入的 `PROCESS-NAME + DOMAIN-*` 规则，而同文件原本已有的 `proxy_onepassword`、`onepassword_proxy.list` 或 `proxy_gfw` 规则仍然正常
- 因此，后续维护 `sync_private_subscription_direct.ps1` 时，优先保持脚本源码 ASCII-only；如果需要引用带中文或 emoji 的策略组名，不要直接硬编码，优先从目标配置中提取现有值后再写回
- 修改同步脚本后，至少人工抽查一次四份目标文件中的新增规则：新写入的策略组名必须与同文件里已有的 `proxy_onepassword` / `onepassword_proxy.list` / `proxy_gfw` 行完全一致，不能出现乱码

## 维护边界

- 不要把真实订阅域名写进 `rules/`、`dist/`、`README.md`、公开模板或公开规则文档
- 不要把这组私有订阅域名同步规则合并进公开 `direct/*.list`、`proxy/gfw.*` 或其他面向所有用户的规则入口
- 如果未来某条规则只影响单一客户端而非全部三份配置，先评估它是否还适合继续放在共享源文件里
- 如果同步脚本、目标文件名或插入顺序发生变化，需同步更新本文以及相关使用说明
