#!/bin/bash

# Configuration commune
TAG="v1.0"
RELEASE_TITLE="Saadiya AI v1.0"
RELEASE_NOTES="Stable release with all features for Saadiya AI."
FILE_PATH="/path/to/SaadiyaInstaller.exe"  # Remplacez par le chemin de votre .exe
FILE_NAME="SaadiyaInstaller.exe"

# ===== GitHub =====
GITHUB_TOKEN="your_github_token_here"
GITHUB_REPO="your_username/your_repository"
echo "Publishing on GitHub..."
RELEASE_ID=$(curl -s -X POST https://api.github.com/repos/$GITHUB_REPO/releases \
  -H "Authorization: token $GITHUB_TOKEN" \
  -d "{\"tag_name\": \"$TAG\", \"name\": \"$RELEASE_TITLE\", \"body\": \"$RELEASE_NOTES\"}" | jq -r .id)
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  -H "Content-Type: application/octet-stream" \
  --data-binary @"$FILE_PATH" \
  "https://uploads.github.com/repos/$GITHUB_REPO/releases/$RELEASE_ID/assets?name=$FILE_NAME"

# ===== GitLab =====
GITLAB_TOKEN="your_gitlab_token_here"
GITLAB_REPO_ID="your_gitlab_repo_id_here"
echo "Publishing on GitLab..."
UPLOAD_URL=$(curl -s -X POST https://gitlab.com/api/v4/projects/$GITLAB_REPO_ID/uploads \
  -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  -F "file=@$FILE_PATH" | jq -r .url)
echo "File uploaded to GitLab at $UPLOAD_URL"

# ===== Bitbucket =====
BITBUCKET_TOKEN="your_bitbucket_token_here"
BITBUCKET_REPO="your_username/your_repository"
echo "Publishing on Bitbucket..."
curl -X POST -u $BITBUCKET_TOKEN:x-oauth-basic \
  -F files=@"$FILE_PATH" \
  https://api.bitbucket.org/2.0/repositories/$BITBUCKET_REPO/downloads

# ===== SourceForge =====
SF_USER="your_username"
SF_PASS="your_password"
SF_PROJECT="your_project_name"
echo "Publishing on SourceForge..."
pscp -pw $SF_PASS "$FILE_PATH" $SF_USER@web.sourceforge.net:/home/frs/project/$SF_PROJECT/releases/

# ===== AWS S3 =====
AWS_BUCKET_NAME="your_bucket_name"
echo "Uploading to AWS S3..."
aws s3 cp "$FILE_PATH" "s3://$AWS_BUCKET_NAME/releases/$FILE_NAME"

# ===== Google Drive =====
GOOGLE_ACCESS_TOKEN="your_google_drive_access_token_here"
echo "Uploading to Google Drive..."
curl -X POST -L -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
  -F "metadata={name :\"$FILE_NAME\"};type=application/json;charset=UTF-8" \
  -F "file=@$FILE_PATH;type=application/octet-stream" \
  "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"

# ===== Dropbox =====
DROPBOX_TOKEN="your_dropbox_token_here"
echo "Uploading to Dropbox..."
curl -X POST https://content.dropboxapi.com/2/files/upload \
  --header "Authorization: Bearer $DROPBOX_TOKEN" \
  --header "Dropbox-API-Arg: {\"path\": \"/releases/$FILE_NAME\", \"mode\": \"add\", \"autorename\": true, \"mute\": false}" \
  --header "Content-Type: application/octet-stream" \
  --data-binary @"$FILE_PATH"

# ===== Mega.nz =====
MEGA_USER="your_mega_email"
MEGA_PASS="your_mega_password"
echo "Uploading to Mega.nz..."
megatools put --username="$MEGA_USER" --password="$MEGA_PASS" "$FILE_PATH"

# ===== OneDrive =====
ONEDRIVE_ACCESS_TOKEN="your_onedrive_access_token_here"
echo "Uploading to OneDrive..."
curl -X PUT "https://graph.microsoft.com/v1.0/me/drive/root:/releases/$FILE_NAME:/content" \
  -H "Authorization: Bearer $ONEDRIVE_ACCESS_TOKEN" \
  --data-binary @"$FILE_PATH"

echo "All platforms have been processed."
