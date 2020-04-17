# dataglen
Project contains an end point with method `POST` to store incoming sensor data and method `GET` to retrieve data based on query
parameters.

As instructed in assignment PDF, UI contains table to display stored data from database, line chart for visiual representation and
Max, Min and Mean value of reading based on given time range.

Development of API has been done in Django and standard MVT (Model, View, Template) structure has been followed. HTML file is in
`/work/templates/dashboard.html` and javascript file is in static folder `/work/static/dashboard.js` path.

For UI, I have pushed some dummy data based on one example that was given in assignment PDF.

# Tech Stack
Dango
VueJs, Jquery, Gstatic Chart


For authentication in `POST` method, hard code token (defined in `settings.py`) has been used. Afer authentication, `Jsonschema` has
been used to validate data received from device (in this case `POSTMAN`) and if data isn't valid, I have dumped it in a text file
so that data doesn't get lost.

A management command has also been added to populate dummy data. Command can be found in `work/management/commands/dummay_data.py`.


For storing data, I have used postgres database and django model has been defined in `work/models.py` file. 

For the frontend, as instructed in assingment PDF, there is one dropdown to select sensor type and there is an option to select
`Start Date` and `End Date` if we wish to apply date range filter.Data gets updated in table and chart become visible based
on filter applied in sensor type.

Chart won't be visible in case of `All` is selected in sensor type dropdown.

Screenshots of UI -

![image](https://user-images.githubusercontent.com/10773085/79552089-30d7ac80-80b8-11ea-99cb-f24261598588.png)

![image](https://user-images.githubusercontent.com/10773085/79552773-1d791100-80b9-11ea-94d5-d341476a7922.png)


