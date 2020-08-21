dweet_feeds_query = """

SELECT ad.id, ad.dweet, au.username, CASE when likes_count is NULL then 0 else likes_count end, 
CASE when comments_count is NULL then 0 else comments_count end, 
ad.creation_timestamp, ad.user_id, CONCAT(au.first_name,' ', au.last_name) AS "fullname",
profile.profile_photo,
EXISTS(SELECT U0.id, U0.dweet_id, U0.liked_by_id, U0.last_update FROM api_likes U0 WHERE (U0.dweet_id = ad.id
AND U0.liked_by_id = __CURRENT_USER_ID__)) AS current_user_liked 

from api_dweets as ad INNER JOIN accounts_user as au ON ad.user_id = au.id
LEFT OUTER JOIN
(
    SELECT dweet_id, COUNT(*) as likes_count FROM api_likes GROUP BY dweet_id
) as likes
ON ad.id = likes.dweet_id
LEFT OUTER JOIN
(
    SELECT dweet_id, COUNT(*) as comments_count FROM api_comments GROUP BY dweet_id
) as comnt
ON ad.id = comnt.dweet_id
INNER JOIN profiles_profile as profile ON au.id = profile.user_id
WHERE profile.id in ( __PROFILE_IDS__ )
order by ad.creation_timestamp DESC

"""