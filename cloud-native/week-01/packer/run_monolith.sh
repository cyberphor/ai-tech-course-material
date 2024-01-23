#!/bin/bash
#TODO: Add in other environment variables and fill from terraform output.
MYSQL_HOST=shared-mysql-fs-cpwkwjpr.mysql.database.azure.com
MYSQL_USER=Monolithic_CloudChat_123
MYSQL_PASSWORD=Monolithic_CloudChat_123
SPRING_REDIS_HOST=redis-cache-vpxufblg.redis.cache.windows.net
SPRING_REDIS_PASSWORD=d5OkJ91ujR320LQJcziHXBTlozDdKultqAzCaENFU28=
SPRING_REDIS_PORT=6379
cd /home/packer/cloudchat/task1-monolith/
/bin/java -jar ./target/cloudchat-1.0.0.jar