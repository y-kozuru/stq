""" Simple task queue """
import flet
import json
import os
import sys
import queue
import unittest

class Task:
    def __init__(self, content: str):
        self._content = content
    
    def content(self) -> str:
        return self._content

class TaskQueue:
    def __init__(self):
        self._queue = queue.Queue()
    
    def enqueue(self, task: Task):
        self._queue.put(task)
    
    def dequeue(self) -> Task:
        return self._queue.get()
    
    def size(self) -> int:
        return self._queue.qsize()
    
    def empty(self) -> bool:
        return self._queue.empty()
    
    def to_json(self) -> dict:
        result = []
        while not self.empty():
            result.append(self.dequeue().content())
        return {"tasks": result}
    
    def from_json(self, from_data: dict):
        for task in from_data["tasks"]:
            self.enqueue(Task(task))

class TestTask(unittest.TestCase):
    def test_content(self):
        expected = "test task"
        task = Task("test task")
        self.assertEqual(task.content(), expected)

class TestTaskQueue(unittest.TestCase):
    def test_task_queue(self):
        task_queue = TaskQueue()
        task_queue.enqueue(Task("task1"))
        task_queue.enqueue(Task("task2"))
        self.assertEqual(task_queue.size(), 2)
        self.assertEqual(task_queue.empty(), False)
        task = task_queue.dequeue()
        self.assertEqual(task.content(), "task1")
        self.assertEqual(task_queue.size(), 1)
        task_queue.dequeue()
        self.assertEqual(task_queue.empty(), True)
        task = task_queue.dequeue()
        self.assertEqual(task, None)

class SimpleTaskQueueAppEngine:
    """ App engine for separating GUI and domain model """

    def __init__(self):
        self._task_queue = TaskQueue()
        self._current_task: Task = None
        self._file_path = "tasks.json"

        if not os.path.isfile(self._file_path):
            return
        with open(self._file_path, mode="r", encoding="utf-8") as f:
            tasks = json.load(f)
        self._task_queue.from_json(tasks)
    
    def enqueue(self, content: str):
        if content == "":
            return
        self._task_queue.enqueue(Task(content))

    def can_dequeue(self) -> bool:
        return not self._task_queue.empty()

    def dequeue(self) -> Task:
        self._enqueue_current_task()
        self._current_task = self._task_queue.dequeue()
        return self._current_task
    
    def mark_as_done(self):
        self._current_task = None
    
    def save(self):
        self._enqueue_current_task()
        with open(self._file_path, mode="w", encoding="utf-8") as f:
            f.write(json.dumps(self._task_queue.to_json(), ensure_ascii=False))

    def _enqueue_current_task(self):
        if self._current_task is None:
            return
        self._task_queue.enqueue(self._current_task)
        self._current_task = None

def main(page: flet.Page):
    app_engine = SimpleTaskQueueAppEngine()
    page.title = "Simple Task Queue"
    page.window.min_width = 340
    page.window.min_height = 340
    page.window.width = page.window.min_width
    page.window.height = page.window.min_height
    page.update()
    task_control: flet.Card = None

    def remove_task_control():
        nonlocal task_control
        if task_control is None:
            return
        page.remove(task_control)
        task_control = None

    def create_task_control(task: Task):
        nonlocal task_control
        task_control = flet.Card(content=flet.Container(content=flet.Text(task.content(), expand=True),
            margin=5, padding=5, alignment=flet.alignment.center_left, border_radius=10))
        page.add(task_control)

    def handle_window_event(e):
        if e.data == "close":
            app_engine.save()
            page.window.destroy()
    page.window.prevent_close = True
    page.window.on_event = handle_window_event

    def submit_new_task(e):
        app_engine.enqueue(content.value)
        content.value = ""
        page.update()
    content = flet.TextField(label="New Task", on_submit=submit_new_task, width=200, text_size=14)

    def dequeue_clicked(e):
        if not app_engine.can_dequeue():
            return
        remove_task_control()
        create_task_control(app_engine.dequeue())
    dequeue = flet.IconButton(icon=flet.Icons.DOWNLOAD_ROUNDED, on_click=dequeue_clicked, width=30)

    def done_clicked(e):
        app_engine.mark_as_done()
        remove_task_control()
    done = flet.IconButton(icon=flet.Icons.DONE_ROUNDED, on_click=done_clicked, width=30)

    page.add(flet.Row([
        flet.Column(controls=[content]),
        flet.Column(controls=[dequeue]),
        flet.Column(controls=[done])
    ]))

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        flet.app(target=main)
