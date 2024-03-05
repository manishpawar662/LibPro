console.log("Hii")

// const input = document.getElementsByTagName('input');
// input.addEventListener('keyup', function() {
//     const query = input.value;
//     console.log(query);

//     fetch('/search', {
//         method: 'POST',
//         body: query
//     });
// });
$(document).ready(function() {
    $('#searchbook').on('input', function() {
        console.log(($(this).val()))
        var searchValue = $(this).val();
        $.ajax({
            url: '/search/books',
            type: 'POST',
            data: { searchitem: searchValue },
            success: function(response) {
                // Handle the response from Flask (if needed)
            },
            error: function(xhr, status, error) {
                // Handle errors
            }
        });
    });
});
