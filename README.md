# Weather Station

## To Do

### Open
* Unix time instead of full date in API JSON data?
* API throttling to prevent malicious attacks (?). Anything built in to Flask?
* Design single API call to get historic indoor and forecast outdoor temperature
* Display weather icons
* Display weather warnings
* Design outdoor weather icons (sun, clouds, rain, wind, etc.)
* Make graph interactive (zoom, scroll) like Google finance
* Mobile site?
* Store historical outdoor data in database
* Graph plot shouldn't move when switching between C and F
* Add option to set location
* Split app into client/server in separate repos?
* Unit tests!!!!!
* Consider updating site colors

<img src="invert.png" width="600">

### Complete
* Store historical indoor temperature in database
* Set up cron job on RPi to update indoor temperature every 5 minutes
* Set URL as weather.gregpaton08.com
* Design house icon
* Fix temperature graph displaying negative times

## Notes

[https://murmuring-caverns-91180.herokuapp.com/](https://murmuring-caverns-91180.herokuapp.com/)

### Run locally
```
flask/bin/gunicorn run:app
```

### Deploy to Heroku
```
git push heroku master
```

### Set config var (for API keys)

```
# set the config var
heroku config:set GITHUB_USERNAME=joesmith

# view the config
heroku config

# unset a config var
heroku config:unset GITHUB_USERNAME
```
```
heroku config:set REST_API_PASSWORD=$(cat api_password.txt)
heroku config:set PRODUCTION=.
```

### Run post script every 5 minutes with cron
```
# change to correct directory
./post_temperature.sh
```

### Debug

#### Access bash of Heroku working directory
```
heroku run bash
```
