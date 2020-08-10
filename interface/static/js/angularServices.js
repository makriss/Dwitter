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

app.directive('logoutPopup', function(restApi, $http){
    return {
        restrict: 'E',
        scope: {
            currentUser: '=data'
//            comment: '&commentWindow'
        },
        templateUrl: 'templates/logout-popup.html',
        link: function(scope, elm, attrs) {
            console.log(elm.children()[1])

            scope.showPopup = false;

            scope.togglePopup = function(){

                if (!scope.showPopup){
                    scope.showPopup = true;
                    parent = $(elm.children()[0]);
                    popup = $(elm.children()[1]);
//                    popup.css(
//                        { top: parent.offset().top - parent.height() - 10 },
//                        { left: parent.offset().left  }
//                    )
                    console.log(parent.outerHeight());
                    popup.css('bottom', parent.outerHeight());
                }
                    else
                        scope.showPopup = false;



            }


            scope.logoutUser = function(){
                $http.post('/accounts/logout').then(function(result){
                    console.log(result);
                })
            }


        }
    }
})

app.factory('restApi', function($http){
    function getCurrentUser(){
         return $http.get('/accounts/current_user')
    }

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
        getCurrentUser: getCurrentUser,
        likeDweet : likeDweet,
        getFeed : getHomepageFeed,
        postDweet : postDweet,
        comment: commentOnDweet,
        commentsView: commentsViewData,
        getUserProfile: getUserProfile,
        followUser: followUser
    }
})