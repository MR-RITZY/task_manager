import datetime, os, os.path, json, threading, time, sys
class Task_manager:
    def __init__(self, filename = ''):
        base_dir = os.path.join(os.getcwd(), "task_manager")
        counter_file = os.path.join(base_dir, "task_manager_counter.json")
        os.makedirs(base_dir, exist_ok=True)
        if filename != '':
            filename = os.path.join(base_dir, filename)
            if os.path.exists(filename) and filename.endswith(".json"):
                with open(filename, 'r') as f:
                    self.task_container = json.load(f)
            else:
                print('No such data file')
                return
        else:
            self.task_container = {}
            if os.path.exists(counter_file):
                with open(counter_file, 'r+') as f:
                    counter_data = json.load(f)
                    counter = counter_data["counter"] + 1
                    f.seek(0)
                    json.dump({"counter": counter}, f)
                    f.truncate()
            else:
                counter = 1
                with open(counter_file, 'w') as f:
                    json.dump({"counter": counter}, f)
            filename = f"task_data{counter}.json"
        self.filename = os.path.join(base_dir, filename)
        self.task_counter = max(map(int, self.task_container.keys()), default=0)

    def add_task(self):
        task_title = input("Add a new task\n")
        while True:
            try:
                task_time = datetime.datetime.strptime(input("Enter task time in DD/MM/YYYY HH:MM (24 hours time)\n"), "%d/%m/%Y %H:%M")
                break
            except:
                print("Invalid time structure")

        note = input("Add notes\n")
        self.task_counter += 1
        task = {"id": self.task_counter, "task_title": task_title, "task_time": task_time.isoformat(), "note": note, "status": False}
        self.task_container[self.task_counter] = task
        self.save()
        print("Task added successfully")
        print(f"Your data file is: {os.path.basename(self.filename)}, the task name is: {task['task_title']}, the task id is: {task['id']}")

    def view_tasks(self):
        now = datetime.datetime.now()
        week_day = (now.weekday()+1)%7
        day_start = datetime.datetime.combine(now, datetime.time())
        day_end = day_start + datetime.timedelta(days=1)
        tomorrow_end = day_end + datetime.timedelta(days=1)
        weekend = day_start + datetime.timedelta(7-week_day)
        next_weekend = weekend + datetime.timedelta(7)
        task_list = list(self.task_container.values())
        task_text = ''
        overdue_tasks, today_tasks, tomorrow_tasks, this_week_tasks, next_week_tasks, this_month_tasks, others, done_task = [], [],[], [], [], [], [], []
        task_categories = [overdue_tasks, today_tasks, tomorrow_tasks, this_week_tasks, next_week_tasks, this_month_tasks, others, done_task]
        task_headings = ["Overdue Tasks", "Today's Tasks", "Tomorrow's Tasks", "This Week Tasks", "Next Week Tasks",
        "This Month Tasks", "Other Tasks", "Completed Tasks"]

        if now.month < 12:
            month_end = datetime.datetime.combine(datetime.date(now.year, now.month+1, 1), datetime.time())
        else:
            month_end = datetime.datetime.combine(datetime.date(now.year+1, 1, 1), datetime.time())

        for task in task_list:
            if not task["status"]:
                time = datetime.datetime.fromisoformat(task["task_time"])
                if day_start <= time < now:
                    overdue_tasks.append(task)
                elif now <= time < day_end:
                    today_tasks.append(task)
                elif day_end <= time < tomorrow_end:
                    tomorrow_tasks.append(task)
                elif tomorrow_end <= time < weekend:
                    this_week_tasks.append(task)
                elif weekend <= time < next_weekend:
                    next_week_tasks.append(task)
                elif next_weekend <= time < month_end:
                    this_month_tasks.append(task)
                else:
                    others.append(task)
            else:
                done_task.append(task)

        for i, task_category in enumerate(task_categories):
            if len(task_category) != 0:
                sorted_task_category = sorted(task_category, key = lambda t: datetime.datetime.fromisoformat(t["task_time"]))
                task_text += task_headings[i] + "\n\n"
                for task in sorted_task_category:
                    time = datetime.datetime.fromisoformat(task["task_time"])
                    if i > 2:
                        formatted_time = time.ctime()
                    elif i == 2:
                        formatted_time = "Tomorrow, " + time.strftime("%H:%M")
                    else:
                        formatted_time = "Today, " + time.strftime("%H:%M")
                    task_text += f"{task['id']}. {task['task_title']}\t\t\t{'✅' if task['status'] else '❌'}\n{formatted_time}\n{task['task_time']}\n\n"
        if task_text != '':
            print(task_text)
        else:
            print("No task available")

    def mark_done(self, task_id, task_name):
        try:
            task_id = int(task_id)
        except ValueError:
            print("Task ID must be a number.")

        if task_id in self.task_container:
            if self.task_container[task_id]["task_title"].lower() == task_name.lower():
                self.task_container[task_id]["status"] = True
                print("Task marked as done ✅")
            else:
                print("No task with such title")
        else:
            print("No task with such ID")
        self.save()

    def un_mark_done(self, task_id, task_name):
        try:
            task_id = int(task_id)
        except ValueError:
            print("Task ID must be a number.")

        if task_id in self.task_container:
            if self.task_container[task_id]["task_title"].lower() == task_name.lower():
                self.task_container[task_id]["status"] = False
                print("Task unmark done ❌")
            else:
                print("No task with such title")
        else:
            print("No task with such ID")
        self.save()

    def delete_task(self, task_id, task_name):
        try:
            task_id = int(task_id)
        except ValueError:
            print("Task ID must be a number.")

        if task_id in self.task_container:
            if self.task_container[task_id]["task_title"].lower() == task_name.lower():
                confirmation = input("Are you sure you want task deleted? yes/no")
                if confirmation.lower() == "yes":
                    del self.task_container[task_id]
                    print("Task deleted 🗑️")
            else:
                print("No task with such title")
        else:
            print("No task with such ID")
        self.save()

    def clear_task_manager(self):
        confirmation = input("Are you sure you want all tasks cleared? yes/no")
        if confirmation.lower() == "yes":
            os.remove(self.filename)
            print("All tasks successfully cleared 🗑")
            return

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.task_container, f, default=str)

    def reminder(self):
        def check_tasks():
            while True:
                now = datetime.datetime.now().replace(second=0, microsecond=0)
                for task in self.task_container.values():
                    task_time = datetime.datetime.fromisoformat(task["task_time"]) if isinstance(task["task_time"], str) else task["time_task"]
                    if not task["status"] and now <= task_time < now + datetime.timedelta(minutes=1):
                        print(f"🔔 Reminder: it's time for '{task['task_title']}'!")
                        os.system('echo \a')
                time.sleep(60)

        t = threading.Thread(target=check_tasks, daemon=True)
        t.start()

def main():
    filename = input("Enter your data file --Not Required If First Time--\n")
    tm = Task_manager(filename)
    tm.reminder()  # Optional
    while True:
        print("\n1. Add Task\n2. View Tasks\n3. Mark Done\n4. Unmark Done\n5. Delete Task\n6. Clear All\n7. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            tm.add_task()
        elif choice == '2':
            tm.view_tasks()
        elif choice == '3':
            task_id = input("Task ID: ")
            task_name = input("Task Name: ")
            tm.mark_done(task_id, task_name)
        elif choice == '4':
            task_id = input("Task ID: ")
            task_name = input("Task Name: ")
            tm.un_mark_done(task_id, task_name)
        elif choice == '5':
            task_id = input("Task ID: ")
            task_name = input("Task Name: ")
            tm.delete_task(task_id, task_name)
        elif choice == '6':
            tm.clear_task_manager()
        elif choice == '7':
            break
        else:
            print("Invalid input")

if __name__ == "__main__":
    main()
