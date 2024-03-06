//Sidebar
function openNav() {
  document.getElementById("mySidebar").style.width = "250px";
}

function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
}

document.addEventListener('DOMContentLoaded', (event) => {
    document.querySelectorAll('.sidebar a').forEach(item => {
        item.addEventListener('click', closeNav);
    });
});