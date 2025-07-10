# Jewellery Choices 珠寶網站

## 網站功能簡介

- 商品前台（products.html）：

  - 雲端自動同步商品資料與圖片
  - 支援搜尋、分類、款式篩選
  - 商品詳情可瀏覽多張圖片
  - 響應式設計，手機、平板、桌面皆適用

- 商品管理後台（admin.html）：

  - 線上新增、修改、刪除商品
  - 多圖上傳、預覽與刪除
  - 所有操作即時同步雲端
  - 入口：請至聯絡頁（contact.html）最下方右側小圓形按鈕

- 完全前端化，無需伺服器，支援 GitHub Pages 部署
- 商品資料與圖片皆儲存於 Supabase 雲端

## 🛠️ 功能說明

### 前台（products.html）

- 商品自動從 Supabase 讀取，無需手動維護 json/xlsx
- 支援「名稱、類別、款式、描述」即時搜尋
- 點擊商品可瀏覽多圖詳情

### 後台（admin.html）

- 進入方式：請至聯絡頁（contact.html）最下方右側小圓形按鈕
- 商品管理：新增、修改、刪除、圖片多圖上傳與預覽
- 所有操作即時同步 Supabase 雲端

---

## 📁 專案結構

- `index.html`：首頁
- `products.html`：商品前台頁
- `admin.html`：商品管理後台（僅由 contact.html 右下角小圓鈕進入）
- `contact.html`：聯絡方式頁，唯一後台入口

---

## 📝 其他

- 如需調整管理入口位置，請修改 contact.html 內的 admin-fab-static 按鈕區塊。
- 本專案無需伺服器、無需資料庫安裝，所有資料與圖片皆雲端同步。

## 📝 商品信息格式

- **id**：商品編號（按順序遞增）
- **name**：商品名稱
- **price**：價格（澳門幣）
- **category**：分類（耳環/項鍊/手鐲/戒指）
- **style**：風格（天然鑽石/天然翡翠/天然珍珠等）
- **description**：商品描述
