
# HotListViewで利用するクエリを記述
hot_query = """
SELECT
    *
FROM
    note AS n
    INNER JOIN
        custom_user AS u
    ON n.user_id = u.id
WHERE
    u.id IN (
        SELECT
            f.followed_id
        FROM
            follow AS f
        WHERE
            f.following_id = %s
    )
"""
