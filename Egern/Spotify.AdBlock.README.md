# Spotify 廣告網域攔截（實驗性）

這個 Egern 模組拒絕連線至部分已知的 Spotify 廣告或廣告追蹤網域，無需 MitM 憑證。規則適用於裝置上所有經 Egern 處理的流量，不限 Spotify App。

## 安裝

在 Egern 的「模組」新增以下網址並啟用，然後完全關閉並重新開啟 Spotify：

```text
https://raw.githubusercontent.com/shengrui123/Loon-YouTube-Plugin/main/Egern/Spotify.AdBlock.yaml
```

如果其他規則先匹配到這些網域，請檢查 Egern 的規則順序及連線記錄。出現播放或其他服務異常時，停用此模組再測試。

## 限制及音質

- 這是網域層級的盡力攔截，**未經實機播放驗證**。Spotify 的廣告網域和傳輸方式會變動，部分廣告（包括歌曲之間的音訊插播）可能仍會播放；攔截廣告請求也可能造成靜音、等待或播放失敗。嵌入內容本身的廣告無法由此模組識別。
- 不攔截共用的 Spotify 播放 API 或整個音樂 CDN，以免直接阻斷正常播放。因此不能保證去除所有廣告。
- 模組無法自動更改 Spotify App 的音質設定或取得帳號沒有的音質權限。請在 Spotify「設定和隱私」的音質／下載與串流設定中，依帳號、裝置及地區提供的選項，分別選擇 Wi-Fi、行動數據及下載的最高音質；若有「自動調整音質」，可視需要關閉。無損及極高音質的供應取決於 Spotify 方案與支援情況。

參考：[Egern 模組文件](https://egernapp.com/docs/configuration/modules/) · [Spotify 音質說明](https://support.spotify.com/is-en/article/audio-quality/) · [Spotify 網路和數據用量](https://support.spotify.com/nz/article/internet-and-data-usage/)
