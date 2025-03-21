-- NOTE: This has a sibling query in dash-backend
SELECT 
    al.id as db_id,
    d.domain_url as domain_url,
    al.share_slug,
    n.postback_id as network_postback_id,
    n.name as network_name,
    al.campaign_name,
    al.ad_name,
    al.created_at,
    al.web_landing_page,
    ga.store_id as google_store_id,
    aa.store_id as apple_store_id
FROM app_links al
LEFT JOIN networks n ON al.network = n.id
LEFT JOIN client_domains d ON al.client_domain = d.id
LEFT JOIN apps ga ON al.google_app_id = ga.id
LEFT JOIN apps aa ON al.apple_app_id = aa.id
;
