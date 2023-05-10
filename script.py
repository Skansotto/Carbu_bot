__user_statuses = dict[int, str]

id_user = 0


if id_user in __user_statuses.keys():
    __user_statuses[id_user] = "started_now"
user_status = __user_statuses[id_user]

if user_status == "loggando":
    username = getMessage()text
