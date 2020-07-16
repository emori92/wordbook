
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
WHERE
    t2.username == 'test'
;


-- star
SELECT
    t1.id AS id
    , t2.username AS user
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


-- star ranking
SELECT
    RANK() OVER (
        ORDER BY
            COUNT(t1.id) DESC
    ) AS Ranking
    , COUNT(t1.id) AS star_num
    , t1.id AS note_id
    , t2.title AS Note
FROM
    star AS t1
INNER JOIN
    note AS t2
ON
    t1.note_id == t2.id
GROUP BY
    t2.title
;


-- ユーザーid:15の人がフォローしているノートを取得
SELECT
    t2.id
    , t2.username
    , t2.followed_id
    , t1.title
FROM
    note AS t1
INNER JOIN
    -- フォローしているユーザーを取得
    (
    SELECT
        *
    FROM
        user AS t1
    INNER JOIN
        follow AS t2
    ON
        t1.id == t2.following_id
    WHERE
        t2.following_id == 18
    ) AS t2
-- フォローされたユーザーでノートテーブルと結合
ON
    t1.user_id == t2.followed_id
WHERE
    t1.public == 1
ORDER BY
    t1.created_at
;
