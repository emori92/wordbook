
# HotListViewで利用するクエリを記述
hot_query = '''

    -- ユーザーがフォローしているノートを取得
    SELECT
        n.id AS pk
        , n.title AS title
        , n.describe AS describe
        , n.star_num
        , u1.id                                        -- pkのため名前変更不可
        , u1.followed_id AS user_pk
        , u2.username
    FROM
        (
            SELECT
                n.id
                , n.title
                , n.describe
                , n.user_id
                , n.public
                , n.created_at
                , COUNT(n.id) AS star_num              -- noteのstar数を集計
            FROM
                note AS n
                INNER JOIN
                    star AS s
                ON n.id == s.note_id
            GROUP BY
                n.id
            ORDER BY
                star_num DESC
        ) AS n
    INNER JOIN
    
        -- フォローしているユーザーを取得
        (
        SELECT
            *
        FROM
            user AS u
            INNER JOIN
                follow AS f
                ON u.id == f.following_id
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
