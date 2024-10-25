from globals import datetime, pytz, time_format

print(datetime.now(pytz.timezone("Asia/Calcutta")).strftime(time_format))
formatted_task = self.TASK_FORMAT.format(
    bulletin = self.character_for_TaskFormat,
    idx = f"{idx}.",
    description = task['description'],
    priority=task['priority'],
    category=task['category'] or '>ungrouped<',
    created_date=task['created_date'],
    due_date=task['due_date'] or '>no due date<'
)
formatted_final = self.TASK_FORMAT_W_STATUS.format(
    bulletin = self.character_for_TaskFormat,
    TASK_FORMAT=formatted_task,
    status="completed" if task['status'] else "pending"
)
print(formatted_final)