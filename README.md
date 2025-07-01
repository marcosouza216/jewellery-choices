# 操作指南

Jewellery Choices 珠寶店商品管理操作步驟。
影片指南： https://drive.google.com/file/d/1NAq_r6v86i2SDe3EkWu4HVn1DQbJU6tI/view?usp=sharing

## 🚀 操作步驟

### 第一步：建立 GitHub 帳戶

1. 訪問：https://github.com
2. 點擊右上角 "Sign up" 註冊
3. 填寫以下信息：
   - **Username**：選擇一個用戶名（例如：yourname）
   - **Email**：輸入您的電子郵箱
   - **Password**：設置密碼
4. 點擊 "Create account"
5. 完成驗證步驟（驗證郵箱等）
6. 登入您的 GitHub 帳戶

### 第二步：申請編輯權限

1. 聯繫倉庫管理員（網站擁有者）
2. 提供您的 GitHub 用戶名
3. 管理員會在倉庫設置中添加您為協作者（Collaborator）
4. 您會收到邀請郵件，點擊接受邀請

### 第三步：打開 Repository

1. 訪問：https://github.com/marcosouza216/jewellery-choices.git
2. 點擊進入倉庫頁面

### 第四步：修改商品列表

#### 方法一：直接在網頁編輯

1. 在倉庫中找到 `products.xlsx` 文件
2. 點擊文件，然後點擊右上角 "Download raw file" 下載到本地
3. 用 Excel 或 Google Sheets 打開並編輯
4. 按照以下格式修改商品信息：

| id  | name         | price | category | style    | description                  |
| --- | ------------ | ----- | -------- | -------- | ---------------------------- |
| 1   | 天然鑽石戒指 | 2888  | 戒指     | 天然鑽石 | 現代科技與經典設計的完美結合 |
| 2   | 天然翡翠吊墜 | 1299  | 項鍊     | 天然翡翠 | 獨特設計的天然翡翠吊墜       |
| 3   | 天然珍珠耳環 | 1588  | 耳環     | 天然珍珠 | 天然珍珠耳環設計             |

5. 編輯完成後，**另存為 Excel 格式 (.xlsx)**
6. 回到 GitHub 倉庫，進入 `products.xlsx` 文件
7. 點擊鉛筆圖標 "Edit this file"
8. 點擊 "Choose your files" 或直接拖拽新的 Excel 文件
9. 點擊 "Commit changes" 替換原文件

#### 方法二：下載 Excel 文件編輯後替換

1. 在倉庫中找到 `products.xlsx` 文件
2. 點擊文件，然後點擊右上角 "Download raw file" 下載到本地
3. 用 Excel 或 Google Sheets 打開並編輯
4. 編輯完成後，**另存為 Excel 格式 (.xlsx)**
5. 回到 GitHub 倉庫，進入 `products.xlsx` 文件
6. 點擊鉛筆圖標 "Edit this file"
7. 點擊 "Choose your files" 或直接拖拽新的 Excel 文件
8. 點擊 "Commit changes" 替換原文件

### 第五步：添加商品圖片

#### 方法一：上傳圖片

1. 進入 `image/product_images/` 文件夾
2. 點擊 "Add file" → "Upload files"
3. **上傳方式**：
   - **單張上傳**：拖拽單張圖片到上傳區域
   - **批量上傳**：按住 Ctrl（Windows）或 Cmd（Mac）選擇多個圖片，或直接拖拽整個圖片文件夾
4. **圖片命名格式**：商品名稱-x.jpg
   - 例如：天然鑽石戒指-1.jpg
   - 例如：天然翡翠吊墜-2.jpg
5. 點擊 "Commit changes"

#### 方法二：替換整個文件夾

1. 進入 `image/` 文件夾
2. 找到 `product_images` 文件夾，點擊進入
3. 點擊 "Add file" → "Upload files"
4. **直接拖拽整個新的 product_images 文件夾**到上傳區域
5. GitHub 會自動替換整個文件夾內容
6. 點擊 "Commit changes"

**注意**：此方法會完全替換現有的 product_images 文件夾，請確保新文件夾包含所有需要的圖片。

## 📝 商品信息格式

- **id**：商品編號（按順序遞增）
- **name**：商品名稱
- **price**：價格（澳門幣）
- **category**：分類（耳環/項鍊/手鐲/戒指）
- **style**：風格（天然鑽石/天然翡翠/天然珍珠等）
- **description**：商品描述

## 🖼️ 圖片要求

- **格式**：PNG、JPG、JPEG
- **命名**：商品名稱-x.jpg（x 為數字）
- **路徑**：`image/product_images/`

### 圖片命名示例

```
商品名稱: 天然鑽石戒指
圖片命名: 天然鑽石戒指-1.jpg

商品名稱: 天然翡翠吊墜
圖片命名: 天然翡翠吊墜-1.jpg
天然翡翠吊墜-2.jpg
```

## 🔧 常見問題

### Q: 如何刪除商品？

A: 編輯 Excel 文件，刪除對應行，同時刪除對應的圖片文件

### Q: 如何刪除圖片？

A: 進入 `image/product_images/` 文件夾，點擊圖片文件 → 點擊垃圾桶圖標 → 填寫確認信息 → Commit changes

### Q: 圖片上傳後網站沒有顯示？

A: 檢查圖片名稱是否與商品名稱一致，包括空格和標點符號
