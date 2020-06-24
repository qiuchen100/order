;
var food_set_ops = {
    init: function () {
        this.eventBind();
        this.initEditor();
    },
    eventBind: function () {
    },
    initEditor: function () {
        var that = this;
        var ue = UE.getEditor('editor', {
            serverUrl: common_ops.buildUrl("/upload/ueditor")
        });

    }
};
$(document).ready(function () {
    food_set_ops.init();
});