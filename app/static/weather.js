var displayTemperatureInFahrenheit = true;
var insideTemperatureC = 0;
var outsideTemperatureC = 0;
var forecastData = [];
var historyData = [];
var currentHour = 0;

function convertCelsiusToFahrenheit(celsius) {
    var fahrenheit = ((celsius * 9.0) / 5.0) + 32.0;
    // Round to one decimal place.
    return Math.round(fahrenheit * 10) / 10;
}

function convertTemperature(temperature) {
    if (displayTemperatureInFahrenheit) {
        return convertCelsiusToFahrenheit(temperature);
    } else {
        return temperature;
    }
}

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

function updateTemperature() {
    $('#insidetemp').text(Math.round(convertTemperature(insideTemperatureC)));
    $('#outsidetemp').text(Math.round(convertTemperature(outsideTemperatureC)));
}

function drawChart() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Time');
    data.addColumn('number', 'Indoor');
    data.addColumn('number', 'Outdoor');

    // Populate historical indoor temperature data for the chart.
    for (var i = 0; i < 12; i++) {
        var hour = currentHour;

        // Search the data for the current hour
        currentTemperature = historyData.find(function(element) {
            return element['hour'] == hour;
        })

        temperature = -10;
        if (currentTemperature) {
            temperature = currentTemperature['temperature'];
        } else {
            console.log('No indoor temperature for hour ' + hour)
        }

        data.addRow([
            formatTime(hour),
            convertTemperature(temperature),
            null
        ]);
    }

    // Populate outdoor temperature forecast data for the chart. Note the two plots overlap so the for i == 0 the current indoor temperature is plotted.
    var arrayLength = Math.min(forecastData.length, 12);
    for (var i = 0; i < arrayLength; i++) {
        current = forecastData[i]
        data.addRow([
            formatTime(parseInt(current['hour'])),
            i == 0 ? convertTemperature(historyData[historyData.length - 1]['temperature']) : null,
            convertTemperature(parseInt(current['temperature']))
        ]);
    }

    var options = {
        // title: 'Company Performance',
        curveType: 'function',
        legend: { position: 'bottom' },
        chartArea: { left: 20, top: 10, width: '100%', height: '80%' },
        vAxis: { gridlines: { color: '#DDD', count: 3 }},
        // vAxis: { minorGridlines: { count: 1 }},
        hAxis: { showTextEvery: 3 }
    };

    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

    chart.draw(data, options);
}

function updateData() {
    $SCRIPT_ROOT = ''

    $.getJSON($SCRIPT_ROOT + '/get_temperature_data_c', {}, function(data) {
        insideTemperatureC = data.inside_temperature;
        outsideTemperatureC = data.outside_temperature;

        updateTemperature();
    });

    $.getJSON($SCRIPT_ROOT + '/get_hourly_weather', {}, function(data) {
        currentHour = data.current_time.hour;
        $.each(data.weather, function(index, value) {
            weatherData = {}
            weatherData['hour'] = value.hour;
            weatherData['temperature'] = value.temp;
            forecastData.push(weatherData);
        });


        $.getJSON($SCRIPT_ROOT + 'get_hourly_indoor_history', {}, function(indoorData) {
            $.each(indoorData.history, function(index, value) {
                indoorData = {}
                indoorData['hour'] = value.hour;
                indoorData['temperature'] = value.temperature;
                historyData.push(indoorData);
            });

            google.charts.load('current', {'packages':['corechart']});
            google.charts.setOnLoadCallback(drawChart);
        });

    });
}

updateData();

$(function() {
    setInterval(updateData, 30000);
});

$(function() {    
    $("#temp_type").click(function(e) {
        e.preventDefault();
        displayTemperatureInFahrenheit = !displayTemperatureInFahrenheit;
        if (displayTemperatureInFahrenheit) {
            $("#temp_type").html('<a href="#">c&deg;</a>|f&deg;');
        } else {
            $("#temp_type").html('c&deg;|<a href="#">f&deg;</a>');
        }
        updateTemperature();
        updateForecast();
        drawChart();
    });
});