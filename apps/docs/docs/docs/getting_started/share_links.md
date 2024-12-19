# Share Links

Share links are setup on your OpenAttribution dashbaord, after adding your apps, at `/links` on your OpenAttribution dash. The suggested way to setup links is to setup a subdomain for share links like `app.yourdomain.com` (links like `app.yourdomain.com/{ShareID}`) or a suffix at your domain like `yourdomain.com/app/` with links like `yourdomain.com/app/{ShareID}`. You can also not use a subdomain and just use the domain like `yourdomain.com/{ShareID}`, but this will require setting nginx config for each new url as well as being careful to not have any other urls that could conflict with the share links, including APIs.

## Nginx Config

The following is an example of an nginx config for `app.yourdomain.com` that will proxy share links to the OpenAttribution Share Links API. Note this example is done before applying any SSL/TLS certificates with certbot.

```nginx
server {
  server_name app.thirdgate.dev;

  listen 80;

  # One option for sharing. Requires at least something set as the suffix
  location / {
    proxy_pass http://localhost:8000/api/links/share$request_uri;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_hide_header 'Access-Control-Allow-Origin';
  }

}
```


https://openattribution.dev/.well-known/apple-app-site-association

https://beasting.app/.well-known/assetlinks.json