$(document).ready(function(){
  $.ajax({
    url : "http://localhost/chartjs/vehicledata.php?vehicle=1",
    type : "GET",
    success : function(data){
      console.log(data)
	  var vehicle = [];
	  var t_diff [];
	  var voltage [];
	  var temperature []

      for(var i in data) {
		vehicle.push(data[i].v_id);
        t_diff.push("t_diff " + data[i].t_diff);
        voltage.push(data[i].volts);
        temperature.push(data[i].temp);
      }

      var chartdata = {
        labels: t_diff,
        datasets: [
          {
            label: "voltage",
            fill: false,
            lineTension: 0.1,
            backgroundColor: "rgba(59, 89, 152, 0.75)",
            borderColor: "rgba(59, 89, 152, 1)",
            pointHoverBackgroundColor: "rgba(59, 89, 152, 1)",
            pointHoverBorderColor: "rgba(59, 89, 152, 1)",
            data: voltage
          },
          {
            label: "temperature",
            fill: false,
            lineTension: 0.1,
            backgroundColor: "rgba(29, 202, 255, 0.75)",
            borderColor: "rgba(29, 202, 255, 1)",
            pointHoverBackgroundColor: "rgba(29, 202, 255, 1)",
            pointHoverBorderColor: "rgba(29, 202, 255, 1)",
            data: temperature
          }
        ]
      };

      var ctx = $("#mycanvas");

      var LineGraph = new Chart(ctx, {
        type: 'line',
        data: chartdata
      });
    },
    error : function(data) {

    }
  });
});