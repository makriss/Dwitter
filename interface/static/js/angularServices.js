app.directive('dweet', function(restApi){
    return {
        restrict: 'E',
        scope: {
            dweetObj: '=data',
            comment: '&commentWindow'
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

    function postDweet(dweet){
        return $http.post('/api/post-dweet', {'dweet': dweet})
    }

    function commentOnDweet(dweetId, comment){
        return $http.post('/api/post-comment', {'dweet_id': dweetId, "comment": comment})
    }

    function commentsViewData(url){
        return $http.post(url)
    }

    function getUserProfile(url){
        return $http.post(url)
    }

    function followUser(username){
        return $http.post('/profile/follow-user',{'follow_username':username})
    }

    return {
        likeDweet : likeDweet,
        getFeed : getHomepageFeed,
        postDweet : postDweet,
        comment: commentOnDweet,
        commentsView: commentsViewData,
        getUserProfile: getUserProfile,
        followUser: followUser
    }
})