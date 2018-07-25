var time = 0;
var csvData;
var photoPos = 0; // the photo index in synchronized data row
var AllphotoPath = "../data_photo/camera/"; // path where you save all photos from one experiment
var PlayTimer
imageDiv = document.getElementById("image_div"); //where we put the photo

//following are all data from one csv file
var allTime = [];
var allLidarData = [];
var allimuAX = [];
var allimuAY = [];
var allimuAZ = [];
var allimuGX = [];
var allimuGY = [];
var allimuGZ = [];

//search and jump to a given time
var time_search = function(){
  var given_time = document.getElementById("time_search").value;
  if(isNaN(given_time)){
    alert("Please give a time")
  }
  else{
    console.log("Given time is " + given_time);
    var time_index;
    for(time_index = 0; time_index < allTime.length; time_index++){
      if(allTime[time_index] == given_time){
        console.log("We find the time, index is " + time_index);
        while(time != time_index){
          document.getElementById('next_button').click();
        }
        break;
      }
    }

  }

}
document.getElementById('time_serach_button').addEventListener('click',time_search)

//jump to the first row of all data
var jump_first = function(){
  while(time > 0){
    document.getElementById('prev_button').click();
  }

}
document.getElementById("first_button").addEventListener('click',jump_first)


//stop the auto play
var stopAutoPlay = function(){
  clearInterval(PlayTimer)
  console.log("you stop the auto play")
  document.getElementById("autoPlay_button").hidden = false
  document.getElementById("autoPlay_frequency").hidden = false
  document.getElementById("autoPlay_stop").hidden = true
}
document.getElementById('autoPlay_stop').addEventListener('click',stopAutoPlay)


//timer for autoplay
var autoPlayTimer = function(){
  if(time == csvData.data.length - 1 || time > (csvData.data.length - 1)){
    clearInterval(PlayTimer)
    document.getElementById("autoPlay_button").hidden = false
    document.getElementById("autoPlay_frequency").hidden = false
    document.getElementById("autoPlay_stop").hidden = true
  }
  else{
    document.getElementById('next_button').click()
  }

}


var autoPlay = function(){
    var frequency = 1000;
    if(! isNaN(document.getElementById("autoPlay_frequency").value)){
      frequency = document.getElementById("autoPlay_frequency").value * 1000;
    }

    PlayTimer = setInterval(autoPlayTimer,frequency)
    //hide autoplay button, show stop button
    document.getElementById("autoPlay_button").hidden = true
    document.getElementById("autoPlay_frequency").hidden = true
    document.getElementById("autoPlay_stop").hidden = false
}
document.getElementById("autoPlay_button").addEventListener('click',autoPlay)


//move to next data row
var increaseTime = function(){
  time = time + 1;
  console.log(time)
  if(time == csvData.data.length || time > csvData.data.length){
    alert("no more afterwards data")
    clearInterval(PlayTimer)
    time = time - 1
    console.log(time)
  }
  else{
    updateData();
    updateImage();
    updateDataChart("add");
  }

}
document.getElementById('next_button').addEventListener('click',increaseTime)


//move to previous data row
var decreaseTime = function(){
  time = time - 1;
  console.log(time);
  if (time < 0){
    alert("no more previous data")
    time = time + 1
    console.log(time)
  }
  else{
    updateData();
    updateImage();
    updateDataChart("remove");
  }

}
document.getElementById("prev_button").addEventListener('click',decreaseTime)


//parse csv file by PapaParse package
//https://www.papaparse.com
function loadFileAsText(){
  var fileToLoad = document.getElementById("fileToLoad").files[0];
  Papa.parse(fileToLoad, {
    delimiter: ",",
    header: false,
  	complete: function(results) {
      csvData = results;
  		//console.log(results);
      document.getElementById("move_button").hidden = false;
      photoPos = csvData.data[time].length - 1;
      updateData();
      updateImage();
      updateDataChart("add");
      updateAllPlot();
  	}
  });
}


//update data on the page based on updated time
function updateData(){
  var allRowData = csvData.data[time]
  var dataTime = allRowData[0]
  var Lidar = allRowData[1]
  var imuAX = allRowData[2]
  var imuAY = allRowData[3]
  var imuAZ = allRowData[4]
  var imuGX = allRowData[5]
  var imuGY = allRowData[6]
  var imuGZ = allRowData[7]
  document.getElementById('time_data').innerHTML = "<h3>" + "Time:  " + dataTime + "</h3> <br>";
  document.getElementById('lidar_data').innerHTML = "<h3>" + "Lidar distance:  " + Lidar + "</h3> <br>";
  document.getElementById('imu_data').innerHTML = "<h3>" + "IMU data:  " + imuAX + ",  " + imuAY + ",  "
  + imuAZ + ",  " + imuGX + ",  " + imuGY + ",  " + imuGZ + "</h3>";

}


//update image on the page based on updated time
function updateImage(){
  var allRowData2 = csvData.data[time];
  filePath = AllphotoPath + allRowData2[photoPos]
  //console.log(filePath)
  if(!(allRowData2[photoPos] === undefined)){
    imageDiv.innerHTML = ""
    var image = document.createElement("img");
    image.setAttribute('src',filePath)
    image.setAttribute('width','400')
    image.setAttribute('height','400')
    imageDiv.appendChild(image);
  }

}



//update plots with all data
var updateAllPlot = function(){
    var index;
    for(index = 0; index < csvData.data.length; index++){
      var allRowData7 = csvData.data[index]
      var dataTime7 = allRowData7[0]
      var Lidar7 = allRowData7[1]
      var imuAX7 = allRowData7[2]
      var imuAY7 = allRowData7[3]
      var imuAZ7 = allRowData7[4]
      var imuGX7 = allRowData7[5]
      var imuGY7 = allRowData7[6]
      var imuGZ7 = allRowData7[7]
      allTime.push(dataTime7);
      allLidarData.push(Lidar7);
      allimuAX.push(imuAX7);
      allimuAY.push(imuAY7);
      allimuAZ.push(imuAZ7);
      allimuGX.push(imuGX7);
      allimuGY.push(imuGY7);
      allimuGZ.push(imuGZ7);
    }

    lidarPlot.data.labels = allTime;
    lidarPlot.data.datasets[0].data = allLidarData;
    lidarPlot.update();

    imuAPlot.data.labels = allTime;
    imuAPlot.data.datasets[0].data = allimuAX;
    imuAPlot.data.datasets[1].data = allimuAY;
    imuAPlot.data.datasets[2].data = allimuAZ;
    imuAPlot.update();

    imuGPlot.data.labels = allTime;
    imuGPlot.data.datasets[0].data = allimuGX;
    imuGPlot.data.datasets[1].data = allimuGY;
    imuGPlot.data.datasets[2].data = allimuGZ;
    imuGPlot.update();

    console.log("finished")
}
