-- Add is_deleted field to biz_achievements table for soft delete functionality
-- Migration: 002_add_is_deleted_to_achievements

-- Add the column with default value
ALTER TABLE biz_achievements 
ADD COLUMN is_deleted BOOLEAN NOT NULL DEFAULT FALSE;

-- Create index for better query performance
CREATE INDEX idx_biz_achievements_is_deleted ON biz_achievements(is_deleted);

-- Verify the change
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'biz_achievements' AND COLUMN_NAME = 'is_deleted';
