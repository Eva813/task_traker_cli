"""
Unit tests for task_cli.py using pytest

Run tests with: pytest test_task_cli.py -v
"""

import pytest
import json
import tempfile
import os
from task_cli import (
    add_task,
    update_task,
    delete_task,
    list_tasks,
    load_database,
    save_database,
    mark_done,
    mark_in_progress,
)


@pytest.fixture
def temp_db(monkeypatch):
    """Create a temporary database for testing.
    
    This fixture:
    1. Creates a temporary JSON file for the database
    2. Initializes it with empty structure {"tasks": []}
    3. Mocks save_database to write only to temp files (not tasks.json)
    4. Yields the temporary file path
    5. Cleans up the temporary file after the test
    """
    # 1. 建立臨時檔案（在專案目錄下，方便檢視）
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, dir='.') as f:
        temp_file_path = f.name
        # 2. 寫入 {"tasks": []}
        json.dump({"tasks": []}, f)
    
    # 列印檔案位置方便調試
    print(f"\n📝 Test database: {temp_file_path}")
    
    # Mock save_database to prevent writing to the real tasks.json
    # but allow writing to temp files for proper testing
    def mock_save_database(database, path="tasks.json"):
        # Only allow saving to temporary files, not to the default tasks.json
        if path != "tasks.json":
            with open(path, "w") as f:
                json.dump(database, f, indent=2)
    
    monkeypatch.setattr("task_cli.save_database", mock_save_database)
    
    # 3. yield 檔案路徑
    yield temp_file_path
    
    # 4. 測試後刪檔
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)


class TestDatabaseIO:
    """Test database loading and saving."""
    
    def test_load_empty_database(self, temp_db):
        """Test loading a non-existent database returns empty structure."""
        # 載入 temp_db 預先創建的空資料庫
        database = load_database(temp_db)
        
        # 驗證：結構正確、tasks 列表為空
        assert isinstance(database, dict), "Database should be a dict"
        assert "tasks" in database, "Database should have 'tasks' key"
        assert database["tasks"] == [], "Empty database should have empty tasks list"
    
    def test_save_and_load_database(self, temp_db):
        """Test that saved data can be loaded back."""
        # 建立一個測試資料庫
        test_database = {
            "tasks": [
                {
                    "id": 1,
                    "description": "Test task 1",
                    "status": "todo",
                    "date": "2025-06-26"
                },
                {
                    "id": 2,
                    "description": "Test task 2",
                    "status": "in-progress",
                    "date": "2025-06-26"
                }
            ]
        }
        
        # 儲存到 temp_db 檔案
        save_database(test_database, temp_db)
        
        # 重新載入
        loaded_database = load_database(temp_db)
        
        # 驗證：載入的資料等於原始資料
        assert loaded_database == test_database, "Loaded database should match saved database"
        assert len(loaded_database["tasks"]) == 2, "Should have 2 tasks"
        assert loaded_database["tasks"][0]["id"] == 1, "First task should have id=1"
        assert loaded_database["tasks"][1]["status"] == "in-progress", "Second task should be in-progress"


class TestAddTask:
    """Test add_task function."""
    
    def test_add_single_task(self, temp_db):
        """Test adding a single task."""
        # TODO: 實現測試
        added_task = add_task(temp_db, "Test single task")
        assert added_task is not None, "Added task should not be None"
        assert added_task["description"] == "Test single task", "Task description should match"
        assert added_task["status"] == "todo", "New task should have 'todo' status"
    
    def test_add_multiple_tasks(self, temp_db):
        """Test adding multiple tasks with auto-incrementing IDs."""
        database = load_database(temp_db)
        
        # Add 3 tasks
        task1 = add_task(temp_db, "First task")
        task2 = add_task(temp_db, "Second task")
        task3 = add_task(temp_db, "Third task")
        
        # Verify IDs are auto-incrementing
        assert task1["id"] == 1, "First task should have id=1"
        assert task2["id"] == 2, "Second task should have id=2"
        assert task3["id"] == 3, "Third task should have id=3"
        
        # Verify all tasks are in database
        database = load_database(temp_db)
        assert len(database["tasks"]) == 3, "Should have 3 tasks"
        assert database["tasks"][0]["description"] == "First task"
        assert database["tasks"][1]["description"] == "Second task"
        assert database["tasks"][2]["description"] == "Third task"
    
    def test_new_task_has_todo_status(self, temp_db):
        """Test that new tasks have 'todo' status by default."""
        # TODO: 實現測試
        added_task = add_task(temp_db, "Check default status")
        assert added_task["status"] == "todo", "New task should have 'todo' status"


class TestUpdateTask:
    """Test update_task function."""
    
    def test_update_task_description(self, temp_db):
        """Test updating task description."""
        # TODO: 實現測試
        added_task = add_task(temp_db, "Original description")
        update_task(temp_db, added_task["id"], description="Updated description")
        database = load_database(temp_db)
        # 從生成器中取得 第一個符合條件的任務。
        # 如果沒有找到任何符合條件的任務，就返回 None（這是 default 的值）。
        task = next((t for t in database["tasks"] if t["id"] == added_task["id"]), None)
        assert task is not None, "Task should exist"
        assert task["description"] == "Updated description", "Task description should be updated"
    
    def test_update_task_status(self, temp_db):
        """Test updating task status."""
        # TODO: 實現測試
        added_task = add_task(temp_db, "test status update")
        update_task(temp_db, added_task["id"], status="done")
        database = load_database(temp_db)
        task = next((t for t in database["tasks"] if t["id"] == added_task["id"]), None)
        assert task is not None, "Task should exist"
        assert task["status"] == "done", "Task status should be done" 
    
    def test_update_nonexistent_task(self, temp_db):
        """Test updating a task that doesn't exist returns False."""
        # TODO: 實現測試
        result = update_task(temp_db, 999, description="Should not exist")
        assert result is False, "Updating a nonexistent task should return False"

class TestDeleteTask:
    """Test delete_task function."""
    
    def test_delete_existing_task(self, temp_db):
        """Test deleting an existing task."""
        # TODO: 實現測試
        added_task = add_task(temp_db, "test status update")
        delete_task(temp_db, added_task["id"])
        database = load_database(temp_db)
        task = next((t for t in database["tasks"] if t["id"] == added_task["id"]), None)
        assert task is None, "Task should be deleted"
    
    def test_delete_nonexistent_task(self, temp_db):
        """Test deleting a task that doesn't exist returns False."""
        # TODO: 實現測試
        result = delete_task(temp_db, 999)
        assert result == False, "Delet a nonexistent task should return False"


class TestListTasks:
    """Test list_tasks function."""
    
    def test_list_all_tasks(self, temp_db):
        """Test listing all tasks."""
        # TODO: 實現測試
        added_task = add_task(temp_db, "test list")
        tasks = list_tasks(temp_db)
        # 驗證：應該只列出一個任務
        assert len(tasks) == 1, "Should list 1 task"
    
    def test_list_tasks_by_status(self, temp_db):
        """Test filtering tasks by status."""
        # 新增 3 筆任務
        task1 = add_task(temp_db, "Task 1")
        task2 = add_task(temp_db, "Task 2")
        task3 = add_task(temp_db, "Task 3")
        
        # 更新其中一筆狀態為 done
        update_task(temp_db, task2["id"], status="done")
        
        # 測試篩選 todo 狀態
        todo_tasks = list_tasks(temp_db, status="todo")
        assert len(todo_tasks) == 2, "Should have 2 todo tasks"
        assert all(t["status"] == "todo" for t in todo_tasks), "All filtered tasks should have todo status"
        
        # 測試篩選 done 狀態
        done_tasks = list_tasks(temp_db, status="done")
        assert len(done_tasks) == 1, "Should have 1 done task"
        assert done_tasks[0]["status"] == "done", "Filtered task should have done status"
        assert done_tasks[0]["id"] == task2["id"], "Should filter correct task by ID"
        # 加測：無該狀態的結果
        empty = list_tasks(temp_db, status="in-progress")
        assert empty == [], "Should return empty list for nonexistent status"
        
    
    def test_list_tasks_by_date(self, temp_db):
        """Test filtering tasks by date."""
        from datetime import datetime, timedelta
        
        task1 = add_task(temp_db, "Task 1")
        task2 = add_task(temp_db, "Task 2")
        
        # Calculate dates dynamically
        today = datetime.today().strftime("%Y-%m-%d")
        tomorrow = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Update task2's date to tomorrow
        update_task(temp_db, task2["id"], date=tomorrow)
        
        # Filter for today's tasks
        today_tasks = list_tasks(temp_db, date=today)
        assert len(today_tasks) == 1, "Should have 1 task for today"
        assert today_tasks[0]["id"] == task1["id"], "Should filter correct task by ID for today"
        
        # Filter for tomorrow's tasks
        tomorrow_tasks = list_tasks(temp_db, date=tomorrow)
        assert len(tomorrow_tasks) == 1, "Should have 1 task for tomorrow"
        assert tomorrow_tasks[0]["id"] == task2["id"], "Should filter correct task by ID for tomorrow"


class TestMarkFunctions:
    """Test mark_done and mark_in_progress functions."""
    
    def test_mark_task_as_done(self, temp_db):
        """Test marking a task as done."""
        # TODO: 實現測試
        added_task = add_task(temp_db, "Task to mark done")
        mark_done(temp_db, added_task["id"])
        database = load_database(temp_db)
        task = next((t for t in database["tasks"] if t["id"] == added_task["id"]), None)
        assert task is not None, "Task should exist"
        assert task["status"] == "done", "Task status should be marked as done"
    
    def test_mark_task_as_in_progress(self, temp_db):
        """Test marking a task as in-progress."""
        # TODO: 實現測試
        added_task = add_task(temp_db, "Task to mark in-progress")
        mark_in_progress(temp_db, added_task["id"])
        database = load_database(temp_db)
        task = next((t for t in database["tasks"] if t["id"] == added_task["id"]), None)
        assert task is not None, "Task should exist"
        assert task["status"] == "in-progress", "Task status should be marked as in-progress"
