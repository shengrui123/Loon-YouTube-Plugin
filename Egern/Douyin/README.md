# 抖音資訊流廣告過濾 · Egern

在 Egern 中添加模組：

https://raw.githubusercontent.com/shengrui123/Loon-YouTube-Plugin/main/Egern/Douyin/Douyin.Feed.Egern.yaml

啟用模組與 HTTPS 解密，安裝並完全信任 Egern 的 MITM CA 證書，然後重新啟動抖音。模組會自動下載同目錄的腳本。避免與其他修改相同資訊流回應的模組同時啟用。

本模組處理列出的 `amemv.com` 和 `aweme.snssdk.com` 上 feed、follow/feed、nearby/feed 介面的 JSON 回應，移除頂層 `aweme_list` 中 `is_ads` 或 `is_ad` 明確為 true、1 或「1」的影片。它是在資料送到播放器前過濾，不控制手機自動上滑。普通影片、沒有明確標記的商業內容、直播、開屏廣告及其他介面不在保證範圍；非 JSON、超過 10 MiB、加密或未經 MITM 的回應不處理。服務端介面可能隨時改變。

已用模擬回應測試過濾、正常資料保留、大整數 ID、異常回應及網址匹配；尚未在實際抖音與 Egern 裝置上驗證，因此不能保證目前版本有效。如無效果，請先確認日誌中的請求域名、路徑和回應格式；不要分享帳號、Cookie 或完整私人回應。

Egern 規範：[模組](https://egernapp.com/docs/configuration/modules/)、[腳本](https://egernapp.com/docs/configuration/scriptings/)、[JavaScript API](https://egernapp.com/docs/javascript-api/)。
