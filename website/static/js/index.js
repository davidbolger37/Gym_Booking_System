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

document.addEventListener('DOMContentLoaded', (event) => {
    const flashMessage = document.getElementById('flash-message');
    if (flashMessage) {
        setTimeout(() => {
            flashMessage.classList.add('fade-out');
        }, 4000); // 4000ms or 4 seconds until fade-out starts
    }
});