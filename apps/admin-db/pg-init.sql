
-- Create apps table
CREATE TABLE stores (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL);

INSERT INTO stores (name) VALUES
('Google Android'),
('Apple iOS')
;


-- Create apps table
CREATE TABLE apps (
    id SERIAL PRIMARY KEY,
    store INTEGER NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    store_id VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


-- Update networks table to exclude custom networks
CREATE TABLE networks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    postback_id VARCHAR(100) UNIQUE NOT NULL,
    status VARCHAR(10) DEFAULT 'inactive' CHECK (status IN ('active', 'inactive', 'error')), 
    is_custom BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Update app_links to reference only custom_networks
CREATE TABLE app_links (
    id SERIAL PRIMARY KEY,
    app INTEGER NOT NULL REFERENCES apps(id) ON DELETE CASCADE,
    share_id INTEGER UNIQUE NOT NULL,
    network INTEGER NOT NULL REFERENCES networks(id) ON DELETE CASCADE,
    campaign_name VARCHAR(100) NOT NULL,
    campaign_id VARCHAR(100) DEFAULT '',
    ad_name VARCHAR(100) DEFAULT '',
    ad_id VARCHAR(100) DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO networks (name, postback_id, status, is_custom) VALUES
('Google','google', 'inactive', FALSE),
('Meta', 'meta', 'inactive', FALSE),
('AppLovin', 'applovin', 'inactive', FALSE),
('Unity Ads', 'unityads', 'inactive', FALSE),
('Digital Turbine','digitalturbine', 'inactive', FALSE),
('ironSource', 'ironsource', 'inactive', FALSE),
('Social Media Posts', 'customsocial', 'inactive', TRUE)
;


