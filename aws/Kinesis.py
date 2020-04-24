from boto import kinesis

aws_profile="learner"

kinesis = kinesis.connect_to_region("us-east-1")

description = kinesis.describe_stream("pharmacy-records")

print(description)
