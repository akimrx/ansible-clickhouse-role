#!/bin/bash

watch -n1 -t 'clickhouse-client --format PrettyNoEscapes --query " \
SELECT \
    elapsed, \
    formatReadableSize(memory_usage) AS mem, \
    http_user_agent AS user_agent, \
    initial_user, \
    address, \
    formatReadableSize(read_bytes) as rbytes, \
    substring(query, 1, 60) AS query_preview \
FROM system.processes"'
