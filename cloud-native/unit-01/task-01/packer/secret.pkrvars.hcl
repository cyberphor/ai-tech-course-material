# You can define secret build variables here, like the following:

# Packer will use these credentials to access Azure
# if you used Vic's Terraform config for setup, 
# refer to the Step 1 of Task 1 for these values
client_id = "3715b604-fac8-4c62-b4bc-837233192837"
client_secret = "TOW8Q~c7og_VJfyD6jTmHyYMStjiG61DNOuN1aKl"

# the "cloudchat" app will use these to access the SQL database 
mysql_user = "Monolithic_CloudChat_123"
mysql_password = "Monolithic_CloudChat_123"

# the "cloudchat" app will use these to access the Redis message broker service
spring_redis_password = "hTEupVAvFqOm1hdYHNV9twBKRTVnjxtZtAzCaB4Gpqc="