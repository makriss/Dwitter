var app = angular.module('dwitterAngularModule',[]);

app.config(function($interpolateProvider, $httpProvider){
    // $interpolateProvider.startSymbol("[[[");
    // $interpolateProvider.endSymbol("]]]");
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
    $httpProvider.defaults.xsrfCookieName=  "csrftoken";
    $httpProvider.defaults.xsrfHeaderName=  "X-CSRFToken";
});



app.controller('dwitterCtrl', ['$scope','menuItems','restApi', function(scope,menuItems,restApi){
    window.scope = scope;
    scope.DWEET_CHAR_LIMIT = 140;

    // loading side menu options
    scope.optionsMenu = menuItems()

    // Refactor to sending promises from present structure
    // https://stackoverflow.com/questions/20555472/can-you-resolve-an-angularjs-promise-before-you-return-it
    function loadFeeds(){
        restApi.getFeed().then(function(response){
                    scope.dweetsFeed = response.data;
                }, function(response){
                    console.error(response)
                })
    }
    loadFeeds()

    scope.postDweet = function(dweet){
        if (!dweet.length)
            return;

        restApi.postDweet(dweet).then(function(response){
                loadFeeds()
                $("#addDweetModal").modal('hide')
            }, function(response){
                console.error(response)
            })
    }

}])

app.constant('menuItems', function(){
    return [
        {"name": "Home", "icon":"home"},
        {"name":"Bookmarks", "icon":"bookmark"},
        {"name":"Profile", "icon":"person"}
    ]
})