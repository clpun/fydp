require(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function($) {
	      $("td").click(function() {
	      		// toggleClass($(this));
	      		
	            // window.alert("clicked: "+$(this).attr('id'));
				$(this).toggleClass("selected-cell");
				if ($(this).attr('class')=="selected-cell") {
					generateTable($(this));
				} else {
					removeTable($(this));
				}
	      });
	});

    function generateTable(classSelected) {
    	var table = '<div class="row" id="'+classSelected.attr('id')+'-table">';
	        table += '<div class="col-md-4">';
	        table += '<h3>'+classSelected.attr('id')+'</h3>';
	          table += '<table class="table table-bordered" >';
	            table += '<thead>';
	              table += '<tr>';
	                table += '<th>Frequency</th>';
	                table += '<th>Power</th>';
	                table += '<th>Power Graph</th>';
	              table += '</tr>';
	            table += '</thead>';
	            table += '<tbody>';
	              table += '<tr>';
	                table += '<td>Delta</td>';
	                table += '<td>251.03</td>';
	                table += '<td><div class="row">';
			        table +=  '<canvas id="myChart" width="20" height="20"></canvas>';
			        table += '</div></td>';
	              table += '</tr>';
	              table += '<tr>';
	                table += '<td>Theta</td>';
	                table += '<td>72.4</td>';
	                table += '<td><div class="row">';
			        table +=  '<canvas id="myChart" width="20" height="20"></canvas>';
			        table += '</div></td>';
	              table += '</tr>';
	              table += '<tr>';
	                table += '<td>Alpha</td>';
	                table += '<td>90.68</td>';
	                table += '<td><div class="row">';
			        table +=  '<canvas id="myChart" width="20" height="20"></canvas>';
			        table += '</div></td>';
	              table += '</tr>';
	              table += '<tr>';
	                table += '<td>Beta</td>';
	                table += '<td>200.4</td>';
	                table += '<td><div class="row">';
			        table +=  '<canvas id="myChart" width="20" height="20"></canvas>';
			        table += '</div></td>';
	              table += '</tr>';
	              table += '<tr>';
	                table += '<td>Gamma</td>';
	                table += '<td>3500.6</td>';
	                table += '<td><div class="row">';
			        table +=  '<canvas id="myChart" width="20" height="20"></canvas>';
			        table += '</div></td>';
	              table += '</tr>';
	            table += '</tbody>';
	          table += '</table>';
	        table += '</div>';
	    table += '</div>';
    	$('#tables-spot').append(table);
    }

    function removeTable(classSelected) {
    	var classToRemove = classSelected.attr('id')
    	$('#'+classToRemove+'-table').remove();
    }


	// var randomScalingFactor = function(){ return Math.round(Math.random()*100)};
 //    var dataArray = [randomScalingFactor(), randomScalingFactor()];
 //    var lineChartData = {
 //      labels : ["0", "1"],
 //      datasets : [
 //        {
 //          label: "My Second dataset",
 //          fillColor : "rgba(151,187,205,0.2)",
 //          strokeColor : "rgba(151,187,205,1)",
 //          pointColor : "rgba(151,187,205,1)",
 //          pointStrokeColor : "#fff",
 //          pointHighlightFill : "#fff",
 //          pointHighlightStroke : "rgba(151,187,205,1)",
 //          data : dataArray
          
          
 //        }
 //      ]
 //    }

 //  window.onload = function(){
 //    var ctx = document.getElementById("myChart").getContext("2d");
 //    window.myLine = new Chart(ctx).Line(lineChartData, {
 //      responsive: false,
 //      bezierCurve : false,
 //      datasetFill : false,
 //      pointDot : false,
 //      animation: true,
 //      animationSteps: 60
 //    });
 //    var count = 1;
 //    window.setInterval(function(){
 //      /// call your function here
 //      dataArray.push(count);
 //      count += 2;
 //      if (count >= 30*4) {
 //        window.myLine.removeData();
 //      };
 //      window.myLine.addData([randomScalingFactor()], count);
      
 //    }, 250);
 //  }
});

