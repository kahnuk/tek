SELECT *
FROM role_tracker
WHERE timestamp < strftime('%s', 'now');