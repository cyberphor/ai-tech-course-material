#!/bin/bash
#TODO: Add in other environment variables and fill from terraform output.
export MYSQL_HOST='shared-mysql-fs-cpwkwjpr.mysql.database.azure.com'
export MYSQL_USER='Monolithic_CloudChat_123'
export MYSQL_PASSWORD='Monolithic_CloudChat_123'
export SPRING_REDIS_HOST='redis-cache-vpxufblg.redis.cache.windows.net'
export SPRING_REDIS_PASSWORD='d5OkJ91ujR320LQJcziHXBTlozDdKultqAzCaENFU28='
export SPRING_REDIS_PORT='6379'
cd /home/packer/
/bin/java -jar ./target/cloudchat-1.0.0.jar