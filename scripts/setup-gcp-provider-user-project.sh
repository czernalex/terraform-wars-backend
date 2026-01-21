#!/usr/bin/env bash
set -euo pipefail

# -------------------------
# Constants (DO NOT EDIT)
# -------------------------
GCP_SA_NAME="terraform-wars-sa"
GCP_SA_DISPLAY_NAME="Terraform Wars Service Account"

TW_GCP_SA_EMAIL="twa-be-cloudrun-runtime-sa@terraform-wars-dev.iam.gserviceaccount.com"

# -------------------------
# Defaults
# -------------------------
CREATE_PROJECT=false
LINK_BILLING=false

# -------------------------
# Usage
# -------------------------
usage() {
  cat <<EOF
Usage: $0 [options]

Required:
  --project-id ID               GCP project ID
  --project-name NAME           GCP project name

Optional:
  --billing-account ID          GCP billing account ID
  --create-project              Actually create the GCP project
  --link-billing                Actually link the billing account
  -h, --help                    Show this help message

Examples:
  $0 --project-id my-project --project-name "My Project" --create-project
  $0 --project-id my-project --project-name "My Project" --link-billing --billing-account XXXX
EOF
}

# -------------------------
# Parse arguments
# -------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-id)
      GCP_PROJECT_ID="$2"
      shift 2
      ;;
    --project-name)
      GCP_PROJECT_NAME="$2"
      shift 2
      ;;
    --billing-account)
      GCP_BILLING_ACCOUNT_ID="$2"
      shift 2
      ;;
    --create-project)
      CREATE_PROJECT=true
      shift
      ;;
    --link-billing)
      LINK_BILLING=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1"
      usage
      exit 1
      ;;
  esac
done

# -------------------------
# Validate required args
# -------------------------
: "${GCP_PROJECT_ID:?Missing --project-id}"
: "${GCP_PROJECT_NAME:?Missing --project-name}"

if [[ "${LINK_BILLING}" == true && -z "${GCP_BILLING_ACCOUNT_ID:-}" ]]; then
  echo "Error: --link-billing requires --billing-account"
  exit 1
fi

# -------------------------
# Auth
# -------------------------
echo "Authenticating to Google Cloud..."
gcloud auth login

# -------------------------
# Create GCP project
# -------------------------
if [[ "${CREATE_PROJECT}" == true ]]; then
  echo "Creating new project: ${GCP_PROJECT_ID}"
  gcloud projects create "${GCP_PROJECT_ID}" \
    --name="${GCP_PROJECT_NAME}"
else
  echo "Skipping project creation"
fi

echo "Setting active project..."
gcloud config set project "${GCP_PROJECT_ID}"

# -------------------------
# Link billing account to project
# -------------------------
if [[ "${LINK_BILLING}" == true ]]; then
  echo "Linking billing account to project..."
  gcloud billing projects link "${GCP_PROJECT_ID}" \
    --billing-account="${GCP_BILLING_ACCOUNT_ID}"
else
  echo "Skipping billing account linking"
fi

# -------------------------
# Create service account
# -------------------------
echo "Creating new service account: ${GCP_SA_NAME}"
gcloud iam service-accounts create "${GCP_SA_NAME}" \
  --display-name="${GCP_SA_DISPLAY_NAME}"

GCP_SA_EMAIL="${GCP_SA_NAME}@${GCP_PROJECT_ID}.iam.gserviceaccount.com"

echo "Granting roles/owner to ${GCP_SA_EMAIL} on project..."
gcloud projects add-iam-policy-binding "${GCP_PROJECT_ID}" \
  --member="serviceAccount:${GCP_SA_EMAIL}" \
  --role="roles/owner"

echo "Granting roles/iam.serviceAccountTokenCreator to ${TW_GCP_SA_EMAIL} on ${GCP_SA_EMAIL}..."
gcloud iam service-accounts add-iam-policy-binding "${GCP_SA_EMAIL}" \
  --member="serviceAccount:${TW_GCP_SA_EMAIL}" \
  --role="roles/iam.serviceAccountTokenCreator"

echo "All steps completed successfully."
