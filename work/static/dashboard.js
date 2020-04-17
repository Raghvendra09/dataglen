 var storeFlags = new Vue({
      el: '#sensor-flags',
      data: {
        sensorTypes: "",
        selected: "ALL",
        start_date: "",
        end_date: "",
        aggregatedData: null,

      },
      methods: {
        changeFilter: function(){
        let self = this;
        console.log(this.selected);
          this.populateTable();
           this.drawChart();

        },
         drawChart: function (){
     let self = this;
     inputData = this.getInputParameter();
     inputData['chart'] = 'chartData';
      $.ajax({
        type:'GET',
        data: inputData,
        url:'/',
        success:function(outputData)
        {
        var data = google.visualization.arrayToDataTable(outputData.data);
        self.aggregatedData = outputData.aggregatedData;
        var options = {
          title: 'Sensor Data',
          curveType: 'function',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

        chart.draw(data, options);
        },
        error: function(data) {

        }
      });


      },
       getInputParameter: function() {
       let self = this;
        var inputData = {};
      if (this.start_date != "" && this.end_date != "") {
        inputData = {"sensorType": this.selected,
         "startDate": this.start_date,
          "endDate": this.end_date}
        }
       else if (this.start_date != ""){
       inputData = {
       "sensorType": this.selected,
        "startDate": this.start_date
        }
       }
       else if (this.end_date != ""){
       inputData = {
       "sensorType": this.selected,
       "endDate": this.end_date
       }
       }
       else {
       inputData = {"sensorType": this.selected}

       }
       return inputData;

       },
      populateTable: function(){
      let self = this;
        inputData = this.getInputParameter();
        inputData['table'] = 'tabledata';
        console.log(inputData);
       $('#sensor-data-table').DataTable().destroy();
        $("#sensor-data-table").DataTable({
        scrollY:        '50vh',
        scrollCollapse: true,
           ajax: {
                  url: '/',
                  method: "GET",
                  xhrFields: {
                      withCredentials: true
                  },
                   data: inputData,

                  },
              "columns": [
                  { "data": '0' },
                  { "data": '1' },
                  { "data": '2'},
                  { "data": '3'},
              ],
              "initComplete": function( settings, json ) {
                       var table = $('#sensor-data-table').DataTable();
                       }
                       });


      },
      getSensorTypes: function(){
      let self = this;
       $.ajax({
        type:'GET',
        data: {'allSensorTypes': 'getAllSensorTypes'},
        url:'/',
        success:function(data)
        {
        self.sensorTypes = data.data;
        },
        error: function(data) {

        }
      });

      }
      },
      mounted: function(){
            this.getSensorTypes();
            this.populateTable();
            google.charts.load('current', {'packages':['corechart']});




      },


   });
