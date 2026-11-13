-- 已有库：去重收藏 + 对齐唯一约束与索引（按需执行一次）
-- 同一用户对同一新闻只保留 id 最小的一条

DELETE f1 FROM `favorite` f1
INNER JOIN `favorite` f2
  ON f1.`user_id` = f2.`user_id`
 AND f1.`news_id` = f2.`news_id`
 AND f1.`id` > f2.`id`;

-- 若仍是旧约束名 uq_favorite_user_news，可改为 user_news_unique（无该约束时跳过报错即可）
-- ALTER TABLE `favorite` DROP INDEX `uq_favorite_user_news`;
-- ALTER TABLE `favorite` ADD UNIQUE KEY `user_news_unique` (`user_id`, `news_id`);

-- ALTER TABLE `favorite` ADD KEY `fk_favorite_user_idx` (`user_id`);
-- ALTER TABLE `favorite` ADD KEY `fk_favorite_news_idx` (`news_id`);
