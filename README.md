# Task Tracker CLI - 學習專案

這是一個基於 [Taskly](https://github.com/brkahmed/taskly) 的 Python CLI 任務管理應用。

## 📋 專案結構

```
task-tracker-python/
├── task_cli.py              # 主程序（包含 TODO 標記）
├── test_task_cli.py         # 單元測試（包含 TODO 標記）
├── tasks.json              # 任務數據存儲
├── pyproject.toml          # 項目配置
├── .python-version         # Python 版本
├── .gitignore             # Git 忽略規則
└── README.md              # 本文件
```

## 🚀 快速開始

### 方式 1️⃣：安裝為全局命令（推薦）

#### 從源碼安裝
```bash
git clone https://github.com/你的用戶名/task-tracker-python.git
cd task-tracker-python
uv pip install -e .
```

#### 或直接從 GitHub 安裝
```bash
uv pip install git+https://github.com/你的用戶名/task-tracker-python.git
```

安裝完成後，重新打開 terminal 或執行：
```bash
source ~/.zshrc
```

現在可以直接使用 `task` 命令：
```bash
task add "Buy groceries"
task list
task update 1 --status done
task mark-done 1
task delete 1
```

### 方式 2️⃣：開發模式（無需全局安裝）

```bash
cd task-tracker-python
uv sync
```

使用 `uv run` 執行：
```bash
uv run task_cli.py add "Buy groceries"
uv run task_cli.py list
uv run task_cli.py update 1 --status done
```

### 運行測試
```bash
uv run pytest test_task_cli.py -v
```

## 📝 學習路線

按照以下順序完成各個 TODO 任務：

### ✅ TODO 1: 實現 JSON 數據存儲功能
實現 `load_database()` 和 `save_database()` 函數
- 從 JSON 文件讀取任務列表
- 將任務列表寫入 JSON 文件
- 處理文件不存在的情況

**檔案**：`task_cli.py` 行 26-49

**學習重點**：
- JSON 文件 I/O
- 字典操作
- Path 對象

---

### ✅ TODO 2: 實現核心任務管理功能

#### 2a. `add_task()` — 添加新任務
- 計算新任務的 ID（最大 ID + 1）
- 創建任務字典（包含 id, description, status, date）
- 保存到數據庫

#### 2b. `update_task()` — 更新任務
- 尋找指定 ID 的任務
- 更新描述或狀態
- 驗證狀態值

#### 2c. `delete_task()` — 刪除任務
- 尋找並刪除指定 ID 的任務
- 返回成功/失敗標誌

#### 2d. `list_tasks()` — 列出任務
- 支持按狀態篩選 (todo, in-progress, done)
- 支持按日期篩選 (<, >, =)
- 返回篩選後的任務列表

**檔案**：`task_cli.py` 行 56-135

**學習重點**：
- 列表和字典操作
- 日期比較
- 篩選和過濾

---

### ✅ TODO 3: 實現快速狀態更新功能
實現 `mark_done()` 和 `mark_in_progress()` 函數
- 這些是 `update_task()` 的快捷方法

**檔案**：`task_cli.py` 行 138-147

**學習重點**：
- 函數包裝（wrapper）

---

### ✅ TODO 4: 實現命令行界面和輸出格式
實現 `print_task()` 和 `print_tasks()` 函數
- 美化輸出格式
- 顯示任務信息（ID, 描述, 狀態, 日期）

**檔案**：`task_cli.py` 行 150-164

**學習重點**：
- 字符串格式化
- 列表遍歷

---

### ✅ TODO 5: 實現命令行參數解析和命令路由
使用 `argparse` 實現：
- `add` 命令：添加任務
- `list` 命令：列出任務（支持 `-s` 和 `-d` 選項）
- `update` 命令：更新任務
- `delete` 命令：刪除任務
- `mark-done` 命令：標記完成
- `mark-in-progress` 命令：標記進行中

**檔案**：`task_cli.py` 行 167-197

**學習重點**：
- argparse 庫
- 子命令處理
- 命令行參數解析

---

### ✅ TODO 6: 編寫單元測試
實現 `test_task_cli.py` 中的所有測試用例

**檔案**：`test_task_cli.py`

**學習重點**：
- pytest 框架
- 測試 fixtures
- 測試覆蓋率

---

## 🎯 實現提示

### 數據結構
```python
database = {
    "tasks": [
        {
            "id": 1,
            "description": "Buy groceries",
            "status": "todo",        # todo, in-progress, done
            "date": "2026-06-15"     # YYYY-MM-DD 格式
        },
        ...
    ]
}
```

### 狀態值
- `"todo"` — 未開始
- `"in-progress"` — 進行中
- `"done"` — 已完成

### 命令示例
```bash
# 添加任務
task add "Buy groceries"

# 列出所有任務
task list

# 列出已完成的任務
task list --status done

# 列出特定日期的任務
task list --date 2026-06-15

# 更新任務
task update 1 --description "Buy milk" --status done

# 快速標記完成
task mark-done 1

# 快速標記進行中
task mark-in-progress 1

# 刪除任務
task delete 1
```

## 📚 學習資源

- [Python 官方文檔 - json](https://docs.python.org/3/library/json.html)
- [Python 官方文檔 - argparse](https://docs.python.org/3/library/argparse.html)
- [Python 官方文檔 - pathlib](https://docs.python.org/3/library/pathlib.html)
- [pytest 文檔](https://docs.pytest.org/)
- [原始 Taskly 專案](https://github.com/brkahmed/taskly)

## 🚀 下一步

完成所有 TODO 後，你可以：

1. ✨ 添加更多功能：
   - 優先級（priority）
   - 截止日期（due date）
   - 標籤（tags）
   - 搜索功能

2. 🎨 改進 UI：
   - 彩色輸出
   - 表格格式
   - 進度條

3. 📦 打包發佈：
   - 上傳到 PyPI
   - 創建可執行文件

4. 🧪 提高測試覆蓋率：
   - 邊界情況測試
   - 集成測試

## 💡 提示

- 先實現基本功能，後添加優化
- 經常測試，邊做邊測
- 查看原始 Taskly 項目獲取靈感
- 不要害怕出錯，錯誤是學習的好機會！

---

祝你學習愉快！🎉
