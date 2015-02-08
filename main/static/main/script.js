function storyController($scope, $http) {
	$scope.stories = [];
	$scope.myData = {};
	$scope.requestLifeStart = function() {
		/*var responsePromise = $http.get("shypaint.com:8001/run/");
		responsePromise.success(function(data, status, headers, config) {});
		responsePromise.error(function(data, status, headers, config) {
			alert("AJAX failed :(");
		});*/
		var xmlHttp = new XMLHttpRequest();
		xmlHttp.open('GET', 'http://shypaint.com:8001/run/', false);
		xmlHttp.send(null);
        if (xmlHttp.responseText == 'Ok'){
            setInterval(function(){$scope.requestLifeData();}, 2000);
        }
	}
	$scope.requestLifeData = function() {
		var responsePromise = $http.get("http://shypaint.com:8001/ref/");
		responsePromise.success(function(data, status, headers, config) {
			angular.forEach(data, function(value, key) {
				$scope.stories.unshift({
					content: value.content.split("*").join($scope.name),
					intel: value.intel,
					health: value.health,
					look: value.look,
					isEvent: value.isEvent
				});
			});
		});
		responsePromise.error(function(data, status, headers, config) {
			alert("AJAX failed :(");
		});
	}
	$scope.fakeInput = function(str) {
		$scope.stories.push({
			string: str
		});
	}
}
