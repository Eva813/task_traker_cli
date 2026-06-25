---
name: commit-skill
description: 產生符合團隊規範的 Git commit 訊息。當使用者說「幫我寫 commit」、「commit 訊息」、「這次改了什麼幫我下 commit」、「產生 commit message」、「git commit」，或貼上 diff / 變更說明要求整理成 commit 時，立即使用此 skill。會根據變更性質自動選擇正確的 prefix（fix / hotfix / update / merge / beta / sync），並遵循 1～2 句為主、過多項目才分行的格式規則。
---

# Commit Skill

## 第一步：取得變更內容

使用者若未提供 diff 或變更描述，**主動執行以下指令**，不要等使用者提供：

```bash
git diff --staged
```

若結果為空，改執行：

```bash
git diff HEAD
```

再搭配以下指令確認整體狀態：

```bash
git status
```

根據取得的內容判斷變更範圍，再進入 prefix 選擇與格式輸出。

---

## Prefix 選擇

| Prefix | 用途 |
|--------|------|
| `fix` | 修 bug、修正錯誤行為、修正顯示異常 |
| `hotfix` | 緊急修補、線上事故 |
| `update` | 功能新增、UI 調整、重構、元件抽取、文件更新（**預設選項**） |
| `merge` | 合併分支 |
| `beta` | 版本封板、測試版里程碑 |
| `sync` | 環境設定、版本同步、依賴對齊 |

判斷順序：修 bug → `fix`，緊急 → `hotfix`，合併 → `merge`，版本封板 → `beta`，其餘 → `update`。

---

## 格式規則

**主訊息：1～2 句，英文，imperative mood（動詞開頭）**

```
[prefix] <動詞> <做了什麼>
```

**多個獨立變更才分行**，用 `and` 或換行 + 逗號分隔，避免每個小改動都開一行：

```
[update] extract PieChart and BarChart into local components, add resize observer cleanup on unmount
```

若項目真的很多（3 項以上且難以一句說清），才使用以下格式：

```
[update] refactor CarDetail chart components

- extract PieChart.vue and BarChart.vue as local components
- add D3 lifecycle cleanup to prevent memory leaks
- align axis label style with design spec
```

---

## 輸出規則

1. **直接給訊息**，不加解釋、不問確認（除非資訊嚴重不足）
2. 若使用者提供 diff 或變更描述，自行判斷 prefix 和摘要
3. 若有多個合理版本（例如一個簡潔、一個詳細），可給 2 個讓使用者選，但不要超過 2 個
4. 語言：**commit 訊息本身永遠用英文**；跟使用者的對話用繁體中文

---

## 範例

```
[fix] check customer type before calling corp data when page is 'promote'
[fix] correct card alignment in SalesAccidence.vue
[update] add insurance category filter and update chart data transform logic
[update] extract shared composable for date range and apply to customer/salesperson pages
[update] add warning icon display condition, apply hover expand on line-bar chart dots, and bump version
[sync] align quasar version with staging environment config
[beta] seal v3.0.0 release with full insurance product type support
```