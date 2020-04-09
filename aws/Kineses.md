# Kinesis is a real time data analysis tool from AWS. It can  also be used to feed stream data to multiple applications at once.

# By default data is persisted in the stream for 1 day. Can be configured for max 7 days.

# Kinesis uses shards to store data into chunks.


How to use Kinesis?

# Create kinesis stream from aws dashboard

# Describe stream
$ aws kinesis describe-stream --stream-name <stream-name> --profile <aws-profile-name>

# Add data to stream
# partition key decides the shard where to store data. key -> MD5 hash function - 128 bit integer
$ aws kinesis put-record --stream-name <stream-name> --partition-key <key> --data <your-data> --profile <aws-profile-name>

# Generate iterator to iterate over all data in a single shard
$ aws kinesis get-shard-iterator --stream-name <stream-name> --shard-iterator-type <iterator type> --shard-id <shard-id> --profile <aws-profile-name>

# Iterate over data
# Data is encoded in base64
kineses get-records --shard-iterator <iterator-name> --limit <no-of-records> --profile <aws-profile-name> --profile <aws-profile-name>


