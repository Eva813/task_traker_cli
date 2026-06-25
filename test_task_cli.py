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
def temp_db():
    """Create a temporary database for testing."""
    # TODO: 實現 fixture
    # 1. 創建臨時文件
    # 2. 初始化空數據庫 {"tasks": []}
    # 3. yield 臨時文件路徑
    # 4. 清理臨時文件
    pass


class TestDatabaseIO:
    """Test database loading and saving."""
    
    def test_load_empty_database(self, temp_db):
        """Test loading a non-existent database returns empty structure."""
        # TODO: 實現測試
        pass
    
    def test_save_and_load_database(self, temp_db):
        """Test that saved data can be loaded back."""
        # TODO: 實現測試
        pass


class TestAddTask:
    """Test add_task function."""
    
    def test_add_single_task(self, temp_db):
        """Test adding a single task."""
        # TODO: 實現測試
        pass
    
    def test_add_multiple_tasks(self, temp_db):
        """Test adding multiple tasks with auto-incrementing IDs."""
        # TODO: 實現測試
        pass
    
    def test_new_task_has_todo_status(self, temp_db):
        """Test that new tasks have 'todo' status by default."""
        # TODO: 實現測試
        pass


class TestUpdateTask:
    """Test update_task function."""
    
    def test_update_task_description(self, temp_db):
        """Test updating task description."""
        # TODO: 實現測試
        pass
    
    def test_update_task_status(self, temp_db):
        """Test updating task status."""
        # TODO: 實現測試
        pass
    
    def test_update_nonexistent_task(self, temp_db):
        """Test updating a task that doesn't exist returns False."""
        # TODO: 實現測試
        pass


class TestDeleteTask:
    """Test delete_task function."""
    
    def test_delete_existing_task(self, temp_db):
        """Test deleting an existing task."""
        # TODO: 實現測試
        pass
    
    def test_delete_nonexistent_task(self, temp_db):
        """Test deleting a task that doesn't exist returns False."""
        # TODO: 實現測試
        pass


class TestListTasks:
    """Test list_tasks function."""
    
    def test_list_all_tasks(self, temp_db):
        """Test listing all tasks."""
        # TODO: 實現測試
        pass
    
    def test_list_tasks_by_status(self, temp_db):
        """Test filtering tasks by status."""
        # TODO: 實現測試
        pass
    
    def test_list_tasks_by_date(self, temp_db):
        """Test filtering tasks by date."""
        # TODO: 實現測試
        pass


class TestMarkFunctions:
    """Test mark_done and mark_in_progress functions."""
    
    def test_mark_task_as_done(self, temp_db):
        """Test marking a task as done."""
        # TODO: 實現測試
        pass
    
    def test_mark_task_as_in_progress(self, temp_db):
        """Test marking a task as in-progress."""
        # TODO: 實現測試
        pass
