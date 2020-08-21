
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
    u.id
    , u.username
    , f.followed_id
    , n.title
-- フォロー
FROM
    follow AS f
-- ノート
INNER JOIN
    note AS n
ON
    n.user_id == f.followed_id
-- ユーザー
INNER JOIN
    user AS u
ON
    u.id == f.following_id
WHERE
    u.username == 'test'
AND
    n.public == 1
ORDER BY
    n.created_at
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
        t2.following_id == 15
    ) AS t2
-- フォローされたユーザーでノートテーブルと結合
ON
    t1.user_id == t2.followed_id
WHERE
    t1.public == 1
ORDER BY
    t1.created_at
;


-- insert review
BEGIN TRANSACTION;
    INSERT INTO
        review
    VALUES
        (1, 15, 1)
    ;

    SELECT * FROM review;
ROLLBACK;
-- COMMIT;
SELECT * FROM review;


-- ユーザー名、復習、問題を抽出
SELECT
    qr.id
    , q.id AS question_id
    , q.question
    , q.hint
    , q.answer
    , qr.review_id
    , qr.review
    , qr.user_id
FROM
    question AS q
-- question review
INNER JOIN
    (
        SELECT
            qr.id
            , qr.question_id
            , r.review_id
            , r.review
            , r.user_id
        FROM
            question_review AS qr
        -- review user
        INNER JOIN
            (
                SELECT
                    r.id AS review_id
                    , r.review
                    , u.id AS user_id
                FROM
                    review AS r
                INNER JOIN
                    user AS u
                ON
                    r.user_id == u.id
                -- WHERE
                --     u.id == 16
            ) AS r
        ON
            qr.review_id = r.review_id
    ) AS qr
ON
    q.id == qr.question_id
;


SELECT
    n.title
    , t.name
FROM
    note_tag AS nt
    LEFT JOIN
        note AS n
    ON nt.note_id == n.id
    LEFT JOIN
        tag AS t
    ON nt.tag_id == t.id
;


-- tagのランキング
SELECT

FROM
    tag AS t
    LEFT JOIN
        note_tag AS nt
    ON t.id == nt.tag_id
