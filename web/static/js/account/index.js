;
var account_index_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $('.wrap_search .search').click(
          function () {
            $('.wrap_search').submit();
          }
        );
        $('.remove').click(
          function () {
            var uid = $(this).attr("data");

            var btn_target = $(this);
            if (btn_target.hasClass('disabled')) {
                common_ops.alert('正在处理，请勿重复点击！')
            }

            $.ajax({
                url: common_ops.buildUrl('/account/ops'),
                type: 'POST',
                data: {'uid': uid},
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass('disabled');
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl('/account/index');
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
    account_index_ops.init();
});