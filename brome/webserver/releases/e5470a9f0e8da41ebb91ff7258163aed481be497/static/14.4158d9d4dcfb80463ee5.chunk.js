webpackJsonp([14],{12:function(e,t,r){"use strict";function a(e){return e&&e.__esModule?e:{"default":e}}Object.defineProperty(t,"__esModule",{value:!0});var s=r(3),n=a(s),l=r(4),i=a(l),o=r(5),u=a(o),d=r(7),c=a(d),f=r(6),p=a(f),m=r(2),h=a(m),b=r(9),v=r(14),_=a(v),g=function(e){function t(){return(0,i["default"])(this,t),(0,c["default"])(this,(0,n["default"])(t).apply(this,arguments))}return(0,p["default"])(t,e),(0,u["default"])(t,[{key:"render",value:function(){return h["default"].createElement("div",{className:"alert alert-danger "+_["default"]["err-msg"],role:"alert",name:this.props.name},h["default"].createElement(b.FormattedMessage,{id:"errorMsg.Error",defaultMessage:"{error}",values:{error:h["default"].createElement("strong",null,"Error: ")}}),h["default"].createElement(b.FormattedMessage,{id:this.props.msgId,defaultMessage:this.props.msgId}))}}]),t}(m.Component);g.propTypes={msgId:m.PropTypes.string.isRequired,name:m.PropTypes.string},t["default"]=g},14:function(e,t){e.exports={"err-msg":"ErrorMsgStyle__err-msg___WmKe1"}},22:function(e,t,r){"use strict";function a(e){return e&&e.__esModule?e:{"default":e}}Object.defineProperty(t,"__esModule",{value:!0});var s=r(3),n=a(s),l=r(4),i=a(l),o=r(5),u=a(o),d=r(7),c=a(d),f=r(6),p=a(f),m=r(2),h=a(m),b=r(9),v=r(18),_=function(e){function t(){return(0,i["default"])(this,t),(0,c["default"])(this,(0,n["default"])(t).apply(this,arguments))}return(0,p["default"])(t,e),(0,u["default"])(t,[{key:"render",value:function(){var e=this;return h["default"].createElement("div",{className:"row"},h["default"].createElement("div",{className:"col-xs-12 col-sm-12 col-md-12 col-lg-12"},h["default"].createElement("ol",{className:"breadcrumb"},function(){return e.props.routes.map(function(e,t){return e.disable?h["default"].createElement("li",{key:t,className:"active"},h["default"].createElement(b.FormattedMessage,{id:"nav."+e.msgId,defaultMessage:e.msgId})):h["default"].createElement("li",{key:t},h["default"].createElement(v.Link,{to:e.to},h["default"].createElement(b.FormattedMessage,{id:"nav."+e.msgId,defaultMessage:e.msgId})))})}())))}}]),t}(m.Component);_.propTypes={routes:m.PropTypes.array.isRequired},t["default"]=_},26:function(e,t,r){"use strict";function a(e){return e&&e.__esModule?e:{"default":e}}Object.defineProperty(t,"__esModule",{value:!0});var s=r(3),n=a(s),l=r(4),i=a(l),o=r(5),u=a(o),d=r(7),c=a(d),f=r(6),p=a(f),m=r(2),h=a(m);r(40);var b=function(e){function t(){return(0,i["default"])(this,t),(0,c["default"])(this,(0,n["default"])(t).apply(this,arguments))}return(0,p["default"])(t,e),(0,u["default"])(t,[{key:"title",value:function(e){return e.charAt(0).toUpperCase()+e.slice(1)}},{key:"render",value:function(){var e=this,t=this.props.browserIcon;return"phantomjs"===this.props.browserName.toLowerCase()?t="snapchat-ghost":"internet explorer"===this.props.browserName.toLowerCase()&&(t="internet-explorer"),h["default"].createElement("span",null," ",function(){return e.props.browserIcon?h["default"].createElement("i",{className:"fa fa-"+t,"aria-hidden":"true"}):null}(),h["default"].createElement("small",null,h["default"].createElement("b",null," ",this.title(this.props.browserName))),function(){return e.props.browserVersion?h["default"].createElement("i",null," ",e.props.browserVersion):null}(),function(){return e.props.platform?h["default"].createElement("small",null," - ",e.props.platform):null}())}}]),t}(m.Component);b.propTypes={browserName:m.PropTypes.string.isRequired,browserVersion:m.PropTypes.string,browserIcon:m.PropTypes.string,platform:m.PropTypes.string},t["default"]=b},47:function(e,t,r){"use strict";function a(e){return e&&e.__esModule?e:{"default":e}}Object.defineProperty(t,"__esModule",{value:!0});var s=r(3),n=a(s),l=r(4),i=a(l),o=r(5),u=a(o),d=r(7),c=a(d),f=r(6),p=a(f),m=r(2),h=a(m),b=r(11),v=a(b),_=function(e){function t(e){(0,i["default"])(this,t);var r=(0,c["default"])(this,(0,n["default"])(t).call(this,e));return r._initLogger(),r._bind("onFirstClick","onPreviousClick","onNextClick","onLastClick"),r}return(0,p["default"])(t,e),(0,u["default"])(t,[{key:"onFirstClick",value:function(){this.debug("onFirstClick"),this.props.fetchData(0)}},{key:"onPreviousClick",value:function(){this.debug("onPreviousClick");var e=this.props.skippedItem-this.props.itemPerPage;this.props.fetchData(e)}},{key:"onNextClick",value:function(){this.debug("onNextClick");var e=this.props.skippedItem+this.props.itemPerPage;this.props.fetchData(e)}},{key:"onLastClick",value:function(){this.debug("onLastClick");var e=void 0;e=this.props.totalItem%this.props.itemPerPage?this.props.totalItem-this.props.totalItem%this.props.itemPerPage:this.props.totalItem-this.props.itemPerPage,this.props.fetchData(e)}},{key:"render",value:function(){var e=!this.props.skippedItem,t=void 0,r=void 0;e?(t=h["default"].createElement("a",{className:"btn btn-default btn-link",disabled:!0},"<<"),r=h["default"].createElement("a",{className:"btn btn-default btn-link",disabled:!0},"<")):(t=h["default"].createElement("a",{onClick:this.onFirstClick,className:"btn btn-default btn-link"},"<<"),r=h["default"].createElement("a",{onClick:this.onPreviousClick,className:"btn btn-default btn-link"},"<"));var a=!this.props.totalItem||this.props.totalItem<=this.props.skippedItem+this.props.itemPerPage,s=void 0,n=void 0;return a?(s=h["default"].createElement("a",{className:"btn btn-default btn-link",disabled:!0},">"),n=h["default"].createElement("a",{className:"btn btn-default btn-link",disabled:!0},">>")):(s=h["default"].createElement("a",{onClick:this.onNextClick,className:"btn btn-default btn-link"},">"),n=h["default"].createElement("a",{onClick:this.onLastClick,className:"btn btn-default btn-link"},">>")),a&&e?null:h["default"].createElement("div",{name:"pager"},t,r,s,n)}}]),t}(v["default"]);_.propTypes={totalItem:m.PropTypes.number.isRequired,skippedItem:m.PropTypes.number.isRequired,fetchData:m.PropTypes.func.isRequired,itemPerPage:m.PropTypes.number.isRequired},t["default"]=_},318:function(e,t,r){"use strict";function a(e){return e&&e.__esModule?e:{"default":e}}function s(e,t,r){return function(a){c["default"].post("/api/crud",e).then(function(s){h.debug("/api/crud (data) (response)",e,s),a(s.data.success?n(s.data,t,r):l(s.data.error))})}}function n(e,t,r){return e.skip=t,e.limit=r,{type:p,data:e}}function l(e){return{type:m,error:e}}function i(){var e=arguments.length<=0||void 0===arguments[0]?b:arguments[0],t=arguments[1];switch(t.type){case f:return(0,u["default"])({},b,{loading:!0});case p:return(0,u["default"])({},b,{browserIdsList:t.data.results[0].browser_ids,totalBrowserIds:t.data.results[0].browser_ids.length,testBatch:t.data.results[0],loading:!1,limit:t.data.limit,skip:t.data.skip});case m:return(0,u["default"])({},b,{loading:!1,error:t.error});default:return e}}Object.defineProperty(t,"__esModule",{value:!0}),t.actions=t.LOADED_BROWSER_IDS_LIST_ERROR=t.LOADED_BROWSER_IDS_LIST_SUCCESS=t.LOADING_BROWSER_IDS_LIST=void 0;var o=r(19),u=a(o);t.doFetchBrowserIds=s,t["default"]=i;var d=r(24),c=a(d),f=t.LOADING_BROWSER_IDS_LIST="LOADING_BROWSER_IDS_LIST",p=t.LOADED_BROWSER_IDS_LIST_SUCCESS="LOADED_BROWSER_IDS_LIST_SUCCESS",m=t.LOADED_BROWSER_IDS_LIST_ERROR="LOADED_BROWSER_IDS_LIST_ERROR",h=r(25).getLogger("BrowserIdsList");h.setLevel("error");var b=(t.actions={doFetchBrowserIds:s},{error:null,broswerIds:null,testBatch:null,loading:!0,totalBrowserIds:0,skip:0,limit:0})},483:function(e,t,r){"use strict";function a(e){return e&&e.__esModule?e:{"default":e}}var s=r(63),n=a(s),l=r(3),i=a(l),o=r(4),u=a(o),d=r(5),c=a(d),f=r(7),p=a(f),m=r(6),h=a(m),b=r(2),v=a(b),_=r(18),g=r(22),I=a(g),k=r(26),E=a(k),y=r(12),w=a(y),P=r(47),S=a(P),L=r(31),R=a(L),B=r(11),N=a(B),C=10,T=function(e){function t(e){(0,u["default"])(this,t);var r=(0,p["default"])(this,(0,i["default"])(t).call(this,e));return r._initLogger(),r._bind("getPath","getTestBatchUid","getTestBatch","fetchBrowserIds"),r}return(0,h["default"])(t,e),(0,c["default"])(t,[{key:"componentWillMount",value:function(){this.debug("componentWillUnmount"),this.fetchBrowserIds(0)}},{key:"componentWillReceiveProps",value:function(){var e=this,t=this.getTestBatch();t&&(t.terminated?this._interval&&(clearInterval(this._interval),this._interval=null):this._interval=setTimeout(function(){e.fetchBrowserIds(0)},2e3))}},{key:"componentWillUnmount",value:function(){this.debug("componentWillUnmount"),clearInterval(this._interval)}},{key:"fetchBrowserIds",value:function(e){var t={token:this.props.state.session.token,actions:{action:"read",uid:this.getTestBatchUid(),skip:e,limit:C,model:"testbatch"}};this.props.actions.doFetchBrowserIds(t,e,C)}},{key:"getPath",value:function(){return this.props.location.query.path}},{key:"getTestBatchUid",value:function(){return this.props.location.query.testbatchuid}},{key:"getTestBatch",value:function(){return this.props.state.browseridslist.testBatch}},{key:"render",value:function(){var e=this,t=this.props.state.browseridslist,r=this.getPath();if(t.error)return v["default"].createElement(w["default"],{msgId:t.error});if(t.loading)return v["default"].createElement("div",{className:"container-fluid"},v["default"].createElement(R["default"],{style:{left:"50%"}}));var a=function(){var a=t.browserIdsList,s=e.getTestBatch(),n=[{msgId:"TestBatchDetail",to:"/testbatchdetail?testbatchuid="+s.uid},{msgId:"BrowserIdsList",disable:!0}];return{v:v["default"].createElement("div",null,v["default"].createElement(I["default"],{routes:n}),v["default"].createElement("h2",{className:"text-center"},"Browser Ids List ",v["default"].createElement("small",null," (",s.friendly_name,") (",s.uid,")")),v["default"].createElement("ul",null,function(){return a.map(function(e,t){return v["default"].createElement("li",{key:t},v["default"].createElement("small",null,v["default"].createElement(_.Link,{className:"btn btn-default btn-link",to:r+"?browserId="+e.id+"&browserName="+e.capabilities.browserName+"&browserIcon="+e.capabilities.browserName+"&browserVersion="+e.capabilities.version+"&platform="+e.capabilities.platform+"&testbatchuid="+s.uid},v["default"].createElement(E["default"],{browserName:e.capabilities.browserName,browserIcon:e.capabilities.browserName,browserVersion:e.capabilities.version,platform:e.capabilities.platform}))))})}()),v["default"].createElement(S["default"],{skippedItem:t.skip,fetchData:e.fetchBrowserIds,totalItem:t.totalBrowserIds,itemPerPage:C}))}}();return"object"===("undefined"==typeof a?"undefined":(0,n["default"])(a))?a.v:void 0}}]),t}(N["default"]);e.exports=T},484:function(e,t,r){"use strict";function a(e){return e&&e.__esModule?e:{"default":e}}function s(e){return{state:e}}function n(e){return{actions:(0,i.bindActionCreators)(o.actions,e)}}Object.defineProperty(t,"__esModule",{value:!0});var l=r(17),i=r(21),o=r(318),u=r(483),d=a(u);t["default"]=(0,l.connect)(s,n)(d["default"])}});
//# sourceMappingURL=14.4158d9d4dcfb80463ee5.chunk.js.map