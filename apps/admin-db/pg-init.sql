
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


CREATE TABLE networks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    postback_id VARCHAR(100) UNIQUE NOT NULL,
    status VARCHAR(10) DEFAULT 'inactive' CHECK (status IN ('active', 'inactive', 'error')), 
    is_custom BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE client_domains (
    id SERIAL PRIMARY KEY,
    domain_url VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE app_links (
    id SERIAL PRIMARY KEY,
    client_domain INTEGER NOT NULL,
    share_slug VARCHAR(100) UNIQUE NOT NULL,
    network INTEGER NOT NULL,
    google_app_id INTEGER NULL DEFAULT NULL,
    apple_app_id INTEGER NULL DEFAULT NULL,
    campaign_name VARCHAR(100) NOT NULL,
    ad_name VARCHAR(100) DEFAULT '',
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_domain) REFERENCES client_domains(id) ON DELETE CASCADE,
    FOREIGN KEY (network) REFERENCES networks(id) ON DELETE CASCADE,
    FOREIGN KEY (google_app_id) REFERENCES apps(id) ON DELETE CASCADE,
    FOREIGN KEY (apple_app_id) REFERENCES apps(id) ON DELETE CASCADE
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


