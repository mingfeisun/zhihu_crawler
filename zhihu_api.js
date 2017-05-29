/**
* Created by mingfeisun on 27/5/2017.
*/
let zhihu = require("zhihu");
let username = "charles-wang-2012";

// zhihu.User.info(username).then(function(user){
//   console.log(user);
// });

// let url = 'http://www.zhihu.com/collection/25547043?page=1';
// Collection.getDataByPage(url);

// let topicID = '19778317';
// zhihu.Topic.getTopicByID(topicID).then(function(result){
//   console.log(result);
// });

// let postUrl = "https://zhuanlan.zhihu.com/p/24241616";
let config = {limit:100, offset:100};
zhihu.Post.page('ethanlam', config).then(function(data){
    console.log(data.length);
    console.log(data);
});

// zhihu.Post.info(postUrl).then(function(data){
//     console.log(data);
// });

// zhihu.Post.likersDetail(postUrl, config).then(function(data){
//     console.log(data);
// });

// zhihu.Post.comments(`https://zhuanlan.zhihu.com/p/24241616?refer=chenyuz`).then(function(comments){
//   console.log(comments);
// });
