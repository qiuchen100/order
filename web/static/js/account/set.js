;
var account_set_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $('.wrap_account_set .save').click(
          function () {
            var uid = $('.wrap_account_set input[name="id"]').val();
            var nickname_target = $('.wrap_account_set input[name="nickname"]');
            var nickname = nickname_target.val();
            var mobile_target = $('.wrap_account_set input[name="mobile"]');
            var mobile = mobile_target.val();
            var email_target = $('.wrap_account_set input[name="email"]');
            var email = email_target.val();
            var login_name_target = $('.wrap_account_set input[name="login_name"]');
            var login_name = login_name_target.val();
            var login_pwd_target = $('.wrap_account_set input[name="login_pwd"]');
            var login_pwd = login_pwd_target.val();

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
                common_ops.tip('请输入正确的邮箱！', email_target);
                return;
            }
            if (login_name == undefined || login_pwd.length < 1) {
                common_ops.tip('请输入正确的用户名！', login_name_target);
                return;
            }
            if (login_pwd == undefined || login_pwd.length < 6) {
                common_ops.tip('请输入正确的密码！', login_pwd_target);
                return;
            }

            if (uid == '' && login_pwd == '******') {
                common_ops.tip('请设置密码！', login_pwd_target);
                return;
            }


            btn_target.addClass('disabled');
            $.ajax({
                url: common_ops.buildUrl('/account/set'),
                type: 'POST',
                data: {'mobile': mobile, 'nickname': nickname, 'email': email, 'login_name': login_name, 'login_pwd': login_pwd, 'uid': uid},
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
    account_set_ops.init();
});