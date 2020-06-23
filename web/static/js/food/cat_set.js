;
var cat_set_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $('.wrap_cat_set .save').click(
          function () {
            var btn_target = $(this);
            if (btn_target.hasClass('disabled')) {
                common_ops.alert('正在处理，请勿重复点击！')
            }

            var id = $('.wrap_cat_set input[name="id"]').val();

            var name_target = $('.wrap_cat_set input[name="name"]');
            var name = name_target.val();
            if (name == undefined || name.length < 1) {
                common_ops.tip('请输入正确的分类名称！', name_target);
                return;
            }

            var weight_target = $('.wrap_cat_set input[name="weight"]');
            var weight = weight_target.val();
            if (parseInt(weight) < 1) {
                common_ops.tip('请输入符合规范的权重，必须为整数且大于等于1！', weight_target);
                return;
            }

            btn_target.addClass('disabled');
            $.ajax({
                url: common_ops.buildUrl('/food/cat-set'),
                type: 'POST',
                data: {'id': id, 'name': name, 'weight': weight},
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass('disabled');
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl('/food/cat');
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
    cat_set_ops.init();
});