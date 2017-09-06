curl -u gpaton:$(cat api_password.txt) -i -H "Content-Type: application/json" -X POST -d '{"temperature":"17.3"}'  http://localhost:8000/update_temperature

# curl -u gpaton:$(cat api_password.txt) -i -H "Content-Type: application/json" -X POST -d '{"temperature":'"19"'}' https://murmuring-caverns-91180.herokuapp.com/update_temperature
