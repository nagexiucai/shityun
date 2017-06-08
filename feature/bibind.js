/*
** 建立以form为单位的双向（模型和视图）绑定
** 拿form.id作为单元定位（要求form.id等于绑定的BiBind对象名）
** 取class是bb的子节点添加观察者模式
** 用bbq指出绑定的属性（要求bbq等于绑定的BiBind对象的对应属性名）
** 支持input/select/textarea标签
** 只响应change事件
** 不支持单元嵌套
*/

function BiBind(id,attrs){
    this.attrs = attrs || {};
    this.watchers = {};
    this.id = id;
    this.compile();
}

// TODO: 用Object.defineProperty改写
BiBind.prototype.compile = function() {
    var unit = document.getElementById(this.id);
    var childs = unit.getElementsByClassName("bb");
    for (var i=0; i<childs.length; i++) {
        childs[i].bb = this;
        function trigger(evt) {
            this.bb.attrs[this.getAttribute("bbq")] = this.value;
            for (var j=0; j<this.bb.watchers[this.getAttribute("bbq")].length; j++) {
                if (this.bb.watchers[this.getAttribute("bbq")][j] === this) {
                    continue;
                }
                this.bb.watchers[this.getAttribute("bbq")][j].value = this.value;
            }
        }
        childs[i].value = this.attrs[childs[i].getAttribute("bbq")];
        if (!this.watchers.hasOwnProperty(childs[i].getAttribute("bbq"))) {
            this.watchers[childs[i].getAttribute("bbq")] = [];
        }
        this.watchers[childs[i].getAttribute("bbq")].push(childs[i]);
        if (childs[i].tagName == "INPUT") {
            if (childs[i].type == "text") {
                childs[i].oninput = trigger;
            }
        }
        else {
            childs[i].onchange = trigger;
        }
    }
};

var test = new BiBind("test",{
    user: "那个秀才",
    owner: "曹操"
});