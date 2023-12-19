from confluent_kafka.admin import AdminClient, NewTopic

# Configuration for the AdminClient
admin_config = {"bootstrap.servers": "localhost:9092"}

# Create an instance of AdminClient
admin_client = AdminClient(admin_config)

# Define the topics to be created
topics_to_create = ["impressions", "clicks", "events"]

# Check existing topics
existing_topics = admin_client.list_topics().topics

# Filter out topics that already exist
topics_to_create = [topic for topic in topics_to_create if topic not in existing_topics]

# Define NewTopic objects for each topic that needs to be created
new_topics = [
    NewTopic(topic, num_partitions=1, replication_factor=1)
    for topic in topics_to_create
]

# Create the topics
if new_topics:
    admin_client.create_topics(new_topics=new_topics)
    print(f"Created topics: {', '.join(topics_to_create)}")
else:
    print("All topics already exist.")
