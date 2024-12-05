# Budget

It would be good to keep the project with an estimated cloud cost of less than $100 a month, but that is just a soft goal as it is difficult to design for both large and small usecases at the same time. Additionally, various differences in cloud pricing make a difference as well.

Currently the project is able to run on a single server with 4GB of RAM. It would be nice to get this down to 2GB but this might be constrained by the OLAP database. Having the ability to switch between a smaller transactional database like PostgreSQL and a OLAP database like Clickhouse would be a good way to support both small and large usecases but would add complexity.

# Pricing

Self-hosted is free of charge. OpenAttribution is currently in a pre-alpha stage and has no hosted/paid versions available. At some point in the future a hosted version may be provided for customers that want to avoid the management overhead of self-hosting.

