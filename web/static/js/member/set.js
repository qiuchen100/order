;
var member_set_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $('.wrap_member_set .save').click(
          function () {
            var btn_target = $(this);
            if (btn_target.hasClass('disabled')) {
                common_ops.alert('正在处理，请勿重复点击！')
            }

            var id = $('.wrap_member_set input[name="id"]').val();
            var nickname_target = $('.wrap_member_set input[name="nickname"]');
            var nickname = nickname_target.val();

            if (nickname == undefined || nickname.length < 1) {
                common_ops.tip('请输入正确的姓名！', nickname_target);
                return;
            }

            btn_target.addClass('disabled');
            $.ajax({
                url: common_ops.buildUrl('/member/set'),
                type: 'POST',
                data: {'nickname': nickname, 'id': id},
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass('disabled');
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl('/member/index');
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
    member_set_ops.init();
});