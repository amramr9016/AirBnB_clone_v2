-- Creates a MySQL server with:
--   Database new_db.
--   User new_user with password new_user_pwd in localhost.
--   Grants all privileges for new_user on new_db.
--   Grants SELECT privilege for new_user on new_schema.


-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS new_db;

-- Create the user if it doesn't exist
CREATE USER IF NOT EXISTS 'new_user'@'localhost' IDENTIFIED BY 'new_user_pwd';

-- Grant all privileges on new_db to new_user
GRANT ALL PRIVILEGES ON new_db.* TO 'new_user'@'localhost';

-- Grant SELECT privilege on new_schema to new_user
GRANT SELECT ON new_schema.* TO 'new_user'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;
