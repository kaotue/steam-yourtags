sam build
sam deploy \
--stack-name steam-yourtags-api \
--s3-bucket steam-yourtags-api \
--capabilities CAPABILITY_NAMED_IAM \
--parameter-overrides SteamApiKey=$STEAM_API_KEY SteamId=$STEAM_ID SteamStrageDomainName=$STEAM_STRAGE_DOMAIN_NAME
