temperature=$(./thermometer.py)
curl -u gpaton:$(cat api_password.txt) -i -H "Content-Type: application/json" -X POST -d '{"temperature":'"${temperature}"'}' https://murmuring-caverns-91180.herokuapp.com/update_temperature

# echo 'updated temperature '${temperature} >> log.txt