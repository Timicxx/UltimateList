function changeActive(cle) {
	
	var el = document.getElementsByClassName('active');
	for(var i = 0; i < el.length; i++) {
		el[i].classList.remove('active');
	}
	cle.parentElement.classList.add('active');
}