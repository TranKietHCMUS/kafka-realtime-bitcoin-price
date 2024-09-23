## Source
curl -X POST  -H  "Content-Type:application/json" http://localhost:8083/connectors -d @connectors/source/mysql.json

curl -X POST  -H  "Content-Type:application/json" http://localhost:8083/connectors -d @connectors/source/postgres.json

## Sink
curl -X POST  -H  "Content-Type:application/json" http://localhost:8083/connectors -d @connectors/sink/binance.json

curl -X POST  -H  "Content-Type:application/json" http://localhost:8083/connectors -d @connectors/sink/coin-market.json