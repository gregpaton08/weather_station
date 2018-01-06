# Weather Station

## Notes

[https://murmuring-caverns-91180.herokuapp.com/](https://murmuring-caverns-91180.herokuapp.com/)

### Run locally
```
venv/bin/gunicorn weatherstation:app
```

## Create Heroku remote
```
heroku git:remote -a murmuring-caverns-91180
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
