app.directive('dweet', function(restApi){
    return {
        restrict: 'E',
        scope: {
            dweetObj: '=data'
        },
        templateUrl: 'templates/dweet-template.html',
        link: function(scope, element, attrs) {
            scope.likeDweet = function(id){
                restApi.likeDweet(id).then(function(response){
                    scope.dweetObj.current_user_liked = response.data.current_user_liked;
                    scope.dweetObj.likes_count = response.data.total_likes;
                }, function(response){
                    console.error(response)
                })
            }
        }
    }
})

app.factory('restApi', function($http){
    function likeDweet(dweet_id){
         return $http.post('/api/like-dweet', {'dweet_id': dweet_id})

    }

    function getHomepageFeed(){
        return $http.post('/get-feed')

    }
    return {
        likeDweet : likeDweet,
        getFeed : getHomepageFeed
    }
})