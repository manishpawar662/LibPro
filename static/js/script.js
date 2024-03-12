console.log("Hii")


function submitSearchForm() {
    console.log("pf")
    document.getElementById('searchForm').submit();
}
window.onload = function() {
document.getElementById("searchRecord").focus();
};

input=document.getElementById("searchbook");
input.focus();
input.setSelectionRange(input.value.length, input.value.length);