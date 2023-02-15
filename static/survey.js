
const checkbox = document.querySelector('#cats-yes');
const conditional = document.querySelector('.conditional');
checkbox.addEventListener('change', () => {
    if (checkbox.checked) {
        conditional.style.display = "block";
    } else {
        conditional.style.display = "none";
    }
});
