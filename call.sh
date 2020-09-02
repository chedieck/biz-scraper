#!/bin/bash

key_call="X-CMC_PRO_API_KEY: "$(cat api.key)

curl -H "$key_call" -H "Accept: application/json" -d "start=1&limit=5000&convert=USD" -G https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest > temp.json




