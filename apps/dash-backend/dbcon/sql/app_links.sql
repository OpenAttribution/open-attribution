SELECT 
    al.share_slug,
    n.name as network_name,
    al.campaign_name,
    al.ad_name,
    al.created_at
FROM app_links al
LEFT JOIN networks n
ON al.network = n.id
WHERE al.play_store_app = :app OR al.ios_app = :app
;