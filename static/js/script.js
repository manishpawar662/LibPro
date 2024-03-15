console.log("Hii")

function validateconditionstransaction() {
    var dateIssued = new Date(document.getElementById('date_issued').value);
    var dateReturned = new Date(document.getElementById('date_returned').value);

    if (dateIssued > dateReturned) {
        alert('Date Issued must be before Date Returned');
        return false; // Prevent form submission
    }

    if (!validateSelection('memberid', 'memberidlist', 'MemberID')) {
        return false;
    }

    if (!validateSelection('bookid', 'bookidlist', 'BookID')) {
        return false;
    }

    if (document.getElementById('transactionidlist').querySelector(`option[value="${document.getElementById('transactionid').value}"]`)) {
        alert('Transaction ID already exists');
        return false; // Prevent form submission
    }

    return true; // Allow form submission
}

function validateSelection(inputId, listId, label) {
    var input = document.getElementById(inputId);
    var options = document.getElementById(listId).getElementsByTagName('option');

    for (var i = 0; i < options.length; i++) {
        if (input.value === options[i].value) {
            return true;
        }
    }

    alert(`Choose Appropriate ${label}`);
    return false;
}
function validateconditionsbooks(){
    var input = document.getElementById('bookid');
    var options = document.getElementById('bookidlist').getElementsByTagName('option');

    for (var i = 0; i < options.length; i++) {
        if (input.value === options[i].value) {
        alert('Book ID already exists');
        input.value = ''; // Clear the input field
        input.focus(); // Focus on the input field for correction
        return false; // Exit the function
        }
    }


}

function validateconditionsmembers(){
    var input = document.getElementById('memberid');
    var options = document.getElementById('memberidlist').getElementsByTagName('option');

    for (var i = 0; i < options.length; i++) {
        if (input.value === options[i].value) {
        alert('Member ID already exists');
        input.value = ''; // Clear the input field
        input.focus(); // Focus on the input field for correction
        return false; // Exit the function
        }
    }

}