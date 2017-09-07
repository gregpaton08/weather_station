# Weather Station

## To Do

### Open
* Fix temperature graph displaying negative times
* Design single API call to get historic indoor and forecast outdoor temperature
* Display weather icons
* Display weather warnings
* Design house icon
* Design outdoor weather icons (sun, clouds, rain, wind, etc.)
* Make graph interactive (zoom, scroll) like Google finance
* Mobile site?
* Sotre historical outdoor data in database
* Graph plot shouldn't move when switching between C and F
* Consider updating site colors
* Add option to set location
* Split app into client/server in separate repos?

<img src="invert.png" width="600">

### Complete
* Store historical indoor temperature in database
* Set up cron job on RPi to update indoor temperature every 5 minutes

## Notes

[https://murmuring-caverns-91180.herokuapp.com/](https://murmuring-caverns-91180.herokuapp.com/)

### Run locally
```
flask/bin/gunicorn run:app
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
