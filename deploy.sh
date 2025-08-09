#!/bin/bash

echo "🚀 Deploying JKIA Aircraft Landing Notifier..."

# Initialize Terraform if needed
if [ ! -d ".terraform" ]; then
    echo "📦 Initializing Terraform..."
    terraform init
fi

# Plan the deployment
echo "📋 Planning deployment..."
terraform plan

# Ask for confirmation
read -p "🤔 Do you want to proceed with the deployment? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔨 Applying Terraform configuration..."
    terraform apply -auto-approve
    
    echo ""
    echo "✅ Deployment complete!"
    echo ""
    echo "📧 Important: Check your email and confirm the SNS subscription!"
    echo "🔔 You should receive a confirmation email shortly."
    echo ""
    echo "📊 To check logs:"
    echo "   aws logs tail /aws/lambda/jkia-landing-notifier --follow"
    echo ""
else
    echo "❌ Deployment cancelled."
fi