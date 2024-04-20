# Sample SAM Templates

This repository contains sample SAM (Serverless Application Model) templates for various AWS services.

## Contents

- [Complex SAM Template](#complex-sam-template)
- [luk_data_etl SAM Template](#luk_data_etl-sam-template)
- [luk_data_etl Redshift SAM Template](#luk_data_etl-redshift-sam-template)
- [luk_data_etl Glue Service SAM Template](#luk_data_etl-glue-service-sam-template)

---

## Complex SAM Template

### Description

Sample SAM Template for a complex SAM application.

### Parameters

- **Stage**: The deployment stage for the application. Default value is `dev`.

### Resources

- **Infra**: Deploys infrastructure using a SAM application.
- **School**: Deploys school-related resources using another SAM application.

---

## luk_data_etl SAM Template

### Description

Sample SAM Template for data extraction, transformation, and loading.

### Parameters

- **Stage**: The deployment stage for the application. Default value is `dev`.
- **Department**: The department for the application.

### Resources

- **S3Bucket**: Creates an S3 bucket for storing data sources.
- **Teacher**: Deploys a Glue service for data transformation.

---

## luk_data_etl Redshift SAM Template

### Description

Sample SAM Template for setting up a Redshift cluster for data processing.

### Parameters

- **Stage**: The deployment stage for the application. Default value is `dev`.

### Resources

- **RedshiftSecurityGroup**: Sets up security group for Redshift.
- **GlueRedshiftConnection**: Creates a Glue connection to Redshift.
- **GlueJobRole**: Defines an IAM role for Glue service.
- **S3Bucket**: Creates an S3 bucket for data storage.
- **S3BucketReject**: Creates an S3 bucket for rejected data.
- **GlueS3Bucket**: Creates an S3 bucket for Glue assets.
- **EventbridgeGlueRole**: Sets up IAM role for EventBridge invocation of Glue.

### Outputs

- **GlueRedshiftConnection**: Glue connection to Redshift.
- **GlueJobRole**: IAM role for Glue service.
- **EventbridgeGlueRoleArn**: IAM role ARN for EventBridge invocation.

---

## luk_data_etl Glue Service SAM Template

### Description

Sample SAM Template for a Glue service.

### Parameters

- **Stage**: The deployment stage for the application. Default value is `dev`.
- **Department**: The department for the Glue service.
- **DataType**: The data type for the Glue service.
- **ExecutionClass**: The execution class for the Glue job. Default value is `STANDARD`.

### Resources

- **GlueJob**: Creates a Glue job for data transformation.
- **GlueWorkflow**: Defines a Glue workflow for managing the job execution.
- **GlueTrigger**: Sets up a trigger for the Glue job.
- **GlueEventRule**: Defines an EventBridge rule for triggering the Glue workflow.

