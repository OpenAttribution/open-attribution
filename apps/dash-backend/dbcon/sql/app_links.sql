-- NOTE: This has a sibling query in postback-api
SELECT 
    al.id as db_id,
    d.domain_url as domain_url,
    al.share_slug,
    n.name as network_name,
    al.campaign_name,
    al.ad_name,
    al.created_at,
    ga.name as google_app_name,
    aa.name as apple_app_name
FROM app_links al
LEFT JOIN networks n ON al.network = n.id
LEFT JOIN client_domains d ON al.client_domain = d.id
LEFT JOIN apps ga ON al.google_app_id = ga.id
LEFT JOIN apps aa ON al.apple_app_id = aa.id
;
