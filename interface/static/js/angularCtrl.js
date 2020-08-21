var app = angular.module('dwitterAngularModule',[]);

app.config(function($interpolateProvider, $httpProvider){
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
    $httpProvider.defaults.xsrfCookieName=  "csrftoken";
    $httpProvider.defaults.xsrfHeaderName=  "X-CSRFToken";

});



app.controller('dwitterCtrl', ['$scope','menuItems','restApi','$window', function(scope,menuItems,restApi,$window){
    window.scope = scope;
    scope.DWEET_CHAR_LIMIT = 140;
    scope.DWEET_DP_DIMENSIONS = 49;
    scope.currentUser = {}
    console.log("ROARING......")
    restApi.getCurrentUser().then(function(response){
                    scope.currentUser = response.data;
                    scope.menuItems = menuItems(scope.currentUser.username)
                }, function(response){
                    console.error(response)
                })

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

    scope.homepageInit = function(){
        loadFeeds();
        activePage = "homepage";

    }

//    called on clicking comment logo (within dweet directive)
    scope.commentWindow = function(dweet){
        console.log(dweet);
        $("#commentDweetModal").modal('show')
        scope.dweetObj = dweet;
    }

    scope.commentOnDweet = function(dweet, comment){
        if (!comment.length)
            return;
//        console.log(dweet,' ',comment);
        restApi.comment(dweet.id, comment).then(function(response){
            if (response.data.status === 201){
                $("#commentDweetModal").modal('hide')
                dweet.comments_count = response.data.total_comments;
                if (activePage == "commentsView") {
                    scope.commentsList.push(response.data.comment)
                }

            }
//            console.log(response.data);
            }, function(response){
                console.error(response)
            })
    }


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


    window.wins = $window;

    scope.selectDweet = function(dweet){
        console.log(dweet);
//        scope.commentsViewDweet = dweet;
        $window.location.href = "/"+dweet.username+"/status/"+dweet.id;
    }



    /*
        Section for comment view page
    */
    scope.commentsView = function(){
        activePage = "commentsView";
        var url = $window.location.pathname;
        restApi.commentsView(url).then(function(response){
                console.log(response.data);
                if (response.data.status === 200){
                    scope.dweetInfo = response.data.dweet_info;
                    scope.commentsList = response.data.comments_list;
                }
            }, function(response){
                console.error(response)
            })
    }


    scope.likeDweet = function(id){
                restApi.likeDweet(id).then(function(response){
                    scope.dweetInfo.current_user_liked = response.data.current_user_liked;
                    scope.dweetInfo.likes_count = response.data.total_likes;
                }, function(response){
                    console.error(response)
                })
            }


}])

app.controller('profileCtrl', ['$scope','restApi','$window', function(scope, restApi, $window){
    window.ps = scope;
    scope.profile = {};
    scope.editProfile = {"bio":""};
    scope.PROFILE_DP_DIMENSIONS = 134;
    scope.BIO_CHAR_LIMIT = 160

    var url = $window.location.pathname;

    const followObject = {classes: ["c-b","bo_blue"], btnText: "Follow"},
            followingObject = {classes: ["dark-sky-back","c-w"], btnText: "Following"};

    restApi.getUserProfile(url).then(function(response){
                    scope.profile.userInfo = response.data.profile_info;
                    scope.profile.userDweets = response.data.user_dweets;
                    scope.profile.likedDweets = response.data.liked_dweets;
//                    console.log(response.data);
                    toggleProfileFollow(response.data)
                }, function(response){
                    console.error(response)
                })

    scope.followUser = function(username){
        restApi.followUser(username).then(function(response){
//                    console.log(response.data);
                    toggleProfileFollow(response.data)
                }, function(response){
                    console.error(response)
                })
    }

    function toggleProfileFollow(data){
        if (data.my_profile)
            scope.showFollowBtn = false;
        else{
            scope.showFollowBtn = true;
            if (data.following)
                scope.classesArr = followingObject;
            else
                scope.classesArr = followObject;
        }
    }

    scope.saveProfile = function(){
        console.log(scope.editProfile);
    }
}])


app.constant('menuItems', function(username){
    return [
        {"name": "Home", "icon":"home", "url":"/home"},
        {"name":"Bookmarks", "icon":"bookmark", "url":"#"},
        {"name":"Profile", "icon":"person", "url": "/profile/"+username}
    ]
})