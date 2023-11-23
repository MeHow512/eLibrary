$(document).ready(function() {
    /*Listens for event if user fills all input-boxes in login form */
    $('#email-login-box, #password-login-box').on('input', function() {
        const emailValue = $('#email-login-box').val().trim();
        const passwordValue = $('#password-login-box').val().trim();

        if (emailValue !== '' && passwordValue !== '') {
            $('#login-button').prop('disabled', false);
        } else {
            $('#login-button').prop('disabled', true);
        }
    });
});
