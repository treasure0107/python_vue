-- 已有库将 user_token 字段/索引对齐 models/user_token.py（按需执行）
ALTER TABLE `user_token`
  MODIFY COLUMN `id` INT NOT NULL AUTO_INCREMENT COMMENT '令牌ID',
  MODIFY COLUMN `user_id` INT NOT NULL COMMENT '用户ID',
  MODIFY COLUMN `token` VARCHAR(255) NOT NULL COMMENT '令牌值',
  MODIFY COLUMN `expires_at` DATETIME NOT NULL COMMENT '过期时间',
  MODIFY COLUMN `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间';

-- 若存在旧索引名，可先 DROP 再 ADD（MySQL 8 可按实际 SHOW INDEX 调整）
-- ALTER TABLE `user_token` DROP INDEX `uq_user_token`, ADD UNIQUE KEY `token_UNIQUE` (`token`);
-- ALTER TABLE `user_token` DROP INDEX `ix_user_token_user_id`, ADD KEY `fk_user_token_user_idx` (`user_id`);
