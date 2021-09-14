# Configuration from files

Supported configuration file formats:

* json
* yaml / yml
* toml

### Global config file

Required keys for config file (global config):

Example located in [./config/template.config.json](./template.config.json)

* DEBUG - is debug mode
* ENV - enviroment
* PROJECTS_SETTINGS_FILEPATH - location of projects config file
* S3_URL - S3 Location
* S3_ACCESS_KEY - S3 Access Key
* S3_SECRET_KEY - S3 Secret Key
* S3_BUCKET - S3 Bucket title

### Projects config file

Projects must be set for 'projects' key in root

Example located in [./config/template.config.json](./template.config.json)

Required keys for each project:
* title - project name
* connection_type - Connection to DB. Allowed: 'direct', 'ssh_tunnel'.
* db_type - DB type. Allowed: 'mongodb', 'postgresql'.
* db_host - DB host URL
* db_port - DB port
* db_username - DB username
* db_password - DB password
* db_name - DB name
* connection_params - Dict of params, which will be added to generated URI
* db_uri - URI. Rewrites settings above
* ssh_tunnel - TBD
