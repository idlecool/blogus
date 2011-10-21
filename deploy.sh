#!/bin/bash
#Local Configuration
LOCAL_URL="http://www.blogus.com"
LOCAL_CDN_URL="http://cdn.blogus.com"

#Server Configuration
DEPLOY_URL="http://beta.idlecool.net"
DEPLOY_USERNAME="m"
DEPLOY_CDN_URL="http://cdn.idlecool.net"
DEPLOY_HOST_NAME="ntra.in"
DEPLOY_WSGI_DIR="~/webserver/www.idlecool.net/wsgi"

#App Engine Configuration
GAE_APPCFG="../google_appengine/appcfg.py"
GAE_EMAIL="idlecool@gmail.com"
GAE_APP_DIR="../gae-as-cdn/"

# function definition
function alert {
    echo
    echo -e "\x1B[00;31m"$1"\x1B[00m"
    echo
}

alert "Initiating rsync: Syncing With The Server"
rsync -r -a -v --exclude=LICENSE --exclude=deploy.sh --exclude=logs --exclude=cdn --exclude=app.yaml --exclude=.* -e "ssh -l "$DEPLOY_USERNAME --delete . $DEPLOY_HOST_NAME:$DEPLOY_WSGI_DIR

alert "Syncing the CDN"
rsync -avr --delete cdn/ $GAE_APP_DIR"root"

alert "Uploading CDN to Google AppEngine Servers"
$GAE_APPCFG --email=$GAE_EMAIL --skip_sdk_update_check --no_cookies update $GAE_APP_DIR

alert "Done"