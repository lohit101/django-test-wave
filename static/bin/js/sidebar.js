var menuBtn = document.getElementById('menuBtn');
var sidebar = document.getElementById('application-sidebar');

menuBtn.addEventListener('click', function () {
    menuBtn.classList.toggle('bg-gray-300');
    sidebar.classList.toggle('translate-x-0');
});