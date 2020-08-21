app.directive('dweet', function(restApi){
    return {
        restrict: 'AE',
        scope: {
            dweetObj: '=data',
            comment: '&commentWindow'
        },
//        templateUrl: 'templates/dweet-template.html',
        templateUrl: function(elm, attrs) {
            return attrs.template;
          },
        link: function(scope, element, attrs) {
            scope.DWEET_DP_DIMENSIONS = 49;

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
        restrict: 'AE',
        scope: {
            currentUser: '=data'
        },
//        templateUrl: 'templates/logout-popup.html',
        templateUrl: function(elm, attrs) {
            return attrs.template;
          },
        link: function(scope, elm, attrs) {
            scope.PROFILE_DP_DIMENSIONS = 39;
            scope.showPopup = false;

            scope.togglePopup = function(){

                if (!scope.showPopup){
                    scope.showPopup = true;
                    parent = $(elm.children()[0]);
                    popup = $(elm.children()[1]);
                    popup.css('bottom', parent.outerHeight());
                }
                    else
                        scope.showPopup = false;
            }

            scope.logoutUser = function(){
                $http.post('/accounts/logout').then(function(result){
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

    function editProfile(data){
        return $http.post('/profile/edit-profile', {'profile_data': data})
    }

    return {
        getCurrentUser: getCurrentUser,
        likeDweet : likeDweet,
        getFeed : getHomepageFeed,
        postDweet : postDweet,
        comment: commentOnDweet,
        commentsView: commentsViewData,
        getUserProfile: getUserProfile,
        followUser: followUser,
        editProfile: editProfile
    }
})