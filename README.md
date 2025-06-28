# 📝 Python Task Manager CLI App

A powerful and lightweight command-line-based Task Manager written in Python. It allows you to create, categorize, view, mark, and delete tasks with time-based reminders—all stored safely in versioned JSON files. Perfect for students, developers, or anyone needing personal productivity tracking from the terminal.

---

## 🚀 Features

- 📂 **Persistent Storage**  
  Automatically creates and saves tasks in versioned `.json` files under the `./task_manager/` directory. Each session is isolated for version control.
  
- ⏰ **Time-Based Reminders**  
  Runs a background thread that alerts you when tasks are due—no need to check manually.

- 📊 **Smart Categorization**  
  Tasks are neatly grouped by due date for easy viewing:
  - Overdue Tasks
  - Today’s Tasks
  - Tomorrow’s Tasks
  - This Week’s Tasks
  - Next Week’s Tasks
  - This Month’s Tasks
  - Other Future Tasks
  - ✅ Completed Tasks

- 📝 **Add Task**  
  Input task title, due date & time (in `DD/MM/YYYY HH:MM` format), and optional notes.

- 👀 **View Tasks**  
  Clean and readable terminal display, sorted and categorized for better context.

- ✅ **Mark / ❌ Unmark Tasks**  
  Toggle task completion status with ID and title confirmation.

- 🗑️ **Delete Individual or All Tasks**  
  Safely remove specific tasks or wipe the entire file upon confirmation.

- 🔁 **Auto Filename Management**  
  Keeps track of all your data versions via `task_manager_counter.json`.

- 🛡️ **Robust Input Validation**  
  Prevents invalid entries and enforces strict matching between task ID and title.

- 🔒 **Zero Dependencies**  
  Built using only Python’s standard library—no installation required beyond Python 3.x.

---

## 📂 File Structure

When first run, the app will create the following structure:

```
project_directory/
│
├── task_manager/                  # Automatically generated folder
│   ├── task_data1.json            # Auto-generated JSON file for tasks
│   └── task_manager_counter.json  # Tracks the latest file version
│
├── task_manager.py                # The main Python script
└── README.md                      # You're reading it!
```

---

## 🛠️ How to Use

### 1. Clone This Repository

```bash
git clone https://github.com/yourusername/task-manager-cli.git
cd task-manager-cli
```

### 2. Run the Application

```bash
python task_manager.py
```

### 3. Available Options in CLI

```
1. Add Task  
2. View Tasks  
3. Mark Done  
4. Unmark Done  
5. Delete Task  
6. Clear All  
7. Exit  
```

- You can enter an existing filename (e.g., `task_data1.json`) when prompted, or leave it blank to create a new session.
- Task ID and title are required to mark or delete tasks, ensuring safe operations.
- Reminders are automatic and trigger once per minute when the task is due.

---

## 📸 Example Output

```
Today's Tasks

1. Finish Project Report           ❌  
Today, 14:00  
2025-06-27T14:00:00  

2. Attend Team Meeting            ✅  
Today, 16:30  
2025-06-27T16:30:00  
```

---

## 🤝 Contributing

Feel free to fork this project, suggest features, or report issues! Pull requests are always welcome.

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 💡 Final Note

This project was built to reinforce command-line automation skills and explore JSON-based storage systems. The categorization logic and real-time reminder features provide an effective, distraction-free way to stay productive directly from your terminal.
