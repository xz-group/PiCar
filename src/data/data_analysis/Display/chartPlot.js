//This js is based on chart.js
//https://www.chartjs.org

var ctx = document.getElementById("myChart");
var maxDataSets = 50;


//make the initial blank chart
//just have imu ax and imu ay
var chart = new Chart(ctx,{
  type: 'line',
  data: {
    labels:[],
    datasets: [{
      label: 'imu accelaration x',
      borderColor:"red",
      data: [],
      borderWidth:1
    },
    {
      label: 'imu accelaration y',
      borderColor:"blue",
      data: [],
      borderWidth:1
    }]
  },
  options:{
    responsive:false,
  }

})


//update the chart based on option
var updateDataChart = function(optionString){
  if(optionString === "add"){
    var allRowData3 = csvData.data[time]
    var dataTime3 = allRowData3[0]
    var imuAX3 = allRowData3[2]
    var imuAY3 = allRowData3[3]
    var dataSet3 = [imuAX3,imuAY3]
    addData(chart,dataTime3,dataSet3);
  }
  else if(optionString === "remove"){
    removeData(chart);
  }
  else if(optionString === "clear"){

  }

}


//add data to the front of graph
//used for keeping max data sets displayed
function unshiftData(chart,label,dataSet){
    chart.data.labels.unshift(label);
    var count = 0;
    chart.data.datasets.forEach((dataset) => {
        dataset.data.unshift(dataSet[count]);
        count++;
    });
    chart.update();
}


//add data based to the end of graph
function addData(chart, label, dataSet) {
    chart.data.labels.push(label);
    var count = 0;
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(dataSet[count]);
        count++;
    });
    if(chart.data.labels.length > maxDataSets){
      shiftData(chart);
    }
    chart.update();
}


//remove first data
//used for keeping max data sets displayed
function shiftData(chart){
  chart.data.labels.shift();
  chart.data.datasets.forEach((dataset) => {
      dataset.data.shift();
  });
  chart.update();
}


//remove last data
function removeData(chart) {
    chart.data.labels.pop();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.pop();
    });
    //console.log("Time is:" + time)
    //console.log("maxDataSets is:" + maxDataSets)
    //console.log("labels length is:" + chart.data.labels.length)
    var LeftDataNumber = time + 1
    if(chart.data.labels.length < maxDataSets){
      if(LeftDataNumber > maxDataSets || LeftDataNumber == maxDataSets){
        //console.log("we decide to add to the front for index " + (time + 1 - maxDataSets))
        var allRowData4 = csvData.data[LeftDataNumber - maxDataSets]
        var dataTime4 = allRowData4[0]
        var imuAX4 = allRowData4[2]
        var imuAY4 = allRowData4[3]
        var dataSet4 = [imuAX4,imuAY4]
        unshiftData(chart,dataTime4,dataSet4);
      }
    }
    chart.update();
}
