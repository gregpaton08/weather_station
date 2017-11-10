
var weatherGlobals = {
    outdoorData: [],
    indoorData: [],
    displayTemperatureInFahrenheit: true
};


/**
 * Conver celsisu to fahrenheit.
 */
function convertCelsiusToFahrenheit(celsius) {
    var fahrenheit = ((celsius * 9.0) / 5.0) + 32.0;
    // Round to one decimal place.
    return Math.round(fahrenheit * 10) / 10;
}

/**
 * Convert the temperature to the desired units.
 */
function convertTemperature(temperature) {
    if (temperature == null) {
        return null;
    }

    if (weatherGlobals.displayTemperatureInFahrenheit) {
        return convertCelsiusToFahrenheit(temperature);
    } else {
        return temperature;
    }
}

/**
 * Convert 24 hour to am/pm.
 */
function formatTime(hour) {
    if (hour == 0) {
        return '12 am';
    } else if (hour > 12) {
        return String(hour - 12) + ' pm';
    } else if (hour == 12) {
        return '12 pm';
    } else {
        return String(hour) + ' am';
    }
}

/**
 * Update the current indoor and outdoor temperature.
 */
function updateTemperature() {
    $('#insidetemp').text(Math.round(convertTemperature(weatherGlobals.insideTemperatureC)));
    $('#outsidetemp').text(Math.round(convertTemperature(weatherGlobals.outsideTemperatureC)));
}


/**
 * Draw the temperature chart.
 */
function drawChart() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Time');
    data.addColumn('number', 'Indoor');
    data.addColumn('number', 'Outdoor');

    // Populate historical indoor temperature data for the chart.
    var previousHours = 12;
    var currentDate = new Date(parseInt(weatherGlobals.currentTime.year), weatherGlobals.currentTime.month - 1, weatherGlobals.weatherGlobals.currentTime.day, weatherGlobals.currentTime.hour - previousHours);
    var arrayLength = Math.min(weatherGlobals.outdoorData.length, 12);
    for (var i = -previousHours; i < arrayLength; i++) {

        // Search the data for the current hour
        currentTemperature = weatherGlobals.indoorData.find(function(element) {
            return parseInt(element['year']) == currentDate.getFullYear() &&
                   parseInt(element['month']) == currentDate.getMonth() + 1 &&
                   parseInt(element['day']) == currentDate.getDate() &&
                   parseInt(element['hour']) == currentDate.getHours();
        })

        var temperature = null;
        if (currentTemperature) {
            temperature = currentTemperature['temperature'];
        } else {
            console.log('No indoor temperature for hour ' + currentDate);
        }

        outdoorTemperature = weatherGlobals.outdoorData.find(function(element) {
            return parseInt(element['year']) == currentDate.getFullYear() &&
                   parseInt(element['month']) == currentDate.getMonth() + 1 &&
                   parseInt(element['day']) == currentDate.getDate() &&
                   parseInt(element['hour']) == currentDate.getHours();
        })

        if (outdoorTemperature) {
            outdoorTemperature = outdoorTemperature['temperature'];
        } else {
            console.log('No outdoor temperature for ' + currentDate);
        }

        data.addRow([
            formatTime(currentDate.getHours()),
            convertTemperature(temperature),
            convertTemperature(outdoorTemperature)
        ]);

        currentDate.setHours(currentDate.getHours() + 1);
    }

    var options = {
        curveType: 'function',
        legend: { position: 'bottom' },
        chartArea: { left: 20, top: 10, width: '100%', height: '80%' },
        vAxis: { gridlines: { color: '#DDD', count: 3 }},
        vAxis: { minorGridlines: { count: 0 }},
        hAxis: { showTextEvery: 3 }
    };

    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

    chart.draw(data, options);
}

/**
 * Update weather data by calling APIs.
 */
function updateData() {
    $SCRIPT_ROOT = ''

    $.getJSON($SCRIPT_ROOT + '/get_temperature_data_c', {}, function(data) {
        weatherGlobals.insideTemperatureC = data.inside_temperature;
        weatherGlobals.outsideTemperatureC = data.outside_temperature;

        updateTemperature();
    });

    $.when(
        $.getJSON($SCRIPT_ROOT + '/get_hourly_weather', {}, function(data) {

            weatherGlobals.currentTime = data.current_time;

            $.each(data.weather, function(index, value) {
                weatherData = {}
                weatherData['year'] = value.year
                weatherData['month'] = value.month
                weatherData['day'] = value.day
                weatherData['hour'] = value.hour;
                weatherData['temperature'] = value.temp;
                weatherGlobals.outdoorData.push(weatherData);
            });
        }),

        $.getJSON($SCRIPT_ROOT + 'get_hourly_indoor_history', {}, function(indoorData) {
            $.each(indoorData.history, function(index, value) {
                indoorData = {}
                indoorData['year'] = value.year
                indoorData['month'] = value.month
                indoorData['day'] = value.day
                indoorData['hour'] = value.hour;
                indoorData['temperature'] = value.temperature;
                weatherGlobals.indoorData.push(indoorData);
            });
        })
    ).then(function() {
        google.charts.load('current', {'packages':['corechart']});
        google.charts.setOnLoadCallback(drawChart);
    });
}

updateData();

/** Anonymous function to call the updateData function every 30 seconds. */
$(function() {
    setInterval(updateData, 30000);
});

/** Function tied to button to toggle between celsisu and fahrenheit. */
$(function() {    
    $("#temp_type").click(function(e) {
        e.preventDefault();
        weatherGlobals.displayTemperatureInFahrenheit = !weatherGlobals.displayTemperatureInFahrenheit;
        if (weatherGlobals.displayTemperatureInFahrenheit) {
            $("#temp_type").html('<a href="#">c&deg;</a>|f&deg;');
        } else {
            $("#temp_type").html('c&deg;|<a href="#">f&deg;</a>');
        }
        updateTemperature();
        updateForecast();
        drawChart();
    });
});