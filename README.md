# Janus Backup

## Motivation

Main goal of this project is to make simple, expandable tool for backuping most popular DBs, such as PostgreSQL,
MongoDB, MySQL and etc.

It is based on:

* [FastAPI](https://github.com/tiangolo/fastapi) as API server
* [Schedule](https://github.com/dbader/schedule) as worker / scheduler
* [SQLAlchemy](https://www.sqlalchemy.org/) and SQLite to store data about hosts and DBs

## Usage

Currently Janus Backup tool supports only worker mode with file configurations.

Steps to start worker:

* Create config file (example: [.config/template.config.json](.config/template.config.json))
* Create projects setting file (example: [.config/template.projects.json](.config/template.projects.json))
* Run worker with command:

```bash
python -m janusbackup worker --config-type file --config-path ./{path_to_your_config}
```

## Installation

TBD

## Roadmap

- [ ] Complete worker / cron
- [ ] Complete API server
- [ ] Prepare for easy deployment
- [ ] Documentation
- [ ] Unit tests
- [ ] Logs, metrics, notifications
- [ ] More DBs, storages and etc.

## License

[MIT](https://choosealicense.com/licenses/mit/)
