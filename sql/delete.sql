DELETE
FROM role_tracker
WHERE guild = ?
  AND member = ?
  AND role = ?