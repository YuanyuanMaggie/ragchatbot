#!/bin/bash
set -e  # Exit on any error

sam build --no-cached && sam deploy \
  --stack-name yuanyuan-chatbot \
  --region us-east-1 \
  --s3-bucket yuanyuan-chatbot \
  --capabilities CAPABILITY_IAM \
  --force-upload \
  --parameter-overrides "AnthropicApiKey=$ANTHROPIC_API_KEY"