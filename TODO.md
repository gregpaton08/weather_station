# To Do

## Open
### Front-end
* add support for celsius and fahrenheit
    * Graph plot shouldn't move when switching between C and F
* chart
    * update chart style to match rest of design (chart.js? or D3?)
    * Make graph interactive (zoom, scroll) like Google finance
* Design outdoor weather icons (sun, clouds, rain, wind, etc.)
* Display weather icons
* Display weather warnings/forecast
    * need to decide how to display this
* Mobile site?
    * Temperature display vertical (top/bottom) instead of horizontal (side-by-side)
* Add option to set location
* Split app into client/server in separate repos? microservice to integrate with all home automation?
* Consider updating site colors

<img src="notes/invert.png" width="600">

### Back-end
* Store historical indoor/outdoor data in persistant database (Heroku?)
* Unix time instead of full date in API JSON data?
* debug performance bottleneck. Data is cached, requests shouldn't take so long.
* Update/improve security for temperature POST
* API throttling to prevent malicious attacks (?). Anything built in to Flask?
* Design single API call to get historic indoor and forecast outdoor temperature
* Unit tests!!!!!

### Stretch Goals
* build and integrate with "smart" thermostat
    * integrate Google calendar to turn down heat when away

## Complete
* Display weather conditions as text
* Store historical indoor temperature in database
* Set up cron job on RPi to update indoor temperature every 5 minutes
* Set URL as weather.gregpaton08.com
* Design house icon
* Fix temperature graph displaying negative times