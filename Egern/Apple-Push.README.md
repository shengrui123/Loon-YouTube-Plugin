# Apple Push — Egern 規則集

Apple Push Notification service（APNs）的 Egern 原生 YAML 規則集，涵蓋 `push.apple.com` 及其子網域，以及 Apple 公布的 APNs IPv4／IPv6 網段。網域後綴也涵蓋正式、測試及廣播 API。

- [Apple-Push.yaml](./Apple-Push.yaml)：使用 Apple 公布的較小 APNs 網段。
- [Apple-Push-Extended.yaml](./Apple-Push-Extended.yaml)：IPv4 使用 Apple 建議的完整 `17.0.0.0/8`，IPv6 使用 Apple 公布的 APNs 網段。完整 IPv4 網段也包含大量其他 Apple 服務，請依需要選用。

## 使用方式

在 Egern 的設定檔 `rules:` 中，將以下規則放在一般 Apple、地區及預設規則之前，並按需求把 `DIRECT` 改為已有的策略或策略組名稱：

```yaml
rules:
  - rule_set:
      match: https://raw.githubusercontent.com/shengrui123/Loon-YouTube-Plugin/main/Egern/Apple-Push.yaml
      policy: DIRECT
      update_interval: 86400
```

廣泛涵蓋版本的網址：

```text
https://raw.githubusercontent.com/shengrui123/Loon-YouTube-Plugin/main/Egern/Apple-Push-Extended.yaml
```

也可在 Egern 的工具 → 規則中新增遠端規則集，指定網址與策略。兩個版本擇一使用即可。Egern 依順序匹配，首次命中後即停止；其他更靠前的規則可能搶先匹配。規則集內各項為「或」的關係，IP 網段匹配不限連接埠，可能包含非推播流量。IP 規則可能觸發 DNS 解析；如自行加上 `no_resolve: true`，尚未解析的網域可能無法命中 IP 規則。

Apple 指出裝置與 APNs 通訊使用 TCP 5223，無法連接時可回退至 443；伺服器向 APNs 發送通知使用 TCP 443 或 2197。請確保網路與所選策略允許對應連線，且不要解密 APNs 連線。APNs 使用負載平衡，網段可能變動；較小網段不是對所有未來節點的保證。此規則集無法保證通知送達。

## 參考資料

- [Apple：裝置無法收到推播通知](https://support.apple.com/en-us/102266)
- [Apple：在企業網路上使用 Apple 產品](https://support.apple.com/en-us/101555)
- [Apple Developer：傳送通知要求至 APNs](https://developer.apple.com/documentation/usernotifications/sending-notification-requests-to-apns)
- [Egern：規則與規則集](https://egernapp.com/docs/configuration/rules/)
