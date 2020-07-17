
# HotListViewで利用するクエリを記述
hot_query = '''

    -- ユーザーがフォローしているノートを取得
    SELECT
        n.id AS note_id
        , n.title AS title
        , n.describe AS describe
        , u1.id                                        -- pkのため名前変更不可
        , u1.followed_id AS followed_id
        , u2.username
    FROM
        note AS n
    INNER JOIN
    
        -- フォローしているユーザーを取得
        (
        SELECT
            *
        FROM
            user AS u
        INNER JOIN
            follow AS f
        ON
            u.id == f.following_id
        WHERE
            f.following_id == %s
        ) AS u1
    ON
        n.user_id == u1.followed_id                 -- フォローされたユーザーでnoteテーブルと結合
    INNER JOIN
        user AS u2                                  -- フォローしているユーザーの名前を取得
    ON
        u1.followed_id == u2.id
    WHERE
        n.public == 1
    ORDER BY
        n.created_at

'''
