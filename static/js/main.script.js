$(document).ready(function () {
	var token = '08cb018327f57109a6f65e6f45465f347f99c69a';
	$(".address").suggestions({
		token: token,
		type: "ADDRESS",
		// onSelect: function (suggestion) {
		// 	console.log(suggestion);
		// }
	});
});