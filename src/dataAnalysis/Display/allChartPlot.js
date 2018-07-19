var lidarCanv = document.getElementById("lidarChart");
var imuACanv = document.getElementById("imuAChart");
var imuGCanv = document.getElementById("imuGChart");
var imuMCanv = document.getElementById("imuMChart");

//add data based to the end of graph
function addDataNoShift(chart, label, dataSet) {
    chart.data.labels.push(label);
    if(dataSet.constructor === Array){
      var count = 0;
      chart.data.datasets.forEach((dataset) => {
          dataset.data.push(dataSet[count]);
          count++;
      });
    }
    else{
      chart.data.datasets.forEach((dataset) => {
          dataset.data.push(dataSet);
      });
    }

    //chart.update();
}


var lidarPlot = new Chart(lidarCanv,{
  type: 'line',
  data: {
    labels:[],
    datasets: [{
      label: 'Lidar Distance',
      borderColor:"red",
      data: [],
      borderWidth:1
    }]
  },
  options:{
    responsive:false,
  }

})


var imuAPlot = new Chart(imuACanv,{
  type:'line',
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
    },
    {
      label: 'imu accelaration z',
      borderColor:"white",
      data:[],
      borderWidth:1
    }]
  },
  options:{
    responsive:false,
  }
})

var imuGPlot = new Chart(imuGCanv,{
  type:'line',
  data: {
    labels:[],
    datasets: [{
      label: 'imu gyro x',
      borderColor:"red",
      data: [],
      borderWidth:1
    },
    {
      label: 'imu gyro y',
      borderColor:"blue",
      data: [],
      borderWidth:1
    },
    {
      label: 'imu gyro z',
      borderColor:"black",
      data:[],
      borderWidth:1
    }]
  },
  options:{
    responsive:false,
  }
})
