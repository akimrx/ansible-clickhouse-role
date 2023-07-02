"""Default basic tests."""

import pytest
import requests


@pytest.fixture
def role_vars(host):
    """Loading standard role variables."""
    defaults_files = "file=./defaults/main.yml name=role_defaults"
    vars_files = "file=./vars/main.yml name=role_vars"

    ansible_vars = host.ansible("include_vars", defaults_files)["ansible_facts"]["role_defaults"]
    ansible_vars.update(host.ansible("include_vars", vars_files)["ansible_facts"]["role_vars"])
    return ansible_vars


@pytest.mark.parametrize(
    "directory",
    [
        "/opt",
        "/opt/conf",
        "/opt/data",
        "/opt/log",
        "/opt/conf/clickhouse",
        "/opt/conf/clickhouse/ssl",
        "/opt/data/clickhouse",
        "/opt/log/clickhouse",
        "/opt/tmp/clickhouse",
        "/opt/lib/clickhouse",
        "/opt/lib/clickhouse/user_files",
    ],
)
def test_directories(host, directory):
    d = host.file(directory)
    assert d.exists
    assert d.is_directory


@pytest.mark.parametrize(
    "directory",
    [
        "/opt",
        "/opt/conf",
        "/opt/data",
        "/opt/log",
        "/opt/tmp",
        "/opt/lib",
    ],
)
def test_global_dirs_permissions_didnt_change(host, directory, role_vars):
    d = host.file(directory)
    general_owner = role_vars["clickhouse_general_owner"]
    assert d.user == general_owner
    assert d.group == general_owner


@pytest.mark.parametrize(
    "directory",
    [
        "/opt/conf/clickhouse",
        "/opt/conf/clickhouse/ssl",
        "/opt/data/clickhouse",
        "/opt/log/clickhouse",
        "/opt/tmp/clickhouse",
        "/opt/lib/clickhouse",
        "/opt/lib/clickhouse/user_files",
    ],
)
def test_specific_dirs_permissions_didnt_change(host, directory, role_vars):
    d = host.file(directory)
    system_user = role_vars["clickhouse_system_user"]
    system_group = role_vars["clickhouse_system_group"]
    assert d.user == system_user
    assert d.group == system_group


def test_clickhouse_top_is_exists(host):
    f = host.file("/usr/bin/clickhouse-top")
    assert f.exists
    assert f.is_file
    assert f.mode == 0o755


def test_listen_port(host, role_vars):
    ports = role_vars["clickhouse_listen_port_http"], role_vars["clickhouse_listen_port_tcp"]
    for port in ports:
        s = host.socket(f"tcp://127.0.0.1:{port}")
        assert s.is_listening


def test_clickhouse_http_is_works(host, role_vars):
    ip = host.ansible.get_variables().get("ansible_host")
    port = role_vars["clickhouse_listen_port_http"]
    url = f"http://{ip}:{port}/ping"

    query_result = requests.get(url).text.strip()
    assert query_result == "Ok."


def test_clickhouse_https_is_works(host, role_vars):
    https_port = role_vars["clickhouse_listen_port_https"]
    command = f"curl -sS 'https://localhost:{https_port}/ping' --cacert /opt/conf/clickhouse/ssl/server.crt"
    cmd = host.run(command)
    assert cmd.stderr.strip() == ""
    assert cmd.stdout.strip() == "Ok."


def test_clickhouse_native_is_works(host, role_vars):
    port = role_vars["clickhouse_listen_port_tcp"]
    command = f"clickhouse-client --port {port} -nq 'SELECT 1'"
    cmd = host.run(command)
    assert cmd.stderr.strip() == ""
    assert cmd.stdout.strip() == "1"


def test_clickhouse_secure_native_is_works(host, role_vars):
    port = role_vars["clickhouse_listen_port_tcp_secure"]
    command = f"clickhouse-client --secure --port {port} -nq 'SELECT 1'"
    cmd = host.run(command)
    assert cmd.stderr.strip() == ""
    assert cmd.stdout.strip() == "1"


def test_can_create_table(host, role_vars):
    ip = host.ansible.get_variables().get("ansible_host")
    port = role_vars["clickhouse_listen_port_http"]
    user = list(filter(lambda _dict: _dict.get("username") == "default", role_vars["clickhouse_users_default"]))[0]
    username, password = user.get("username"), user.get("password")
    query = "CREATE TABLE IF NOT EXISTS `default`.`test` (text String DEFAULT '') ENGINE Log"

    url = f"http://{ip}:{port}?user={username}&password={password}&query={query}"
    query_result = requests.post(url).status_code
    assert query_result in (201, 200)


def test_writer_can_write(host, role_vars):
    ip = host.ansible.get_variables().get("ansible_host")
    port = role_vars["clickhouse_listen_port_http"]
    user = list(filter(lambda _dict: _dict.get("username") == "default", role_vars["clickhouse_users_default"]))[0]
    username, password = user.get("username"), user.get("password")
    query = "INSERT INTO `default`.`test` VALUES ('test')"

    url = f"http://{ip}:{port}?user={username}&password={password}&query={query}"
    query_result = requests.post(url).status_code
    assert query_result in (201, 200)


def test_reader_can_read(host, role_vars):
    ip = host.ansible.get_variables().get("ansible_host")
    port = role_vars["clickhouse_listen_port_http"]
    user = list(filter(lambda _dict: _dict.get("username") == "readonly", role_vars["clickhouse_users_default"]))[0]
    username, password = user.get("username"), user.get("password")
    query = "SELECT text FROM `default`.`test` LIMIT 1"

    url = f"http://{ip}:{port}?user={username}&password={password}&query={query}"
    query_result = requests.post(url).text.strip()
    assert query_result == "test"


def test_reader_cant_write(host, role_vars):
    ip = host.ansible.get_variables().get("ansible_host")
    port = role_vars["clickhouse_listen_port_http"]
    user = list(filter(lambda _dict: _dict.get("username") == "readonly", role_vars["clickhouse_users_default"]))[0]
    username, password = user.get("username"), user.get("password")
    query = "INSERT INTO `default`.`test` VALUES ('test')"

    url = f"http://{ip}:{port}?user={username}&password={password}&query={query}"
    query_result = requests.post(url).status_code
    assert query_result in range(500, 504)


@pytest.mark.parametrize(
    "query",
    [
        "CREATE USER molecule_access IDENTIFIED WITH plaintext_password BY 'molecule' SETTINGS PROFILE 'readonly'",
        "GRANT SHOW TABLES, SELECT ON *.* TO molecule_access",
    ],
)
def test_default_can_access_management(host, role_vars, query):
    ip = host.ansible.get_variables().get("ansible_host")
    port = role_vars["clickhouse_listen_port_http"]
    user = list(filter(lambda _dict: _dict.get("username") == "default", role_vars["clickhouse_users_default"]))[0]
    username, password = user.get("username"), user.get("password")

    url = f"http://{ip}:{port}?user={username}&password={password}&query={query}"
    query_result = requests.post(url).status_code
    assert query_result in (201, 200)
