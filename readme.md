# stq - simple task queue
Priority queue for simple task management.

# How to Use
Write a task in **New Task** and press Enter to add the task.  
Click the exclamation mark instead of pressing Enter to add the task as a priority task.

Click the dequeue button (down arrow) to get a task from the queue.  
If priority tasks exist, they will be deququed first.

Click the check mark to mark a test as completed.  
Only one task can be displayed at the time.

If you click the dequeue button while a task is not completed, the current task will be skipped.  
The skipped task will be enqueued in the queue, and the next task will be dequeued from the queue.

# tasks.json
If there are tasks remaining in the queue when the app is closed, the remaining tasks are recorded in tasks.json.  
When you launch the app again, it will restore the queue from tasks.json.  
tasks.json will be created in the directory where the app was run.

# Setup
```bash
pip install -r requirements.txt
```

# Run
```bash
python stq.py
```
