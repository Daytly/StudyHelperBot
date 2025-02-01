from data.constants.callback_patterns import customer_menu_pattern, edit_task_menu_pattern

create_new_task_callback = customer_menu_pattern.replace("\\S*", "create_task")
delete_task_callback = customer_menu_pattern.replace("\\S*", "delete_task")
edit_task_callback = customer_menu_pattern.replace("\\S*", "edit_task {0}")
expand_tasks_list_callback = customer_menu_pattern.replace("\\S*", "expand_task_list")
collapse_task_list_callback = customer_menu_pattern.replace("\\S*", "collapse_task_list")
next_task_callback = customer_menu_pattern.replace("\\S*", "next_task {0}")
previous_task_callback = customer_menu_pattern.replace("\\S*", "previous_task {0}")
edit_task_exit_callback = customer_menu_pattern.replace("\\S*", "edit_task_exit")

edit_task_text_callback = edit_task_menu_pattern.replace("\\S*", "text {0}")
edit_task_award_callback = edit_task_menu_pattern.replace("\\S*", "award {0}")
edit_task_death_line_callback = edit_task_menu_pattern.replace("\\S*", "deathline {0}")
edit_task_delete_callback = edit_task_menu_pattern.replace("\\S*", "delete {0}")
edit_task_confirm_callback = edit_task_menu_pattern.replace("\\S*", "delete {0}")
