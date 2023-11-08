function expandTextarea(element) {
    element.style.height = "auto";
    element.style.height = (element.scrollHeight + 10) + "px";
}

// Функція для відкриття/закриття меню при кліку на кнопку dropdown
function toggleDropdown() {
            document.getElementById("dropdownMenu").classList.toggle("show");
        }

function selectItem(value) {
    document.getElementById("selectedItem").value = value;
    document.getElementById("selectedItemButton").innerText = "Selected: " + value;
    document.getElementById("dropdownMenu").classList.remove("show");
}

// Закрити випадаюче меню при кліку поза ним
window.onclick = function(event) {
    if (!event.target.matches('.dropdown-toggle')) {
        var dropdowns = document.getElementsByClassName("dropdown-menu");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
};

const noteContents = document.querySelectorAll('.note-content');
const openButtons = document.querySelectorAll('.open-button');

openButtons.forEach((button, index) => {
    let isExpanded = false;

    button.addEventListener('click', function() {
        isExpanded = !isExpanded;
        if (isExpanded) {
            noteContents[index].style.webkitLineClamp = 'initial';
            noteContents[index].style.overflow = 'initial';
            noteContents[index].style.textOverflow = 'initial';
            button.innerText = 'Close';
        } else {
            noteContents[index].style.webkitLineClamp = '3';
            noteContents[index].style.overflow = 'hidden';
            noteContents[index].style.textOverflow = 'ellipsis';
            button.innerText = 'Open';
        }
    });
});

const editButtons = document.querySelectorAll('.edit-button');
const editForms = document.querySelectorAll('.edit-form');

editButtons.forEach((button, index) => {
    button.addEventListener('click', function() {

        const form = editForms[index];
        if (form.style.display === 'none') {
            // Відкриття форми
            form.style.display = 'block';
            button.innerText = 'Cancel'; // Зміна тексту кнопки на "Cancel"
            const textarea = form.querySelector('textarea');
            expandTextarea(textarea);
        } else {
            // Закриття форми
            form.style.display = 'none';
            button.innerText = 'Edit'; // Зміна тексту кнопки на "Edit"
        }
    });
});









let card = document.querySelector(".card-user-profile"); //declearing profile card element
let displayPicture = document.querySelector(".display-picture"); //declearing profile picture

displayPicture.addEventListener("click", function() { //on click on profile picture toggle hidden class from css
card.classList.toggle("hidden")})



