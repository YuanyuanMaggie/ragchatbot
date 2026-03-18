#!/bin/bash

# Deploy widget files to S3
# Usage: ./deploy-widget-to-s3.sh <bucket-name> <api-url>

set -e  # Exit on error

BUCKET_NAME="${1}"
API_URL="${2}"

if [ -z "$BUCKET_NAME" ]; then
    echo "❌ Usage: ./deploy-widget-to-s3.sh <bucket-name> <api-url>"
    echo "   Example: ./deploy-widget-to-s3.sh yuanyuanli.com https://xxx.us-east-1.cs.amazonlightsail.com"
    exit 1
fi

if [ -z "$API_URL" ]; then
    echo "❌ API URL is required"
    echo "   Example: https://xxx.us-east-1.cs.amazonlightsail.com"
    exit 1
fi

echo "🚀 Deploying widget to S3..."
echo "Bucket: $BUCKET_NAME"
echo "API URL: $API_URL"
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check if bucket exists
echo "📋 Checking if bucket exists..."
if ! aws s3 ls "s3://$BUCKET_NAME" &> /dev/null; then
    echo "❌ Bucket '$BUCKET_NAME' not found or no access"
    exit 1
fi

echo "✅ Bucket found"

# Create temp directory for modified files
TEMP_DIR=$(mktemp -d)
echo "📁 Created temp directory: $TEMP_DIR"

# Copy widget files to temp directory
cp frontend/widget.html "$TEMP_DIR/"
cp frontend/widget.css "$TEMP_DIR/"
cp frontend/widget.js "$TEMP_DIR/"

# Update API_URL in widget.js
echo ""
echo "🔧 Updating API URL in widget.js..."
sed -i.bak "s|const API_URL = '/api';|const API_URL = '${API_URL}/api';|g" "$TEMP_DIR/widget.js"
rm "$TEMP_DIR/widget.js.bak" 2>/dev/null || true

echo "✅ API URL updated"

# Add cache-busting version parameter
VERSION=$(date +%Y%m%d%H%M%S)
echo ""
echo "📦 Version: $VERSION"

# Upload files to S3
echo ""
echo "📤 Uploading files to S3..."

# Upload with proper content types and cache headers
aws s3 cp "$TEMP_DIR/widget.html" "s3://$BUCKET_NAME/widget.html" \
    --content-type "text/html" \
    --cache-control "public, max-age=300" \
    --metadata version="$VERSION"

aws s3 cp "$TEMP_DIR/widget.css" "s3://$BUCKET_NAME/widget.css" \
    --content-type "text/css" \
    --cache-control "public, max-age=3600" \
    --metadata version="$VERSION"

aws s3 cp "$TEMP_DIR/widget.js" "s3://$BUCKET_NAME/widget.js" \
    --content-type "application/javascript" \
    --cache-control "public, max-age=300" \
    --metadata version="$VERSION"

# Make files public
echo ""
echo "🔓 Making files public..."

aws s3api put-object-acl --bucket "$BUCKET_NAME" --key widget.html --acl public-read
aws s3api put-object-acl --bucket "$BUCKET_NAME" --key widget.css --acl public-read
aws s3api put-object-acl --bucket "$BUCKET_NAME" --key widget.js --acl public-read

# Clean up
rm -rf "$TEMP_DIR"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Widget Deployment Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Widget URLs:"
echo "  HTML: https://${BUCKET_NAME}/widget.html"
echo "  CSS:  https://${BUCKET_NAME}/widget.css"
echo "  JS:   https://${BUCKET_NAME}/widget.js"
echo ""
echo "Test widget:"
echo "  https://${BUCKET_NAME}/widget.html"
echo ""
echo "Next steps:"
echo "1. Test the widget at the URL above"
echo "2. Add widget code to your index.html"
echo "3. Upload updated index.html to S3"
echo ""
echo "Embed code for your website:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat <<'EOF'

<!-- Add before </body> tag -->
<link rel="stylesheet" href="/widget.css">

<button id="chatWidgetButton" class="chat-widget-button" aria-label="Open chat">
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
    </svg>
    <span id="notificationBadge" class="notification-badge" style="display: none;">0</span>
</button>

<div id="widgetContainer" class="widget-container">
    <!-- Copy entire widget-container content from widget.html lines 11-111 -->
</div>

<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="/widget.js"></script>

EOF
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if CloudFront is being used
echo "💡 Tip: If using CloudFront, invalidate cache:"
echo "   aws cloudfront create-invalidation --distribution-id YOUR_ID --paths '/widget*'"
echo ""
