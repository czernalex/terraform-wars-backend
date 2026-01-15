# Terraform Wars - Backend

## TODO:
- Define roles per project, that need to be granted to the user service account
- Deploy the cloud run job that executes terraform code
- Add terraform code validation (syntax, rce detection, etc., support for variables)
- Add default apis per project (author of the project can decide which apis to enable by default)
- Add Terraform Step Submission evaluation -> script that can evaluate either terraform state or user for example gcloud cli api to truly evaluate the created resources
