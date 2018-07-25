var showPlotPage = function(){
  document.getElementById("all_plot_div").hidden = false;
  document.getElementById("home_div").hidden = true;
}

document.getElementById('plotPage').addEventListener('click',showPlotPage)

var showHomePage = function(){
  document.getElementById('all_plot_div').hidden = true;
  document.getElementById('home_div').hidden = false;
}
document.getElementById('homePage').addEventListener('click',showHomePage)
