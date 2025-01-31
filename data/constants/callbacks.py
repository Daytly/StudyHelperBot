from data.constants.callback_patterns import customer_menu_pattern

create_new_task_callback = customer_menu_pattern.replace("\\S*", "create_task")
delete_task_callback = customer_menu_pattern.replace("\\S*", "delete_task")
edit_task_callback = customer_menu_pattern.replace("\\S*", "edit_task")
expand_tasks_list_callback = customer_menu_pattern.replace("\\S*", "expand_task_list")
collapse_task_list_callback = customer_menu_pattern.replace("\\S*", "collapse_task_list")
next_task_callback = customer_menu_pattern.replace("\\S*", "next_task")
previous_task_callback = customer_menu_pattern.replace("\\S*", "previous_task")