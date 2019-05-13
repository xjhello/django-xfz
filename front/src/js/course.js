function Course() {

}

Course.prototype.enter = function () {
    var enter = $('.click');
    enter.click(function () {
         var course_id = enter.attr('course_id');
         console.log(enter);
         console.log(course_id);
         xfzajax.post({
             'url': '/course/course_detail',
             'data': {
               'course_detail': course_id
             },
             'success': function (result) {
                 console.log(result);
               if(result['code'] === 200){
                    console.log("================");
               }else {
                   window.messageBox.showError(result['message']);
               }
             },
         })
    })
};

Course.prototype.run = function () {
  this.enter();
};

$(function () {
   var course = new Course();
   course.run();
});