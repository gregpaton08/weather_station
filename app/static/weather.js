var displayTemperatureInFahrenheit = true;
var insideTemperatureC = 0;
var outsideTemperatureC = 0;
var forecastData = [];
var historyData = [];

function convertCelsiusToFahrenheit(celsius) {
    return Math.round(((celsius * 9.0) / 5.0) + 32.0);
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
    $('#insidetemp').text(convertTemperature(insideTemperatureC));
    $('#outsidetemp').text(convertTemperature(outsideTemperatureC));
}

function updateForecast() {
    $html = '';
    $.each(forecastData, function(index, value) {
        $html += '<td><div class="time">' + formatTime(value.hour) + '</div><div class="temperature">' + String(convertTemperature(value.temperature)) + '&deg;</div></td>';

        return index < 12;
    });
    $('#hourly_forecast tr').html($html).show();
}

function drawChart() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Time');
    data.addColumn('number', 'Indoor');
    data.addColumn('number', 'Outdoor');

    // Populate historical indoor temperature data for the chart.
    for (var i = 0; i < 12; i++) {
        // Compute the current hour
        var hour = forecastData[0]['hour'] - 12 + i;

        // Search the data for the current hour
        currentTemperature = historyData.find(function(element) {
            return element['hour'] == hour;
        })

        temperature = -10;
        if (currentTemperature) {
            temperature = currentTemperature['temperature'];
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
            i == 0 ? convertTemperature(29) : null,
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

    $.getJSON($SCRIPT_ROOT + '/get_hourly_forecast', {}, function(data) {
        $.each(data.forecast, function(index, value) {
            data = {}
            data['hour'] = value.FCTTIME.hour;
            data['temperature'] = value.temp.metric;
            data['condition'] = value.condition;
            forecastData.push(data);
        });

        updateForecast();

        $.getJSON($SCRIPT_ROOT + 'get_hourly_indoor_history', {}, function(indoorData) {
            $.each(indoorData.history, function(index, value) {
                data = {}
                data['hour'] = value.hour;
                data['temperature'] = value.temperature;
                historyData.push(data);
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