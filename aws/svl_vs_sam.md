#Overview

1. AWS Server Application Model (SAM) and Serverless Framework (SVL) are both used to create Lambdas (basically the serverless stack).
2. SVL can help create the serverless stack even on other providers other than AWS.
3. SAM is built to work well with various AWS components.
4. SVL supports plugins, SAM has decided against it.
5. Behind the scenes, they both create CloudFormation stack, which creates all our resources. It's a syntactical sugar (and a feature superset) of Cloudformation.


#Feature Comparison
1. Using existing VPC instead of creating a new one - both SVL and SAM can do this. 
 - https://stackoverflow.com/questions/50498620/serverless-framework-add-lambda-to-an-existing-vpc-and-subnet
 - https://github.com/awslabs/serverless-application-model/tree/master/examples/2016-10-31/hello_world_vpc
2. Lambdas can be given an S3 bucket to pick up the deployable. Both SAM and Serverless can create this bucket, or you can specify an existing one. They both have the following mechanism of providing an existing bucket 
 - https://medium.com/@oieduardorabelo/reusing-s3-bucket-for-multiple-serverless-framework-projects-deploy-828e3a45f713
 - https://aws.amazon.com/blogs/compute/a-simpler-deployment-experience-with-aws-sam-cli/
3. SVL can setup a trigger, so that the lambda listens to changes to an 'existing' and a 'new' S3 bucket. SAM can do this only for a new bucket.


