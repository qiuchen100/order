;
var user_edit_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $('.user_edit_wrap .save').click(
          function () {
            var mobile = $('.user_edit_wrap input[name="mobile"]').val();
            var nickname = $('.user_edit_wrap input[name="nickname"]').val();
            var email = $('.user_edit_wrap input[name="email"]').val();

            var btn_target = $(this);
            if (btn_target.hasClass('disabled')) {
                common_ops.alert('正在处理，请勿重复点击！')
            }

            if (mobile == undefined || mobile.length < 1) {
                common_ops.alert('请输入正确的手机号！');
                return;
            }

            if (nickname == undefined || nickname.length < 1) {
                common_ops.alert('请输入正确的姓名！');
                return;
            }
            if (email == undefined || email.length < 1) {
                common_ops.alert('请输入正确的邮箱！');
                return;
            }
            btn_target.addClass('disabled');
            $.ajax({
                url: common_ops.buildUrl('/user/edit'),
                type: 'POST',
                data: {'mobile': mobile, 'nickname': nickname, 'email': email},
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass('disabled');
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl('/user/edit');
                        };
                    }
                    common_ops.alert(res.msg, callback);
                },
                error: function () {
                    btn_target.removeClass('disabled');
                    common_ops.alert('服务暂时不可用，请稍后再尝试！');
                }
            });
          }
        );
    }
};
$(document).ready(function () {
    user_edit_ops.init();
});