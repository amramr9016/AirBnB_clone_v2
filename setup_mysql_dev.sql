-- Creates a MySQL server with:
--   Database new_dev_db.
--   User new_dev with password new_dev_pwd in localhost.
--   Grants all privileges for new_dev on new_dev_db.
--   Grants SELECT privilege for new_dev on performance.

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS new_dev_db;

-- Create the user if it doesn't exist
CREATE USER IF NOT EXISTS 'new_dev'@'localhost' IDENTIFIED BY 'new_dev_pwd';

-- Grant all privileges on new_dev_db to new_dev
GRANT ALL PRIVILEGES ON new_dev_db.* TO 'new_dev'@'localhost';

-- Grant SELECT privilege on performance_schema to new_dev
GRANT SELECT ON performance_schema.* TO 'new_dev'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;
