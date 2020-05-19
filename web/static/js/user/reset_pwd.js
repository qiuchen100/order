;
var user_reset_pwd_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $('#save').click(
          function () {
            var old_password = $('#old_password').val();
            var new_password = $('#new_password').val();
            var new_password2 = $('#new_password2').val();

            var btn_target = $(this);
            if (btn_target.hasClass('disabled')) {
                common_ops.alert('正在处理，请勿重复点击！')
            }

            if (old_password == undefined || old_password.length < 6) {
                common_ops.alert('请输入正确的原来的密码！');
                return;
            }

            if (new_password == undefined || new_password.length < 6) {
                common_ops.alert('新密码的长度至少为6位！');
                return;
            }

            if (new_password == old_password) {
                common_ops.alert('新密码不能和原来的密码相同！');
                return;
            }

            if (new_password != new_password2) {
                common_ops.alert('两次输入的密码不一致，请重新输入！');
                return;
            }

            btn_target.addClass('disabled');
            $.ajax({
                url: common_ops.buildUrl('/user/reset-pwd'),
                type: 'POST',
                data: {'old_password': old_password, 'new_password': new_password, 'new_password2': new_password2},
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass('disabled');
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl('/user/reset-pwd');
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
    user_reset_pwd_ops.init();
});