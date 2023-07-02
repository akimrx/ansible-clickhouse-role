Clickhouse
==========

Clickhouse role.
Supported service managers: 
- `systemd`
- `docker`

Tested via `systemd` on the:
- Ubuntu 18.04 bionic
- Ubuntu 20.04 focal
- Ubuntu 22.04 jammy

Tested via `docker` on the:
- Ubuntu 18.04 bionic
- Ubuntu 20.04 focal

Install role
------------

* Install using `ansible-galaxy`:

```shell
ansible-galaxy role install https://github.com/akimrx/ansible-clickhouse-role.git
```

* Lastest version:
```shell
ansible-galaxy role install https://github.com/akimrx/ansible-clickhouse-role.git,master
```

* Upgrade to latest:
```shell
ansible-galaxy role install https://github.com/akimrx/ansible-clickhouse-role.git --upgrade
```

* Using `requirements.yml` file for Ansible Galaxy:
```yaml
---
roles:
  - name: clickhouse
    src: https://github.com/akimrx/ansible-clickhouse-role.git
    type: git
    version: master
```

Command for install: `ansible-galaxy role install -r requirements.yml`



Prepare & running tests locally
-------------------------------

```shell
mkdir ~/ansible-collections/
cd ~/ansible-collections/
git clone https://github.com/akimrx/ansible-clickhouse-role.git
cd clickhouse

python3 -m venv venv
source venv/bin/activate

pip3 install -r test-requirements.txt


molecule -v test default  # test default scenario with systemd service manager
molecule -v test docker  # test alternative scenario with docker service manager
```


Role Variables
--------------

#### Common system variables

| Variable | Type | Default | Choices | Description |
|----------|------|---------|---------|-------------|
| `clickhouse_service_manager` | `str` | `systemd` | `systemd, docker` | service manager for clickhouse-server |
| `clickhouse_base_dir_root` | `str` | `/opt` | `-` | parent common base dir |
| `clickhouse_base_dir_config` | `str` | `{{ clickhouse_base_dir_root }}/conf` | `-` | parent common config dir |
| `clickhouse_base_dir_data` | `str` | `{{ clickhouse_base_dir_root }}/data` | `-` | parent common data dir |
| `clickhouse_base_dir_log` | `str` | `{{ clickhouse_base_dir_root }}/log` | `-` | parent common dir for logs |
| `clickhouse_base_dir_library` | `str` | `{{ clickhouse_base_dir_root }}/lib` | `-` | parent common dir for library files |
| `clickhouse_base_dir_temp` | `str` | `{{ clickhouse_base_dir_root }}/tmp` | `-` | parent common dir for temp files |
| `clickhouse_dir_data` | `str` | `{{ clickhouse_base_dir_data }}/clickhouse` | `-` | specific data dir for service |
| `clickhouse_dir_config` | `str` | `{{ clickhouse_base_dir_config }}/clickhouse` | `-` | specific config dir for service |
| `clickhouse_dir_log` | `str` | `{{ clickhouse_base_dir_log }}/clickhouse` | `-` | specific logs dir for service |
| `clickhouse_dir_temp` | `str` | `{{ clickhouse_base_dir_temp }}/clickhouse` | `-` | specific dir for CH temp files |
| `clickhouse_dir_ssl` | `str` | `{{ clickhouse_dir_config }}/ssl` | `-` | specific dir for CH SSL files |
| `clickhouse_dir_library` | `str` | `{{ clickhouse_base_dir_library }}/clickhouse` | `-` | specific dir for CH library files |
| `clickhouse_dir_user_files` | `str` | `{{ clickhouse_dir_library }}/user_files` | `-` | specific dir for CH user files |
| `clickhouse_dir_format_schemas` | `str` | `{{ clickhouse_dir_library }}/format_schemas` | `-` | specific dir for CH format schemas |
| `clickhouse_general_owner` | `str` | `root` | `-` | general user for parent dirs and common files |
| `clickhouse_system_user` | `str` | `clickhouse` | `-` | user for clickhouse dirs and service |
| `clickhouse_system_group` | `str` | `clickhouse` | `-` | group for clickhouse dirs and service |
| `clickhouse_apt_repository_repo` | `str` | `deb https://packages.clickhouse.com/deb stable main` | `-` | apt repository with CH packages |
| `clickhouse_apt_repository_key_id` | `str` | `8919F6BD2B48D754` | `-` | key for apt repository |
| `clickhouse_apt_repository_key_server` | `str` | `hkp://keyserver.ubuntu.com:80` | `-` | apt repository key server |

#### Clickhouse DBMS specific variables

| Variable | Type | Default | Choices | Description |
|----------|------|---------|---------|-------------|
| `clickhouse_version` | `str` | `22.1.3.7` | `-` | clickhouse packages version |
| `clickhouse_prompt` | `str` | `{{ inventory_hostname }} - clickhouse` | `-` | display name for clickhouse shell |
| `clickhouse_default_database_name` | `str` | `default` | `-` | default database for CH (autocreate) |
| `clickhouse_default_profile` | `str` | `default` | see `clickhouse_user_profiles_default` | the default profile for users who don't have it |
| `clickhouse_macros_shard_name` | `str` | `01` | `-` | macros name for sharding |
| `clickhouse_macros_replica_name` | `str` | `{{ inventory_hostname }}` | `-` | macros name for replica identifier |
| `clickhouse_listen_hosts` | `list` | `["::"]` | `-` | listen addresses |
| `clickhouse_listen_reuse_port` | `bool` | `true` | `true, false` | allow clickhouse to reuse listen port for many hosts |
| `clickhouse_listen_try` | `int` | `1` | `-` | number of attempts to listen a port |
| `clickhouse_listen_backlog` | `int` | `4096` | `-` | TCP listen backlog for clickhouse |
| `clickhouse_listen_port_mysql` | `int` | `-` | `-` | MySQL-compatible Clickhouse port, disabled by default |
| `clickhouse_listen_port_tcp` | `int` | `9000` | `-` | clickhouse tcp port |
| `clickhouse_listen_port_http` | `int` | `8123` | `-` | clickhouse http port |
| `clickhouse_listen_port_interserver` | `int` | `9009` | `-` | clickhouse interserver port |
| `clickhouse_enable_secure_protocols` | `bool` | `false` | `true, false` | enable SSL/TLS protocols |
| `clickhouse_ssl_certificate` | `str` (certificate content) | `""` | `-` | Public x509 SSL certificate content |
| `clickhouse_ssl_private_key` | `str` (private key content) | `""` | `-` | Private OpenSSL key content | 
| `clickhouse_listen_port_https` | `int` | `8443` | `-` | clickhouse https port |
| `clickhouse_listen_port_tcp_secure` | `int` | `9440` | `-` | clickhouse secure tcp port |
| `clickhouse_zookeeper_enabled` | `bool` | `false` | `true, false` | use zookeeper for replication |
| `clickhouse_zookeeper_hosts` | `list[dict]` | `-` | `[{ 'fqdn': 'zoo1.example.com', 'port': 2181 }, { ... }]` | list of zookeeper hosts |
| `clickhouse_zookeeper_session_timeout_ms` | `int` | `30000` | `-` | Timeout for ZK session in milliseconds |
| `clickhouse_zookeeper_operation_timeout_ms` | `int` | `10000` | `-` | Timeout for ZK operation in milliseconds |
| `clickhouse_distributed_ddl_zookeeper_path` | `str` | `/clickhouse/task_queue/ddl` | `-` | Zookeeper path for DDL |
| `clickhouse_distributed_ddl_profile` | `str` | `-` | see `clickhouse_user_profiles_default` var | Profile for DDL queries |
| `clickhouse_resharding_task_queue_path` | `str` | `/clickhouse/task_queue` | `-` | Zookeeper path for task queue |
| `clickhouse_config_log_level` | `str` | `warning` | `trace, debug, information, warning, error` | clickhouse log level |
| `clickhouse_config_log_size` | `str` | `1000M` | `-` | max size for log file |
| `clickhouse_config_log_count` | `int` | `5` | `-` | max count rotated logs for store |
| `clickhouse_config_max_open_files` | `int, str` | `maximum` | `-` | CH soft limit for max opened files |
| `clickhouse_config_uncompressed_cache_size` | `int` | `8589934592` | `-` | CH uncompressed cache size |
| `clickhouse_config_mark_cache_size` | `int` | `5368709120` | `-` | CH mark cache size |
| `clickhouse_config_timezone` | `str` | `Europe/Moscow` | see timezones on wikipedia | Default timezone for CH Date/DateTime columns |
| `clickhouse_config_mlock_executable` | `bool` | `false` | `true, false` | CH mlock executable setting |
| `clickhouse_config_umask` | `str` | `"027"` | `-` | umask |
| `clickhouse_config_builtin_dictionaries_reload_interval` | `int` | `3600` | `-` | Dictionaries reload interval |
| `clickhouse_config_max_table_size_to_drop` | `int` | `50GB` | `-` | Large table delete protection |
| `clickhouse_config_max_partition_size_to_drop` | `int` | `5 GB` | `-` | The same as table size, but about the partitions |
| `clickhouse_config_max_server_memory_usage_to_ram_ratio` | `float` | `0.8` | `-` | Memory ratio soft limit |
| `clickhouse_config_max_thread_pool_size` | `int` | `15000` | `-` | Thread pool size, it is important that these are the streams of the clickhouse itself, they do not correlate with the number of cores |
| `clickhouse_config_max_concurrent_queries` | `int` | `300` | `-` | Max concurrent quieries |
| `clickhouse_config_max_connections` | `int` | `4096` | `-` | Max client connections |
| `clickhouse_config_keep_alive_timeout` | `int` | `3` | `-` | TCP keep alive timeout |
| `clickhouse_config_max_session_timeout` | `int` | `3600` | `-` | Max client session timeout |
| `clickhouse_config_default_session_timeout` | `int` | `60` | `-` | Default session timeout for clients |
| `clickhouse_config_custom_settings` | `dict` | `-` | `{ foo: bar }` | Other uncovered config settings like `<key>value</key>` |
| `clickhouse_merge_tree_settings` | `dict` | `-` | `{ foo: bar }` | MergeTree settings |
| `clickhouse_sharding_clusters` | `list(dict)` | `-` | see `defaults/main.yml` for example | Settings for sharding |
| `clickhouse_query_log_database` | `str` | `system` | `-` | Database name for query logs |
| `clickhouse_query_log_table` | `str` | `query_log` | `-` | Table name for query logs |
| `clickhouse_query_log_engine` | `str` | see `defaults/main.yml` | `-` | Engine settings for query log table |
| `clickhouse_query_log_flush_interval_milliseconds` | `int` | `7500` | `-` | Interval for flushing logs |
| `clickhouse_part_log_enabled` | `bool` | `true` | `true, false` | Enable partitions log |
| `clickhouse_part_log_database` | `str` | `system` | `-` | Database name for part logs |
| `clickhouse_part_log_table` | `str` | `part_log` | `-` | Table name for part logs |
| `clickhouse_part_log_partition_by` | `str` | `toMonday(event_date)` | `-` | PartitionBy expression for Engine |
| `clickhouse_part_log_flush_interval_milliseconds` | `int` | `7500` | `-` | Interval for flushing logs |
| `clickhouse_user_profiles_default` | `dict` | see `defaults/main.uml` | `-` | Default user profiles |
| `clickhouse_user_profles_custom` | `dict` | `-` | `-` | The same as `clickhouse_user_profiles_default`, taken out for ease of management |
| `clickhouse_user_quotas_default` | `dict` | see `defaults/main.uml` | `-` | Default user quotas |
| `clickhouse_user_quotas_custom` | `dict` | `-` | `-` | The same as `clickhouse_user_quotas_default`, taken out for ease of management |
| `clickhouse_users_default` | `list[dict]` | see `defaults/main.yml` | `-` | Default users list (by default password is insecure) |
| `clickhouse_users_custom` | `list[dict]` | `-` | `-` | The same as `clickhouse_users_default`, taken out for ease of management |
| `clickhouse_graphite_rollup` | `dict` | see example `defaults/main.yml` | `-` | Graphite rollup settings |
| `clickhouse_compression` | `list[dict]` | see example `defaults/main.yml` | `-` | Compression settings |

#### Clickhouse client variables
| Variable | Type | Default | Choices | Description |
|----------|------|---------|---------|-------------|
| `clickhouse_client_os_user` | `str` | `"{{ ansible_user or default('root') }}"` | `-` | Config owner |
| `clickhouse_client_os_group` | `str` | `"{{ ansible_user or default('root') }}"` | `-` | Config group |
| `clickhouse_client_config_user_name` | `str` | `default` | `-` | Default CH user for clickhouse-client |
| `clickhouse_client_config_user_password` | `str` | password for user `default` | `-` | Password for Default clickhouse-client user |
| `clickhouse_client_config_send_timeout` | `int` | `1800` | `-` | Client send data timeout |
| `clickhouse_client_config_receive_timeout` | `int` | `6000` | `-` | Client receive data timeout |
| `clickhouse_client_config_secure` | `bool` | `false` | `true, false` | Enable only secure connect via clickhouse-client |

#### SystemD specific variables

| Variable | Type | Default | Choices | Description |
|----------|------|---------|---------|-------------|
| `clickhouse_systemd_service_dir` | `str` | `/lib/systemd/system` | `-` | Path to actual service file |
| `clickhouse_systemd_default_service_dir` | `str` | `/etc/systemd/system/` | `-` | Path to default service file (default service will be removed) |
| `clickhouse_systemd_service_name` | `str` | `clickhouse-server.service` | `-` | Service name (include file) |
| `clickhouse_systemd_service_type` | `str` | `simple` | `simple, fork` | Service type |
| `clickhouse_systemd_capability_bounding_set` | `list` | `[CAP_NET_ADMIN, CAP_IPC_LOCK, CAP_SYS_NICE]` | `-` | Service capability |
| `clickhouse_systemd_limit_nofile` | `int, str` | `500000` | `-` | NOfile limits for service |
| `clickhouse_systemd_limit_core` | `int, str` | `infinity` | `-` | Core limits for service |
| `clickhouse_systemd_restart` | `str` | `always` | `-` | Restart policy |
| `clickhouse_systemd_restart_sec` | `int` | `30` | `-` | Restart interval for failed service |
| `clickhouse_systemd_custom_settings` | `dict` | see example `defaults/main.yml` | `-` | Uncovered custom settings for system service |

#### Docker specific variables

| Variable | Type | Default | Choices | Description |
|----------|------|---------|---------|-------------|
| `clickhouse_docker_prune_after_up` | `bool` | `true` | `true, false` | Execute `docker system prune` after composition deploy |
| `clickhouse_docker_service_name` | `str` | `clickhouse` | `-` | Docker-compose service name |
| `clickhouse_docker_restart_policy` | `str` | `unless-stopped` | `-` | Service restart policy |
| `clickhouse_docker_container_name` | `str` | `clickhouse` | `-` | Clickhouse container bane |
| `clickhouse_docker_hostname` | `str` | `clickhouse` | `-` | Container hostname |
| `clickhouse_docker_cpus` | `int` | `-` | `-` | CPU's quota for container |
| `clickhouse_docker_mem_limit` | `str` | `-` | `-` | Memory quota for container |
| `clickhouse_docker_cap_add` | `list` | `[SYS_ADMIN, SYS_NICE, NET_ADMIN]` | `-` | Container capability set |
| `clickhouse_docker_published_ports` | `list(dict)` | see `defaults/main.yml` | `[{ 'host': 8123, 'container': 8080 }, { ... }]` | Published ports |


Example Playbook
----------------

* Basic example

```yaml
- hosts: clickhouse01.example.com
  roles:
    - role: clickhouse
      vars:
        clickhouse_service_manager: systemd
        clickhouse_listen_port_http: 8123
        clickhouse_listen_port_tcp: 9000
        clickhouse_enable_secure_protocols: true
        clickhouse_ssl_certificate: "{{ lookup('file', '/tmp/server.crt') }}"
        clickhouse_ssl_private_key: "{{ lookup('file', '/tmp/server.key') }}"
        clickhouse_users_custom:
          - username: test
            password: test
            profile: default
            quota: default
            allow_databases:
              - test
            networks:
              ip:
                - ::/0
```


* Example of installing two Clickhouse instances on the same server:

```yaml
- hosts: clickhouse01.example.com
  roles:
    - role: clickhouse
      vars:
        clickhouse_service_manager: docker
        clickhouse_dir_data: "{{ clickhouse_base_dir_data }}/clickhouse_docker"
        clickhouse_dir_log: "{{ clickhouse_base_dir_log }}/clickhouse_docker"
        clickhouse_dir_config: "{{ clickhouse_base_dir_config }}/clickhouse_docker"
        clickhouse_docker_published_ports:
          - host: "{{ clickhouse_listen_port_tcp }}"
            container: 8125
          - host: "{{ clickhouse_listen_port_http }}"
            container: 9005

    - role: clickhouse
      vars:
        clickhouse_service_manager: systemd
        clickhouse_listen_port_http: 7798
        clickhouse_listen_port_tcp: 9100
```

Author Information
------------------

akimstrong@yandex.ru
