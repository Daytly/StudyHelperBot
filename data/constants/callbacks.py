from data.constants.callback_patterns import customer_menu_pattern, edit_task_menu_pattern, admin_group_menu_pattern, \
    executor_menu_pattern

create_new_order_callback = customer_menu_pattern.replace("\\S*", "create_task")
delete_order_callback = customer_menu_pattern.replace("\\S*", "delete_task")
edit_order_callback = customer_menu_pattern.replace("\\S*", "edit_task {0}")
expand_order_list_callback = customer_menu_pattern.replace("\\S*", "expand_task_list")
collapse_order_list_callback = customer_menu_pattern.replace("\\S*", "collapse_task_list")
next_order_callback = customer_menu_pattern.replace("\\S*", "next_task {0}")
previous_order_callback = customer_menu_pattern.replace("\\S*", "previous_task {0}")
edit_order_exit_callback = customer_menu_pattern.replace("\\S*", "edit_task_exit")

edit_task_text_callback = edit_task_menu_pattern.replace("\\S*", "text {0}")
edit_task_award_callback = edit_task_menu_pattern.replace("\\S*", "award {0}")
edit_task_death_line_callback = edit_task_menu_pattern.replace("\\S*", "deathline {0}")
edit_task_delete_callback = edit_task_menu_pattern.replace("\\S*", "delete {0}")
edit_task_confirm_callback = edit_task_menu_pattern.replace("\\S*", "confirm {0}")

access_task_callback = admin_group_menu_pattern.replace("\\S*", "access {0}")
cancel_task_callback = admin_group_menu_pattern.replace("\\S*", "cancel {0}")

confirm_task_callback = executor_menu_pattern.replace("\\S*", "confirm_task {0}")
expand_task_list_callback = executor_menu_pattern.replace("\\S*", "expand_task_list")
collapse_task_list_callback = executor_menu_pattern.replace("\\S*", "collapse_task_list")
next_task_callback = executor_menu_pattern.replace("\\S*", "next_task {0}")
previous_task_callback = executor_menu_pattern.replace("\\S*", "previous_task {0}")
