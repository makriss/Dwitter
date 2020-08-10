get_liked_dweets_by_profile_query = """
SELECT ad.id, ad.dweet, likes_count, CASE when comments_count is NULL then 0 else comments_count end, 
ad.creation_timestamp, ad.user_id, dweeter.username,  CONCAT(dweeter.first_name,' ', dweeter.last_name) AS "fullname",

EXISTS(SELECT U0.id, U0.dweet_id, U0.liked_by_id, U0.last_update FROM api_likes U0 WHERE (U0.dweet_id = al.dweet_id 
AND U0.liked_by_id = __CURRENT_USER_ID__)) AS current_user_liked 

from api_likes as al INNER JOIN api_dweets as ad on al.dweet_id = ad.id 
INNER JOIN accounts_user as au ON al.liked_by_id = au.id
INNER JOIN accounts_user as dweeter ON ad.user_id = dweeter.id
INNER JOIN
(
    SELECT dweet_id, COUNT(*) as likes_count FROM api_likes GROUP BY dweet_id
) as likes
ON al.dweet_id = likes.dweet_id
LEFT JOIN
(
    SELECT dweet_id, COUNT(*) as comments_count FROM api_comments GROUP BY dweet_id
) as comnt
ON al.dweet_id = comnt.dweet_id

WHERE au.username='__PROFILE_USERNAME__'
order by al.last_update DESC
"""
