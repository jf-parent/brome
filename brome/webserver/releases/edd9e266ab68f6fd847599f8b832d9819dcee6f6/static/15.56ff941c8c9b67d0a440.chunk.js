webpackJsonp([15],{13:function(e,t,a){"use strict";function r(e){return e&&e.__esModule?e:{"default":e}}Object.defineProperty(t,"__esModule",{value:!0});var n=a(3),l=r(n),s=a(4),u=r(s),o=a(5),i=r(o),d=a(7),c=r(d),f=a(6),p=r(f),m=a(2),g=r(m),h=a(9),b=a(15),v=r(b),_=function(e){function t(){return(0,u["default"])(this,t),(0,c["default"])(this,(0,l["default"])(t).apply(this,arguments))}return(0,p["default"])(t,e),(0,i["default"])(t,[{key:"render",value:function(){return g["default"].createElement("div",{className:"alert alert-danger "+v["default"]["err-msg"],role:"alert",name:this.props.name},g["default"].createElement(h.FormattedMessage,{id:"errorMsg.Error",defaultMessage:"{error}",values:{error:g["default"].createElement("strong",null,"Error: ")}}),g["default"].createElement(h.FormattedMessage,{id:this.props.msgId,defaultMessage:this.props.msgId}))}}]),t}(m.Component);_.propTypes={msgId:m.PropTypes.string.isRequired,name:m.PropTypes.string},t["default"]=_},15:function(e,t){e.exports={"err-msg":"ErrorMsgStyle__err-msg___WmKe1"}},25:function(e,t,a){"use strict";function r(e){return e&&e.__esModule?e:{"default":e}}Object.defineProperty(t,"__esModule",{value:!0});var n=a(3),l=r(n),s=a(4),u=r(s),o=a(5),i=r(o),d=a(7),c=r(d),f=a(6),p=r(f),m=a(2),g=r(m),h=a(9),b=a(19),v=function(e){function t(){return(0,u["default"])(this,t),(0,c["default"])(this,(0,l["default"])(t).apply(this,arguments))}return(0,p["default"])(t,e),(0,i["default"])(t,[{key:"render",value:function(){var e=this;return g["default"].createElement("div",{className:"row"},g["default"].createElement("div",{className:"col-xs-12 col-sm-12 col-md-12 col-lg-12"},g["default"].createElement("ol",{className:"breadcrumb"},function(){return e.props.routes.map(function(e,t){return e.disable?g["default"].createElement("li",{key:t,className:"active"},g["default"].createElement(h.FormattedMessage,{id:"nav."+e.msgId,defaultMessage:e.msgId})):g["default"].createElement("li",{key:t},g["default"].createElement(b.Link,{to:e.to},g["default"].createElement(h.FormattedMessage,{id:"nav."+e.msgId,defaultMessage:e.msgId})))})}())))}}]),t}(m.Component);v.propTypes={routes:m.PropTypes.array.isRequired},t["default"]=v},30:function(e,t,a){"use strict";function r(e){return e&&e.__esModule?e:{"default":e}}Object.defineProperty(t,"__esModule",{value:!0});var n=a(3),l=r(n),s=a(4),u=r(s),o=a(5),i=r(o),d=a(7),c=r(d),f=a(6),p=r(f),m=a(2),g=r(m);a(44);var h=function(e){function t(){return(0,u["default"])(this,t),(0,c["default"])(this,(0,l["default"])(t).apply(this,arguments))}return(0,p["default"])(t,e),(0,i["default"])(t,[{key:"title",value:function(e){return e.charAt(0).toUpperCase()+e.slice(1)}},{key:"render",value:function(){var e=this,t=this.props.browserIcon;return"phantomjs"===this.props.browserName.toLowerCase()?t="snapchat-ghost":"internet explorer"===this.props.browserName.toLowerCase()&&(t="internet-explorer"),g["default"].createElement("span",null," ",function(){return e.props.browserIcon?g["default"].createElement("i",{className:"fa fa-"+t,"aria-hidden":"true"}):null}(),g["default"].createElement("small",null,g["default"].createElement("b",null," ",this.title(this.props.browserName))),function(){return e.props.browserVersion?g["default"].createElement("i",null," ",e.props.browserVersion):null}(),function(){return e.props.platform?g["default"].createElement("small",null," - ",e.props.platform):null}())}}]),t}(m.Component);h.propTypes={browserName:m.PropTypes.string.isRequired,browserVersion:m.PropTypes.string,browserIcon:m.PropTypes.string,platform:m.PropTypes.string},t["default"]=h},469:function(e,t,a){"use strict";function r(e){return e&&e.__esModule?e:{"default":e}}var n=a(79),l=r(n),s=a(3),u=r(s),o=a(4),i=r(o),d=a(5),c=r(d),f=a(7),p=r(f),m=a(6),g=r(m),h=a(2),b=r(h),v=a(22),_=r(v),E=a(25),y=r(E),w=a(30),I=r(w),M=a(34),T=r(M),k=a(13),N=r(k),L=a(11),P=r(L),x=function(e){function t(e){(0,i["default"])(this,t);var a=(0,p["default"])(this,(0,u["default"])(t).call(this,e));return a._initLogger(),a._bind("fetchTestInstanceLog"),a.state={lines:[],loading:!0,error:null,parent:null,name:null},a}return(0,g["default"])(t,e),(0,c["default"])(t,[{key:"fetchTestInstanceLog",value:function(e,t){var a=this,r={model:"testinstance",uid:e,skip:t};_["default"].post("/api/logstreamout",r).then(function(t){a.debug("/api/logstreamout (data) (response)",r,t),t.data.success?(a.setState({lines:a.state.lines.concat(t.data.results),loading:!1,parent:t.data.parent,name:t.data.name}),t.data.parent.terminated||(a._interval=setTimeout(function(){a.fetchTestInstanceLog(e,t.data.total)},2e3))):a.setState({loading:!1,error:t.data.error})})}},{key:"componentWillMount",value:function(){var e=this,t=this.props.location.query.testinstanceuid;setTimeout(function(){e.fetchTestInstanceLog(t,0)})}},{key:"componentWillUnmount",value:function(){this.debug("componentWillUnmount"),clearInterval(this._interval)}},{key:"render",value:function(){var e=this;if(this.state.loading)return b["default"].createElement("div",{className:"container-fluid"},b["default"].createElement(T["default"],{style:{left:"50%"}}));if(this.state.error)return b["default"].createElement(N["default"],{msgId:this.state.error});var t=function(){var t=e.state.lines,a={border:"2px solid black",padding:"4px",margin:"4px",overflow:"scroll"},r=[{msgId:"TestBatchDetail",to:"/testbatchdetail?testbatchuid="+e.state.parent.test_batch_id},{msgId:"TestInstanceList",to:"testinstancelist?path=testinstancelog&testbatchuid="+e.state.parent.test_batch_id},{msgId:"TestInstanceLog",disable:!0}],n=b["default"].createElement(I["default"],{browserName:e.state.parent.browser_capabilities.browserName,browserIcon:e.state.parent.browser_capabilities.browserName,browserVersion:e.state.parent.browser_capabilities.version,platform:e.state.parent.browser_capabilities.platform});return{v:b["default"].createElement("div",null,b["default"].createElement(y["default"],{routes:r}),b["default"].createElement("h2",null,"Test Batch Log ",b["default"].createElement("small",null,"(",e.state.parent.name," - ",n,") (",e.state.parent.test_batch_id,")")),b["default"].createElement("span",null,"Log:"," "),b["default"].createElement("b",null,e.state.name),b["default"].createElement("div",{style:a},b["default"].createElement("ol",null,function(){return t.map(function(e,t){return b["default"].createElement("li",{key:t},b["default"].createElement("small",null,b["default"].createElement("i",null,e)))})}())))}}();return"object"===("undefined"==typeof t?"undefined":(0,l["default"])(t))?t.v:void 0}}]),t}(P["default"]);e.exports=x},470:function(e,t,a){"use strict";function r(e){return e&&e.__esModule?e:{"default":e}}function n(e){return{state:e}}Object.defineProperty(t,"__esModule",{value:!0});var l=a(17),s=a(469),u=r(s);t["default"]=(0,l.connect)(n)(u["default"])}});
//# sourceMappingURL=15.56ff941c8c9b67d0a440.chunk.js.map