$(document).ready(function() {
    /*Listens for event if user fills all input-boxes in register form and if pesel has correct fill */
    $('#login-register-box, #email-register-box, #password-register-box, #pesel-register-box').on('input', function() {
        const loginValue = $('#login-register-box').val().trim();
        const emailValue = $('#email-register-box').val().trim();
        const passwordValue = $('#password-register-box').val().trim();
        const peselValue = $('#pesel-register-box').val().trim();
        const peselRegex = /^[0-9]+$/;
        let registerButtonState = true;

        if (loginValue !== '' && emailValue !== '' && passwordValue !== '' && peselValue !== '') {
            if (peselRegex.test(peselValue) && peselValue.length === 11) {
                registerButtonState = false;
            }
        }
        $('#register-button').prop('disabled', registerButtonState);
    });
});
