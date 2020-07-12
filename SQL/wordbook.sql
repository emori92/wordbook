
-- follow
SELECT
    t2.username AS following
    , t3.username AS followed
FROM
    follow AS t1
LEFT JOIN
    user AS t2
ON
    t1.following_id == t2.id
LEFT JOIN
    user AS t3
ON
    t1.followed_id == t3.id
-- WHERE
--     t2.username == 'test'
;


-- star
SELECT
    t2.username AS user
    , t3.title AS liked_title
FROM
    star AS t1
LEFT JOIN
    user AS t2
ON
    t1.user_id == t2.id
LEFT JOIN
    note AS t3
ON
    t1.note_id == t3.id
;