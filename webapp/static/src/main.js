require(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function($) {
	      $(".o1").click(function() {
	            window.alert("o1 selected");
	      });
	});


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

