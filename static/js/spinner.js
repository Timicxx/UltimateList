function toggleSpinner() {

    let form = document.getElementById('form');
    form.classList.remove('d-block');
    form.classList.add('d-none');
    let spinner = document.getElementById('spinner');
    spinner.classList.remove('d-none');
    spinner.classList.add('d-block');
}