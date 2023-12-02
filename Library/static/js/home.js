import { showAlert } from './main_page.js';

$(document).ready(function() {
    /*Listens for the cancel button to be pressed*/
    $('#cancelAddBookModal').click(function() {
        $('#addBookModal').modal('hide');
        $('#bookName').val('');
        $('#bookImage').val('');
        $('#addBookModalButton').prop('disabled', true);
    });


    /*Listens if user set all data in modal add book form */
    $('#bookName, #bookImage').on('input', function() {
        let bookName = $('#bookName').val().trim();
        let bookImage = $('#bookImage').val().trim();

        if (bookName !== '' && bookImage !== '') {
            $('#addBookModalButton').prop('disabled', false);
        } else {
            $('#addBookModalButton').prop('disabled', true);
        }
    });


    /*Listens for the add button to be pressed*/
    $('#addBookModalButton').click(function() {
        let bookName = $('#bookName').val();
        let bookImage = $('#bookImage').prop('files')[0];

        let formData = new FormData();
        formData.append('book_name', bookName);
        formData.append('book_image', bookImage);

        $.ajax({
            url: '/add_book',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                if (response) {
                    showAlert(response['message'], response['status']);
                }
                location.reload();
            },
        });

        $('#addBookModal').modal('hide');
        $('#addBookModalButton').prop('disabled', true);
        $('#bookName').val('');
        $('#bookImage').val('');
    });


    /*Listens for the remove button to be pressed*/
    $('.book-remove-button').click(function() {
        let bookId = $(this).closest('.book-div').data('book-id');
        let bookName = $(this).closest('.book-div').data('book-name')
        let bookImg = $(this).closest('.book-div').data('book-img-name')

        $.ajax({
            url: '/remove_book',
            type: 'POST',
            data: { book_id: bookId, book_name: bookName, book_img: bookImg },
            success: function(response) {
                if (response) {
                    showAlert(response['message'], response['status']);
                }
                location.reload();
            },
        });
    });


    $('.book-edit-button').click(function() {
        let bookId = $(this).closest('.book-div').data('book-id');
        let saveChangesBtn = $('#editBookModalButton-' + bookId);

        let bookNameEditField = '#editNewBookNameModal-' + bookId;
        let bookImageEditField = '#editNewBookImageModal-' + bookId;


        /*Listens if user input all data in edit book modal and enable/disable button property*/
        $(bookNameEditField + ', ' + bookImageEditField).on('input', function() {
            let newBookName = $(bookNameEditField).val();
            let newBookImage = $(bookImageEditField).val();

            if (newBookName !== '' && newBookImage !== '') {
                saveChangesBtn.prop('disabled', false);
            } else {
                saveChangesBtn.prop('disabled', true);
            }
        });

        /*Listens if user clicked cancel button, and clear all fields in edit book modal*/
        $('#cancelEditBookModalButton-' + bookId).click(function() {
            clearEditModalFIelds(bookId);
            saveChangesBtn.prop('disabled', true);
        });

        /*Listens if user clicked edit button and saves the data entered by the user */
        $(saveChangesBtn).click(function() {
            let newBookName = $(bookNameEditField).val();
            let newBookImage = $(bookImageEditField).prop('files')[0];
            clearEditModalFIelds(bookId);
            saveChangesBtn.prop('disabled', true);

            let formData = new FormData();
            formData.append('book_id', bookId);
            formData.append('new_book_name', newBookName);
            formData.append('new_book_img', newBookImage);

            $.ajax({
                url: '/edit_book',
                type: 'POST',
                data: formData,
                contentType: false,
                processData: false,
                success: function(response) {
                    if (response) {
                        showAlert(response['message'], response['status']);
                    }
                    location.reload();
                },
            });
        });
    });

    /*Clear all fields in selected edit modal*/
    function clearEditModalFIelds(selectedModalId) {
        $('#editNewBookNameModal-' + selectedModalId).val('');
        $('#editNewBookImageModal-' + selectedModalId).val('');
    }
});