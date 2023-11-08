    const editButton = document.querySelector('.edit-button');
    const editable = document.querySelector('.editable');
    const nonEditable = document.querySelector('.non-editable');
    const saveButton = document.querySelector('.save-button');


    editButton.addEventListener('click', () => {
        editable.style.display = 'inline';
        nonEditable.style.display = 'none';
        editable.focus();
        saveButton.classList.remove('d-none');

    });

