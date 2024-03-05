//Sidebar
function openNav() {
  document.getElementById("mySidebar").style.width = "250px";
}

document.addEventListener('DOMContentLoaded', () => {
    // Define the closeNav function
    function closeNav() {
        document.getElementById('mySidebar').style.width = '0';
    }

    // Attach event listeners to sidebar links
    document.querySelectorAll('.sidebar a').forEach(item => {
        item.addEventListener('click', closeNav);
    });
});

