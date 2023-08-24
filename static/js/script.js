console.log("Hii")

const input = document.getElementsByTagName('input');
input.addEventListener('keyup', function() {
    const query = input.value;
    console.log(query);

    fetch('/search', {
        method: 'POST',
        body: query
    });
});
