// Get the input element
console.log("Hii")
const input = document.querySelector('#searchitem');

// Listen for the keyup event on the input element
input.addEventListener('keyup', function() {
    // Get the value of the input field
    const query = input.value;
    console.log(query)
    // const data = new URLSearchParams();
    // data.append('q', query);
    // console.log("data-",data)
    
    fetch('/searchbook', {
        method: 'POST',
        body: query
    });
});
