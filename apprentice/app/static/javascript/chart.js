//var context = document.getElementById("nutrition-info").getContext('2d');
//
//var myPieChart = new Chart(ctxP, {
//type: 'pie',
//data: {
//labels: ["Carbohydrates", "Proteins", "Fats"],
//datasets: [{
//data: [300, 50, 100],
//backgroundColor: ["#B3C1E3", "#BAE3B3", "#D6A7A7"],
//hoverBackgroundColor: ["#26729E", "#5D9464", "#B54343"]
//}]
//},
//options: {
//responsive: true
//}
//});

//pie
var ctxP = document.getElementById("pieChart").getContext('2d');
var myPieChart = new Chart(ctxP, {
type: 'pie',
data: {
labels: ["Red", "Green", "Yellow", "Grey", "Dark Grey"],
datasets: [{
data: [300, 50, 100, 40, 120],
backgroundColor: ["#F7464A", "#46BFBD", "#FDB45C", "#949FB1", "#4D5360"],
hoverBackgroundColor: ["#FF5A5E", "#5AD3D1", "#FFC870", "#A8B3C5", "#616774"]
}]
},
options: {
responsive: true
}
});