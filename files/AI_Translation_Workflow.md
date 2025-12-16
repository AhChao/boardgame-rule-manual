# AI Agent 規則翻譯與開發流程 (Workflow)

本文檔說明 AI Agent 如何將遊戲規則手冊 (PDF/Text) 轉換為行動裝置友善的繁體中文網頁應用程式 (Web App) 的標準作業程序 (SOP)。

## 1. 資料獲取與前處理 (Ingestion & Pre-processing)

一切始於原始檔案。

*   **輸入來源**：PDF 規則書 (如 `Secret_Hitler_Rules.pdf`) 或純文字檔。
*   **工具**：Python 腳本 (使用 `pypdf` 庫)。
*   **動作**：
    1.  撰寫 Python 腳本 (`extract_rules.py`)。
    2.  執行腳本並將 PDF 內容逐頁提取為純文字格式 (`raw_rules.txt`)。
    3.  **目的**：讓 AI 能夠以純文字形式完整閱讀並理解長篇規則，不受 PDF 排版干擾。

## 2. 理解與翻譯 (Comprehension & Translation)

AI 閱讀提取出的純文字後，進行以下認知處理：

*   **語意理解**：分析遊戲的核心機制、勝利條件、角色能力及遊戲階段。
*   **術語對照**：建立關鍵字的繁體中文對照表 (例如：Liberal -> 自由派, Fascist -> 法西斯, Policy -> 法案)。
*   **翻譯策略**：採用意譯而非逐字翻譯，確保語句通順並符合中文桌遊玩家的習慣用語。

## 3. 結構化與網頁開發 (Structuring & Development)

將翻譯後的文本直接轉換為互動式網頁。

*   **技術堆疊**：HTML5 + CSS3 + Vanilla JavaScript (單一檔案，無需後端)。
*   **Mobile-First 設計**：
    *   **卡片式佈局 (Cards)**：將規則分段放入卡片容器，便於手機閱讀。
    *   **色彩系統**：根據遊戲主題定義 CSS 變數 (例如：`--red-team`, `--blue-team`)。
*   **導航系統**：
    *   實作**浮動導航欄 (Floating Nav)**，確保長篇規則中能快速跳轉。
    *   利用 `IntersectionObserver` 實作**滾動監聽**，自動標示當前閱讀章節。

## 4. 功能增強 (Feature Implementation)

針對數位閱讀體驗加入紙本無法提供的功能：

*   **搜尋功能**：為角色或技能建立專屬查詢頁面 (如 `characters.html`)，支援中英文關鍵字搜尋。
*   **遊戲輔助工具**：製作互動式速查表 (Cheat Sheet) 或遊戲配置建議，例如根據玩家人數篩選的設置表。

## 5. 多專案整合 (Multi-Project Integration)

當有多個規則書專案時，建立統一入口：

*   **中央樞紐 (Central Hub)**：在根目錄建立 `index.html`，作為所有桌遊規則的索引頁 (Index Page)。
*   **雙向導航**：
    *   **Hub -> Rules**：樞紐頁提供卡片式連結前往各遊戲規則。
    *   **Rules -> Hub**：每個規則書的 Header 必須包含「🏠 返回首頁」連結，確保使用者能隨時回到索引。

## 6. 驗證與迭代 (Verification & Iteration)

*   **瀏覽器代理測試 (Browser Subagent)**：AI 啟動內建瀏覽器，模擬真實使用者行為 (點擊、滾動、輸入搜尋)。
*   **視覺確認**：檢查 CSS 樣式是否跑版，顏色是否正確。
*   **修正**：根據測試結果即時修正代碼 (如調整表格樣式、修復連結錯誤)。

---

## 總結 (Summary)

這個流程將靜態的 PDF 文件轉化為「活」的數位應用：

1.  **PDF** (原始資料)
2.  ⬇️ **Python Extraction** (純文字化)
3.  ⬇️ **AI Processing** (翻譯/理解/設計)
4.  ⬇️ **HTML/CSS/JS** (互動網頁)
5.  ✅ **Web Rulebook** (最終產出)
