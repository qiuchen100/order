;
var user_edit_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $('.user_edit_wrap .save').click(
          function () {
            var mobile_target = $('.user_edit_wrap input[name="mobile"]');
            var mobile = mobile_target.val();
            var nickname_target = $('.user_edit_wrap input[name="nickname"]');
            var nickname = nickname_target.val();
            var email_target = $('.user_edit_wrap input[name="email"]');
            var email = email_target.val();

            var btn_target = $(this);
            if (btn_target.hasClass('disabled')) {
                common_ops.alert('正在处理，请勿重复点击！')
            }

            if (mobile == undefined || mobile.length < 1) {
                common_ops.tip('请输入正确的手机号！', mobile_target);
                return;
            }

            if (nickname == undefined || nickname.length < 1) {
                common_ops.tip('请输入正确的姓名！', nickname_target);
                return;
            }
            if (email == undefined || email.length < 1) {
                common_ops.tip('请输入正确的邮箱！', nickname_target);
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
                            window.location.href = window.location.href;
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