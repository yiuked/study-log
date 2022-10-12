写入物品空投
```sql
-- 单个空投
SELECT MD5(concat(m.token_id,m.good_id1)) uuid,m.user_id,1 origin,m.token_id from_token_id,m.creator_user_id,m.product_id,m.good_id1 airdrop_welfare_id,m.card_fiexd_id card_welfare_type,
m.card_type1 card_welfare_fixed_id,
w.cover_url,w.`name` title,w.`desc`,1 take_status,1 transfer,1 sale_status,w.goods_type,w.virtual_type,w.virtual_url FROM a_music m
LEFT JOIN airdrop_welfare w ON m.good_id1=w.id WHERE m.id>1289;


-- 多空投
SELECT MD5(concat(m.order_no,m.token_id,m.good_id1)) uuid,m.user_id,1 origin,m.token_id from_token_id,m.creator_user_id,m.product_id,m.good_id1 airdrop_welfare_id,m.card_fiexd_id card_welfare_type,
m.card_type1 card_welfare_fixed_id,
w.cover_url,w.`name` title,w.`desc`,1 take_status,1 transfer,1 sale_status,w.goods_type,w.virtual_type,w.virtual_url FROM a_music m
LEFT JOIN airdrop_welfare w ON m.good_id1=w.id WHERE m.id>1289
UNION ALL
SELECT MD5(concat(m.order_no,m.token_id,m.good_id2)) uuid,m.user_id,1 origin,m.token_id from_token_id,m.creator_user_id,m.product_id,m.good_id2 airdrop_welfare_id,m.card_fiexd_id card_welfare_type,
m.card_type2 card_welfare_fixed_id,
w.cover_url,w.`name` title,w.`desc`,1 take_status,1 transfer,1 sale_status,w.goods_type,w.virtual_type,w.virtual_url FROM a_music m
LEFT JOIN airdrop_welfare w ON m.good_id2=w.id WHERE m.id>1278;





-- INSERT INTO goods_owner(uuid,user_id,origin,from_token_id,creator_user_id,product_id,airdrop_welfare_id,card_welfare_type,card_welfare_fixed_id,cover_url,title,`desc`,take_status,transfer,sale_state,goods_type,virtual_type,virtual_url) 
-- VALUES
-- ();
```

同步字段
```sql
-- UPDATE a_music a SET a.user_id=(SELECT u.id FROM `user` u WHERE u.phone=a.phone AND u.deleted_at IS NULL);

-- UPDATE a_music a SET a.token_id=(SELECT u.token_id FROM `order` u WHERE u.order_no=a.order_no AND u.deleted_at IS NULL)

-- UPDATE a_music a SET a.creator_user_id=(SELECT u.user_id FROM `product` u WHERE u.id=a.product_id AND u.deleted_at IS NULL);

-- SELECT o.token_id FROM a_music a LEFT JOIN `order` o ON a.order_no=o.order_no


SELECT m.card_no,o.token_no,o.token_id,m.token_id FROM a_music m 
LEFT JOIN product_token_owner o ON m.token_id=o.token_id


UPDATE a_music a SET a.user_id=(SELECT u.id FROM `user` u WHERE u.phone=a.phone AND u.deleted_at IS NULL) WHERE a.user_id IS NULL;
UPDATE a_music a SET a.creator_user_id=(SELECT u.user_id FROM `product` u WHERE u.id=a.product_id AND u.deleted_at IS NULL) WHERE a.creator_user_id IS NULL;
UPDATE a_music a SET a.creator=(SELECT u.art_name FROM `creator` u WHERE u.user_id=a.creator_user_id AND u.deleted_at IS NULL) WHERE a.creator IS NULL;

-- 公益订单
-- UPDATE a_music a SET a.token_id=(SELECT u.token_id FROM `cares_support_order` u WHERE u.order_no=a.order_no AND u.deleted_at IS NULL) WHERE a.token_id IS NULL;
-- 原创订单
UPDATE a_music a SET a.token_id=(SELECT u.token_id FROM `product_token_owner` u WHERE u.token_no=a.card_no AND u.user_id=a.user_id AND u.deleted_at IS NULL) WHERE a.token_id IS NULL;

-- UPDATE a_music a SET a.product_name=(SELECT u.`title` FROM `product` u WHERE u.id=a.product_id AND u.deleted_at IS NULL) WHERE a.product_name IS NULL;

```