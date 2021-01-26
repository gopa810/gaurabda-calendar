# Example of results from find-location


## Request (method GET)

```
http://server.address:port/find-location?name=Bra
```

## Response (body)

```json
{
    "CONTAINS": [
        {
            "city": "Rio Branco",
            "country": "Brazil",
            "latitude": -9.974722,
            "longitude": -67.809998,
            "name": "Rio Branco (Brazil)",
            "offset": -5,
            "tzid": 74,
            "tzname": "-5:00 America/Rio_Branco"
        },
        {
            "city": "Vila da Ribeira Brava",
            "country": "Cape Verde",
            "latitude": 16.616667,
            "longitude": -24.299999,
            "name": "Vila da Ribeira Brava (Cape Verde)",
            "offset": -1,
            "tzid": 126,
            "tzname": "-1:00 Atlantic/Cape_Verde"
        },
        {
            "city": "Al Mahallah al Kubra",
            "country": "Egypt",
            "latitude": 30.97611,
            "longitude": 31.166945,
            "name": "Al Mahallah al Kubra (Egypt)",
            "offset": 2,
            "tzid": 139,
            "tzname": "+2:00 Africa/Cairo"
        },
        {
            "city": "Gibraltar",
            "country": "Gibraltar",
            "latitude": 36.133335,
            "longitude": -5.35,
            "name": "Gibraltar (Gibraltar)",
            "offset": 1,
            "tzid": 161,
            "tzname": "+1:00 Europe/Gibraltar"
        }
    ],
    "EQUALS": [],
    "STARTS": [
        {
            "city": "Brasilia",
            "country": "Brazil",
            "latitude": -15.77972,
            "longitude": -47.929722,
            "name": "Brasilia (Brazil)",
            "offset": -3,
            "tzid": 67,
            "tzname": "-3:00 America/Sao_Paulo"
        },
        {
            "city": "Brazzaville",
            "country": "Congo",
            "latitude": -4.259167,
            "longitude": 15.284722,
            "name": "Brazzaville (Congo)",
            "offset": 1,
            "tzid": 111,
            "tzname": "+1:00 Africa/Brazzaville"
        },
        {
            "city": "Braunschweig",
            "country": "Germany",
            "latitude": 52.266666,
            "longitude": 10.533333,
            "name": "Braunschweig (Germany)",
            "offset": 1,
            "tzid": 130,
            "tzname": "+1:00 Europe/Berlin"
        },
        {
            "city": "Bradford",
            "country": "United Kingdom",
            "latitude": 53.783333,
            "longitude": -1.75,
            "name": "Bradford (United Kingdom)",
            "offset": 0,
            "tzid": 155,
            "tzname": "+0:00 Europe/London"
        },
        {
            "city": "Brahmapur",
            "country": "India",
            "latitude": 19.316668,
            "longitude": 84.783333,
            "name": "Brahmapur (India)",
            "offset": 5.5,
            "tzid": 188,
            "tzname": "+5:30 Asia/Calcutta"
        },
        {
            "city": "Brasov",
            "country": "Romania",
            "latitude": 45.633335,
            "longitude": 25.583334,
            "name": "Brasov (Romania)",
            "offset": 2,
            "tzid": 294,
            "tzname": "+2:00 Europe/Bucharest"
        },
        {
            "city": "Braila",
            "country": "Romania",
            "latitude": 45.266666,
            "longitude": 27.983334,
            "name": "Braila (Romania)",
            "offset": 2,
            "tzid": 294,
            "tzname": "+2:00 Europe/Bucharest"
        },
        {
            "city": "Bratsk",
            "country": "Russia",
            "latitude": 56.1325,
            "longitude": 101.614166,
            "name": "Bratsk (Russia)",
            "offset": 8,
            "tzid": 304,
            "tzname": "+8:00 Asia/Irkutsk"
        },
        {
            "city": "Bratislava",
            "country": "Slovakia",
            "latitude": 48.150002,
            "longitude": 17.116667,
            "name": "Bratislava (Slovakia)",
            "offset": 1,
            "tzid": 321,
            "tzname": "+1:00 Europe/Bratislava"
        },
        {
            "city": "Brakpan",
            "country": "South Africa",
            "latitude": -26.233334,
            "longitude": 28.366667,
            "name": "Brakpan (South Africa)",
            "offset": 2,
            "tzid": 396,
            "tzname": "+2:00 Africa/Johannesburg"
        }
    ]
}
```