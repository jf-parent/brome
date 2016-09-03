webpackJsonp([11],{12:function(t,e,a){"use strict";function s(t){return t&&t.__esModule?t:{"default":t}}Object.defineProperty(e,"__esModule",{value:!0});var n=a(3),l=s(n),d=a(4),i=s(d),r=a(5),o=s(r),u=a(7),c=s(u),p=a(6),f=s(p),h=a(1),m=s(h),g=a(9),b=a(14),T=s(b),y=function(t){function e(){return(0,i["default"])(this,e),(0,c["default"])(this,(0,l["default"])(e).apply(this,arguments))}return(0,f["default"])(e,t),(0,o["default"])(e,[{key:"render",value:function(){return m["default"].createElement("div",{className:"alert alert-danger "+T["default"]["err-msg"],role:"alert",name:this.props.name},m["default"].createElement(g.FormattedMessage,{id:"errorMsg.Error",defaultMessage:"{error}",values:{error:m["default"].createElement("strong",null,"Error: ")}}),m["default"].createElement(g.FormattedMessage,{id:this.props.msgId,defaultMessage:this.props.msgId}))}}]),e}(h.Component);y.propTypes={msgId:h.PropTypes.string.isRequired,name:h.PropTypes.string},e["default"]=y},14:function(t,e){t.exports={"err-msg":"ErrorMsgStyle__err-msg___WmKe1"}},46:function(t,e,a){"use strict";function s(t){return t&&t.__esModule?t:{"default":t}}var n=a(39),l=s(n),d=a(3),i=s(d),r=a(4),o=s(r),u=a(5),c=s(u),p=a(7),f=s(p),h=a(6),m=s(h),g=a(1),b=s(g),T=a(52),y=s(T);a(57);var E=function(t){function e(t){(0,o["default"])(this,e);var a=(0,f["default"])(this,(0,i["default"])(e).call(this,t));return a.state={isDisabled:t.isDisabled,isLoading:t.isLoading},a}return(0,m["default"])(e,t),(0,c["default"])(e,[{key:"render",value:function(){var t=this.props.btnClass;return t+=this.state.isDisabled?" btn-danger":" btn-success",b["default"].createElement("center",null,b["default"].createElement(y["default"],(0,l["default"])({disabled:this.state.isDisabled,className:t,onClick:this.props.onSubmit,loading:this.props.isLoading,buttonStyle:"zoom-out"},this.props),this.props.children))}}]),e}(g.Component);E.propTypes={isDisabled:g.PropTypes.bool.isRequired,isLoading:g.PropTypes.bool.isRequired,onSubmit:g.PropTypes.func.isRequired,btnClass:g.PropTypes.string,children:g.PropTypes.any},E.defaultProps={btnClass:"btn btn-lg btn-primary btn-block"},t.exports=E},48:function(t,e,a){e=t.exports=a(8)(),e.push([t.id,"/*!\n * Ladda\n * http://lab.hakim.se/ladda\n * MIT licensed\n *\n * Copyright (C) 2016 Hakim El Hattab, http://hakim.se\n */.ladda-button{position:relative}.ladda-button .ladda-spinner{position:absolute;z-index:2;display:inline-block;width:32px;height:32px;top:50%;margin-top:0;opacity:0;pointer-events:none}.ladda-button .ladda-label{position:relative;z-index:3}.ladda-button .ladda-progress{position:absolute;width:0;height:100%;left:0;top:0;background:rgba(0,0,0,.2);visibility:hidden;opacity:0;-webkit-transition:all .1s linear!important;transition:all .1s linear!important}.ladda-button[data-loading] .ladda-progress{opacity:1;visibility:visible}.ladda-button,.ladda-button .ladda-label,.ladda-button .ladda-spinner{-webkit-transition:all .3s cubic-bezier(.175,.885,.32,1.275)!important;transition:all .3s cubic-bezier(.175,.885,.32,1.275)!important}.ladda-button[data-style=zoom-in],.ladda-button[data-style=zoom-in] .ladda-label,.ladda-button[data-style=zoom-in] .ladda-spinner,.ladda-button[data-style=zoom-out],.ladda-button[data-style=zoom-out] .ladda-label,.ladda-button[data-style=zoom-out] .ladda-spinner{-webkit-transition:all .3s ease!important;transition:all .3s ease!important}.ladda-button[data-style=expand-right] .ladda-spinner{right:-6px}.ladda-button[data-style=expand-right][data-size=s] .ladda-spinner,.ladda-button[data-style=expand-right][data-size=xs] .ladda-spinner{right:-12px}.ladda-button[data-style=expand-right][data-loading]{padding-right:56px}.ladda-button[data-style=expand-right][data-loading] .ladda-spinner{opacity:1}.ladda-button[data-style=expand-right][data-loading][data-size=s],.ladda-button[data-style=expand-right][data-loading][data-size=xs]{padding-right:40px}.ladda-button[data-style=expand-left] .ladda-spinner{left:26px}.ladda-button[data-style=expand-left][data-size=s] .ladda-spinner,.ladda-button[data-style=expand-left][data-size=xs] .ladda-spinner{left:4px}.ladda-button[data-style=expand-left][data-loading]{padding-left:56px}.ladda-button[data-style=expand-left][data-loading] .ladda-spinner{opacity:1}.ladda-button[data-style=expand-left][data-loading][data-size=s],.ladda-button[data-style=expand-left][data-loading][data-size=xs]{padding-left:40px}.ladda-button[data-style=expand-up]{overflow:hidden}.ladda-button[data-style=expand-up] .ladda-spinner{top:-32px;left:50%;margin-left:0}.ladda-button[data-style=expand-up][data-loading]{padding-top:54px}.ladda-button[data-style=expand-up][data-loading] .ladda-spinner{opacity:1;top:26px;margin-top:0}.ladda-button[data-style=expand-up][data-loading][data-size=s],.ladda-button[data-style=expand-up][data-loading][data-size=xs]{padding-top:32px}.ladda-button[data-style=expand-up][data-loading][data-size=s] .ladda-spinner,.ladda-button[data-style=expand-up][data-loading][data-size=xs] .ladda-spinner{top:4px}.ladda-button[data-style=expand-down]{overflow:hidden}.ladda-button[data-style=expand-down] .ladda-spinner{top:62px;left:50%;margin-left:0}.ladda-button[data-style=expand-down][data-size=s] .ladda-spinner,.ladda-button[data-style=expand-down][data-size=xs] .ladda-spinner{top:40px}.ladda-button[data-style=expand-down][data-loading]{padding-bottom:54px}.ladda-button[data-style=expand-down][data-loading] .ladda-spinner{opacity:1}.ladda-button[data-style=expand-down][data-loading][data-size=s],.ladda-button[data-style=expand-down][data-loading][data-size=xs]{padding-bottom:32px}.ladda-button[data-style=slide-left]{overflow:hidden}.ladda-button[data-style=slide-left] .ladda-label{position:relative}.ladda-button[data-style=slide-left] .ladda-spinner{left:100%;margin-left:0}.ladda-button[data-style=slide-left][data-loading] .ladda-label{opacity:0;left:-100%}.ladda-button[data-style=slide-left][data-loading] .ladda-spinner{opacity:1;left:50%}.ladda-button[data-style=slide-right]{overflow:hidden}.ladda-button[data-style=slide-right] .ladda-label{position:relative}.ladda-button[data-style=slide-right] .ladda-spinner{right:100%;margin-left:0;left:16px}.ladda-button[data-style=slide-right][data-loading] .ladda-label{opacity:0;left:100%}.ladda-button[data-style=slide-right][data-loading] .ladda-spinner{opacity:1;left:50%}.ladda-button[data-style=slide-up]{overflow:hidden}.ladda-button[data-style=slide-up] .ladda-label{position:relative}.ladda-button[data-style=slide-up] .ladda-spinner{left:50%;margin-left:0;margin-top:1em}.ladda-button[data-style=slide-up][data-loading] .ladda-label{opacity:0;top:-1em}.ladda-button[data-style=slide-up][data-loading] .ladda-spinner{opacity:1;margin-top:0}.ladda-button[data-style=slide-down]{overflow:hidden}.ladda-button[data-style=slide-down] .ladda-label{position:relative}.ladda-button[data-style=slide-down] .ladda-spinner{left:50%;margin-left:0;margin-top:-2em}.ladda-button[data-style=slide-down][data-loading] .ladda-label{opacity:0;top:1em}.ladda-button[data-style=slide-down][data-loading] .ladda-spinner{opacity:1;margin-top:0}.ladda-button[data-style=zoom-out]{overflow:hidden}.ladda-button[data-style=zoom-out] .ladda-spinner{left:50%;margin-left:32px;-webkit-transform:scale(2.5);transform:scale(2.5)}.ladda-button[data-style=zoom-out] .ladda-label{position:relative;display:inline-block}.ladda-button[data-style=zoom-out][data-loading] .ladda-label{opacity:0;-webkit-transform:scale(.5);transform:scale(.5)}.ladda-button[data-style=zoom-out][data-loading] .ladda-spinner{opacity:1;margin-left:0;-webkit-transform:none;transform:none}.ladda-button[data-style=zoom-in]{overflow:hidden}.ladda-button[data-style=zoom-in] .ladda-spinner{left:50%;margin-left:-16px;-webkit-transform:scale(.2);transform:scale(.2)}.ladda-button[data-style=zoom-in] .ladda-label{position:relative;display:inline-block}.ladda-button[data-style=zoom-in][data-loading] .ladda-label{opacity:0;-webkit-transform:scale(2.2);transform:scale(2.2)}.ladda-button[data-style=zoom-in][data-loading] .ladda-spinner{opacity:1;margin-left:0;-webkit-transform:none;transform:none}.ladda-button[data-style=contract]{overflow:hidden;width:100px}.ladda-button[data-style=contract] .ladda-spinner{left:50%;margin-left:0}.ladda-button[data-style=contract][data-loading]{border-radius:50%;width:52px}.ladda-button[data-style=contract][data-loading] .ladda-label{opacity:0}.ladda-button[data-style=contract][data-loading] .ladda-spinner{opacity:1}.ladda-button[data-style=contract-overlay]{overflow:hidden;width:100px;box-shadow:0 0 0 2000px transparent}.ladda-button[data-style=contract-overlay] .ladda-spinner{left:50%;margin-left:0}.ladda-button[data-style=contract-overlay][data-loading]{border-radius:50%;width:52px;box-shadow:0 0 0 2000px rgba(0,0,0,.8)}.ladda-button[data-style=contract-overlay][data-loading] .ladda-label{opacity:0}.ladda-button[data-style=contract-overlay][data-loading] .ladda-spinner{opacity:1}",""])},51:function(t,e,a){t.exports=a(55)},52:function(t,e,a){var s=a(1),n=a(42).findDOMNode,l=a(51),d={buttonStyle:"data-style",buttonColor:"data-color",buttonSize:"data-size",spinnerSize:"data-spinner-size",spinnerColor:"data-spinner-color"},i=s.createClass({displayName:"LaddaButton",mixins:[l],propTypes:{loading:s.PropTypes.bool,progress:s.PropTypes.number,buttonStyle:s.PropTypes.string,buttonColor:s.PropTypes.string,buttonSize:s.PropTypes.string,spinnerSize:s.PropTypes.number,spinnerColor:s.PropTypes.string},getDefaultProps:function(){return{loading:!1,buttonStyle:"expand-left"}},componentDidMount:function(){this.laddaButton=a(53).create(n(this))},componentWillUnmount:function(){this.laddaButton.remove&&this.laddaButton.remove()},componentWillReceiveProps:function(t){this.laddaButton&&(!t.loading&&t.disabled&&(this.laddaButton.stop(),this.laddaButton.disable()),t.loading&&!this.laddaButton.isLoading()?this.laddaButton.start():!t.loading&&this.laddaButton.isLoading()&&this.laddaButton.stop(),"undefined"!=typeof t.progress&&this.laddaButton.setProgress(t.progress))},render:function(){var t={};for(var e in this.props)t[d[e]||e]=this.props[e];return t.className="ladda-button "+(t.className||""),s.DOM.button(t,s.DOM.span({className:"ladda-label"},this.props.children),s.DOM.span({className:"ladda-spinner"}))}});t.exports=i},53:function(t,e,a){/*!
	 * Ladda 0.9.8 (2015-03-19, 17:22)
	 * http://lab.hakim.se/ladda
	 * MIT licensed
	 *
	 * Copyright (C) 2015 Hakim El Hattab, http://hakim.se
	 */
!function(e,s){t.exports=s(a(54))}(this,function(t){"use strict";function e(t){if(void 0===t)return void console.warn("Ladda button target must be defined.");t.querySelector(".ladda-label")||(t.innerHTML='<span class="ladda-label">'+t.innerHTML+"</span>");var e,a=t.querySelector(".ladda-spinner");a||(a=document.createElement("span"),a.className="ladda-spinner"),t.appendChild(a);var s,n={start:function(){return e||(e=d(t)),t.setAttribute("disabled",""),t.setAttribute("data-loading",""),clearTimeout(s),e.spin(a),this.setProgress(0),this},startAfter:function(t){return clearTimeout(s),s=setTimeout(function(){n.start()},t),this},stop:function(){return t.removeAttribute("disabled"),t.removeAttribute("data-loading"),clearTimeout(s),e&&(s=setTimeout(function(){e.stop()},1e3)),this},toggle:function(){return this.isLoading()?this.stop():this.start(),this},setProgress:function(e){e=Math.max(Math.min(e,1),0);var a=t.querySelector(".ladda-progress");0===e&&a&&a.parentNode?a.parentNode.removeChild(a):(a||(a=document.createElement("div"),a.className="ladda-progress",t.appendChild(a)),a.style.width=(e||0)*t.offsetWidth+"px")},enable:function(){return this.stop(),this},disable:function(){return this.stop(),t.setAttribute("disabled",""),this},isLoading:function(){return t.hasAttribute("data-loading")},remove:function(){clearTimeout(s),t.removeAttribute("disabled",""),t.removeAttribute("data-loading",""),e&&(e.stop(),e=null);for(var a=0,l=r.length;l>a;a++)if(n===r[a]){r.splice(a,1);break}}};return r.push(n),n}function a(t,e){for(;t.parentNode&&t.tagName!==e;)t=t.parentNode;return e===t.tagName?t:void 0}function s(t){for(var e=["input","textarea","select"],a=[],s=0;e.length>s;s++)for(var n=t.getElementsByTagName(e[s]),l=0;n.length>l;l++)n[l].hasAttribute("required")&&a.push(n[l]);return a}function n(t,n){n=n||{};var l=[];"string"==typeof t?l=i(document.querySelectorAll(t)):"object"==typeof t&&"string"==typeof t.nodeName&&(l=[t]);for(var d=0,r=l.length;r>d;d++)(function(){var t=l[d];if("function"==typeof t.addEventListener){var i=e(t),r=-1;t.addEventListener("click",function(){var e=!0,l=a(t,"FORM");if(void 0!==l)for(var d=s(l),o=0;d.length>o;o++)""===d[o].value.replace(/^\s+|\s+$/g,"")&&(e=!1),"checkbox"!==d[o].type&&"radio"!==d[o].type||d[o].checked||(e=!1),"email"===d[o].type&&(e=/^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/.test(d[o].value));e&&(i.startAfter(1),"number"==typeof n.timeout&&(clearTimeout(r),r=setTimeout(i.stop,n.timeout)),"function"==typeof n.callback&&n.callback.apply(null,[i]))},!1)}})()}function l(){for(var t=0,e=r.length;e>t;t++)r[t].stop()}function d(e){var a,s=e.offsetHeight;0===s&&(s=parseFloat(window.getComputedStyle(e).height)),s>32&&(s*=.8),e.hasAttribute("data-spinner-size")&&(s=parseInt(e.getAttribute("data-spinner-size"),10)),e.hasAttribute("data-spinner-color")&&(a=e.getAttribute("data-spinner-color"));var n=12,l=.2*s,d=.6*l,i=7>l?2:3;return new t({color:a||"#fff",lines:n,radius:l,length:d,width:i,zIndex:"auto",top:"auto",left:"auto",className:""})}function i(t){for(var e=[],a=0;t.length>a;a++)e.push(t[a]);return e}var r=[];return{bind:n,create:e,stopAll:l}})},54:function(t,e,a){!function(e,a){t.exports=a()}(this,function(){"use strict";function t(t,e){var a,s=document.createElement(t||"div");for(a in e)s[a]=e[a];return s}function e(t){for(var e=1,a=arguments.length;e<a;e++)t.appendChild(arguments[e]);return t}function a(t,e,a,s){var n=["opacity",e,~~(100*t),a,s].join("-"),l=.01+a/s*100,d=Math.max(1-(1-t)/e*(100-l),t),i=o.substring(0,o.indexOf("Animation")).toLowerCase(),r=i&&"-"+i+"-"||"";return c[n]||(p.insertRule("@"+r+"keyframes "+n+"{0%{opacity:"+d+"}"+l+"%{opacity:"+t+"}"+(l+.01)+"%{opacity:1}"+(l+e)%100+"%{opacity:"+t+"}100%{opacity:"+d+"}}",p.cssRules.length),c[n]=1),n}function s(t,e){var a,s,n=t.style;for(e=e.charAt(0).toUpperCase()+e.slice(1),s=0;s<u.length;s++)if(a=u[s]+e,void 0!==n[a])return a;if(void 0!==n[e])return e}function n(t,e){for(var a in e)t.style[s(t,a)||a]=e[a];return t}function l(t){for(var e=1;e<arguments.length;e++){var a=arguments[e];for(var s in a)void 0===t[s]&&(t[s]=a[s])}return t}function d(t,e){return"string"==typeof t?t:t[e%t.length]}function i(t){this.opts=l(t||{},i.defaults,f)}function r(){function a(e,a){return t("<"+e+' xmlns="urn:schemas-microsoft.com:vml" class="spin-vml">',a)}p.addRule(".spin-vml","behavior:url(#default#VML)"),i.prototype.lines=function(t,s){function l(){return n(a("group",{coordsize:u+" "+u,coordorigin:-o+" "+-o}),{width:u,height:u})}function i(t,i,r){e(p,e(n(l(),{rotation:360/s.lines*t+"deg",left:~~i}),e(n(a("roundrect",{arcsize:s.corners}),{width:o,height:s.width,left:s.radius,top:-s.width>>1,filter:r}),a("fill",{color:d(s.color,t),opacity:s.opacity}),a("stroke",{opacity:0}))))}var r,o=s.length+s.width,u=2*o,c=2*-(s.width+s.length)+"px",p=n(l(),{position:"absolute",top:c,left:c});if(s.shadow)for(r=1;r<=s.lines;r++)i(r,-2,"progid:DXImageTransform.Microsoft.Blur(pixelradius=2,makeshadow=1,shadowopacity=.3)");for(r=1;r<=s.lines;r++)i(r);return e(t,p)},i.prototype.opacity=function(t,e,a,s){var n=t.firstChild;s=s.shadow&&s.lines||0,n&&e+s<n.childNodes.length&&(n=n.childNodes[e+s],n=n&&n.firstChild,n=n&&n.firstChild,n&&(n.opacity=a))}}var o,u=["webkit","Moz","ms","O"],c={},p=function(){var a=t("style",{type:"text/css"});return e(document.getElementsByTagName("head")[0],a),a.sheet||a.styleSheet}(),f={lines:12,length:7,width:5,radius:10,rotate:0,corners:1,color:"#000",direction:1,speed:1,trail:100,opacity:.25,fps:20,zIndex:2e9,className:"spinner",top:"50%",left:"50%",position:"absolute"};i.defaults={},l(i.prototype,{spin:function(e){this.stop();var a=this,s=a.opts,l=a.el=n(t(0,{className:s.className}),{position:s.position,width:0,zIndex:s.zIndex});s.radius+s.length+s.width;if(n(l,{left:s.left,top:s.top}),e&&e.insertBefore(l,e.firstChild||null),l.setAttribute("role","progressbar"),a.lines(l,a.opts),!o){var d,i=0,r=(s.lines-1)*(1-s.direction)/2,u=s.fps,c=u/s.speed,p=(1-s.opacity)/(c*s.trail/100),f=c/s.lines;!function h(){i++;for(var t=0;t<s.lines;t++)d=Math.max(1-(i+(s.lines-t)*f)%c*p,s.opacity),a.opacity(l,t*s.direction+r,d,s);a.timeout=a.el&&setTimeout(h,~~(1e3/u))}()}return a},stop:function(){var t=this.el;return t&&(clearTimeout(this.timeout),t.parentNode&&t.parentNode.removeChild(t),this.el=void 0),this},lines:function(s,l){function i(e,a){return n(t(),{position:"absolute",width:l.length+l.width+"px",height:l.width+"px",background:e,boxShadow:a,transformOrigin:"left",transform:"rotate("+~~(360/l.lines*u+l.rotate)+"deg) translate("+l.radius+"px,0)",borderRadius:(l.corners*l.width>>1)+"px"})}for(var r,u=0,c=(l.lines-1)*(1-l.direction)/2;u<l.lines;u++)r=n(t(),{position:"absolute",top:1+~(l.width/2)+"px",transform:l.hwaccel?"translate3d(0,0,0)":"",opacity:l.opacity,animation:o&&a(l.opacity,l.trail,c+u*l.direction,l.lines)+" "+1/l.speed+"s linear infinite"}),l.shadow&&e(r,n(i("#000","0 0 4px #000"),{top:"2px"})),e(s,e(r,i(d(l.color,u),"0 0 1px rgba(0,0,0,.1)")));return s},opacity:function(t,e,a){e<t.childNodes.length&&(t.childNodes[e].style.opacity=a)}});var h=n(t("group"),{behavior:"url(#default#VML)"});return!s(h,"transform")&&h.adj?r():o=s(h,"animation"),i})},55:function(t,e,a){"use strict";var s=a(56),n={shouldComponentUpdate:function(t,e){return s(this,t,e)}};t.exports=n},56:function(t,e,a){"use strict";function s(t,e,a){return!n(t.props,e)||!n(t.state,a)}var n=a(83);t.exports=s},57:function(t,e,a){var s=a(48);"string"==typeof s&&(s=[[t.id,s,""]]);a(23)(s,{});s.locals&&(t.exports=s.locals)},156:function(t,e,a){"use strict";function s(t){return t&&t.__esModule?t:{"default":t}}Object.defineProperty(e,"__esModule",{value:!0});var n=a(3),l=s(n),d=a(4),i=s(d),r=a(5),o=s(r),u=a(7),c=s(u),p=a(6),f=s(p),h=a(1),m=s(h),g=a(9),b=a(174),T=s(b),y=function(t){function e(){return(0,i["default"])(this,e),(0,c["default"])(this,(0,l["default"])(e).apply(this,arguments))}return(0,f["default"])(e,t),(0,o["default"])(e,[{key:"render",value:function(){return m["default"].createElement("div",{className:"alert alert-success "+T["default"]["success-msg"],role:"alert",name:this.props.name},m["default"].createElement(g.FormattedMessage,{id:this.props.msgId,defaultMessage:this.props.msgId}))}}]),e}(h.Component);y.propTypes={msgId:h.PropTypes.string.isRequired,name:h.PropTypes.string},e["default"]=y},174:function(t,e){t.exports={"success-msg":"SuccessMsgStyle__success-msg___1liPg"}},209:function(t,e,a){"use strict";function s(t){return t&&t.__esModule?t:{"default":t}}function n(){return function(t){t({type:m})}}function l(t){return function(e){e({type:y}),h["default"].post("/api/crud",t).then(function(a){x.debug("/api/crud (data) (response)",t,a),e(a.data.success?{type:E}:{type:v})})}}function d(t){return function(e){e({type:g}),h["default"].post("/api/crud",t).then(function(a){x.debug("/api/crud (data) (response)",t,a),e(a.data.success?{type:b}:{type:T})})}}function i(t,e){var a={token:t.token,actions:{action:"read",model:"testbatch",uid:e}};return function(t){h["default"].post("/api/crud",a).then(function(e){x.debug("/api/crud (data) (response)",a,e),t(e.data.success?r(e.data):o(e.data.error))})}}function r(t){return{type:_,data:t}}function o(t){return{type:B,error:t}}function u(){var t=arguments.length<=0||void 0===arguments[0]?k:arguments[0],e=arguments[1];switch(e.type){case _:var a=t.testBatch;return a[e.data.results[0].uid]=e.data.results[0],(0,p["default"])({},t,{testBatch:a});case B:return(0,p["default"])({},t,{error:e.error});case y:return(0,p["default"])({},t,{deletingTestBatch:!0});case E:return(0,p["default"])({},t,{deletingTestBatch:!1,deletedTestBatchSuccess:!0});case v:return(0,p["default"])({},t,{deletingTestBatch:!1,deletedTestBatchError:!0});case g:return(0,p["default"])({},t,{terminatingTestBatch:!0});case b:return(0,p["default"])({},t,{terminatingTestBatch:!1,terminatedTestBatchSuccess:!0});case T:return(0,p["default"])({},t,{terminatingTestBatch:!1,terminatedTestBatchError:!0});case m:return(0,p["default"])({},t,{terminatingTestBatch:!1,terminatedTestBatchSuccess:!1,terminatedTestBatchError:!1,deletingTestBatch:!1,deletedTestBatchSuccess:!1,deletedTestBatchError:!1});default:return t}}Object.defineProperty(e,"__esModule",{value:!0}),e.actions=e.LOADED_TEST_BATCH_DETAIL_ERROR=e.LOADED_TEST_BATCH_DETAIL_SUCCESS=e.DELETED_TEST_BATCH_ERROR=e.DELETED_TEST_BATCH_SUCCESS=e.DELETING_TEST_BATCH=e.TERMINATED_TEST_BATCH_ERROR=e.TERMINATED_TEST_BATCH_SUCCESS=e.TERMINATING_TEST_BATCH=e.RESET=void 0;var c=a(19),p=s(c);e.doReset=n,e.doDelete=l,e.doTerminate=d,e.doLoadTestBatchDetail=i,e["default"]=u;var f=a(24),h=s(f),m=e.RESET="RESET",g=e.TERMINATING_TEST_BATCH="TERMINATING_TEST_BATCH",b=e.TERMINATED_TEST_BATCH_SUCCESS="TERMINATED_TEST_BATCH_SUCCESS",T=e.TERMINATED_TEST_BATCH_ERROR="TERMINATED_TEST_BATCH_ERROR",y=e.DELETING_TEST_BATCH="DELETING_TEST_BATCH",E=e.DELETED_TEST_BATCH_SUCCESS="DELETED_TEST_BATCH_SUCCESS",v=e.DELETED_TEST_BATCH_ERROR="DELETED_TEST_BATCH_ERROR",_=e.LOADED_TEST_BATCH_DETAIL_SUCCESS="LOADED_TEST_BATCH_DETAIL_SUCCESS",B=e.LOADED_TEST_BATCH_DETAIL_ERROR="LOADED_TEST_BATCH_DETAIL_ERROR",x=a(25).getLogger("TestBatchDetail");x.setLevel("error");var k=(e.actions={doLoadTestBatchDetail:i,doTerminate:d,doDelete:l,doReset:n},{testBatch:{},deletingTestBatch:!1,deletedTestBatchSuccess:!1,deletedTestBatchError:!1,terminatingTestBatch:!1,terminatedTestBatchSuccess:!1,terminatedTestBatchError:!1,error:null})},449:function(t,e,a){"use strict";function s(t){return t&&t.__esModule?t:{"default":t}}var n=a(3),l=s(n),d=a(4),i=s(d),r=a(5),o=s(r),u=a(7),c=s(u),p=a(6),f=s(p),h=a(1),m=s(h),g=a(9),b=a(18);a(33);var T=a(621),y=a(2),E=s(y),v=a(46),_=s(v),B=a(12),x=s(B),k=a(156),D=s(k),C=a(31),M=s(C),S=a(553),N=s(S),w=a(132),A=s(w),L=a(11),R=s(L),z=function(t){function e(t){(0,i["default"])(this,e);var a=(0,c["default"])(this,(0,l["default"])(e).call(this,t));return a._initLogger(),a._bind("getTestBatchUid","getTestBatch","getRunningTime","fetchTestBatchDetail","getToolbelt","getTool","onDelete","onTerminate","getActionToolbelt","getProgress","getNotification","getTestResults","getCrashes","getMilestone"),a}return(0,f["default"])(e,t),(0,o["default"])(e,[{key:"componentWillMount",value:function(){this.fetchTestBatchDetail()}},{key:"componentWillReceiveProps",value:function(){var t=this.getTestBatch();t&&t.terminated&&this._interval&&(clearInterval(this._interval),this._interval=null)}},{key:"componentWillUnmount",value:function(){this.debug("componentWillUnmount"),clearInterval(this._interval),this.props.actions.doReset()}},{key:"onTerminate",value:function(){var t={token:this.props.state.session.token,actions:{action:"update",uid:this.getTestBatchUid(),model:"testbatch",data:{killed:!0}}};this.props.actions.doTerminate(t)}},{key:"onDelete",value:function(){var t={token:this.props.state.session.token,actions:{action:"delete",uid:this.getTestBatchUid(),model:"testbatch"}};this.props.actions.doDelete(t)}},{key:"getRunningTime",value:function(){function t(t){return(t<10?"0":"")+t}var e=this.getTestBatch(),a=(0,E["default"])(e.starting_timestamp),s=void 0;s=e.ending_timestamp?(0,E["default"])(e.ending_timestamp):Date.now();var n=E["default"].duration((0,E["default"])(s).diff(a)),l=parseInt(n.asHours()),d=parseInt(n.asMinutes())-60*l,i=parseInt(n.asSeconds())-60*l-60*d,r=t(l)+":"+t(d)+":"+t(i);return m["default"].createElement("div",{className:"row"},m["default"].createElement("center",null,m["default"].createElement("small",null,m["default"].createElement("b",null,m["default"].createElement(g.FormattedMessage,{id:"testBatchList.TotalDuration",defaultMessage:"Total duration:"}))," ",r)))}},{key:"getNotification",value:function(){var t=this.props.state.testbatchdetail;return t.terminatedTestBatchError?m["default"].createElement(x["default"],{msgId:"testBatchDetail.TerminatedTestBatchError"}):t.terminatedTestBatchSuccess&&!this.getTestBatch().terminated?m["default"].createElement(D["default"],{msgId:"testBatchDetail.TerminatedTestBatchSuccess"}):t.deletedTestBatchError?m["default"].createElement(x["default"],{msgId:"testBatchDetail.DeletedTestBatchError"}):t.deletedTestBatchSuccess?m["default"].createElement(D["default"],{msgId:"testBatchDetail.DeletedTestBatchSuccess"}):null}},{key:"getActionToolbelt",value:function(){var t=this.props.state.testbatchdetail;return t.testBatch[this.getTestBatchUid()].terminated?m["default"].createElement("div",{className:"row "+A["default"]["no-gutter"]},m["default"].createElement("div",{className:"pull-right"},m["default"].createElement(_["default"],{isLoading:t.deletingTestBatch,onClick:this.onDelete},m["default"].createElement("i",{className:"fa fa-trash-o","aria-hidden":"true"})," ",m["default"].createElement(g.FormattedMessage,{id:"testBatchDetail.Delete",defaultMessage:"Delete"})))):m["default"].createElement("div",{className:"row "+A["default"]["no-gutter"]},m["default"].createElement("div",{className:"pull-right"},m["default"].createElement(_["default"],{isLoading:t.terminatingTestBatch,onClick:this.onTerminate},m["default"].createElement("i",{className:"fa fa-plug","aria-hidden":"true"})," ",m["default"].createElement(g.FormattedMessage,{id:"testBatchDetail.Terminated",defaultMessage:"Terminate"}))))}},{key:"getProgress",value:function(){if(this.getTestBatch().terminated)return null;var t=this.getTestBatch(),e=t.total_tests,a=t.total_executing_tests,s=t.total_executed_tests,n=parseInt(s/e*100);return m["default"].createElement("center",null,m["default"].createElement("span",null,m["default"].createElement("small",null,m["default"].createElement(g.FormattedMessage,{id:"testBatchDetail.TotalTests",defaultMessage:"Total Tests:"})," ",m["default"].createElement("b",null,e)," ~ "," ")),m["default"].createElement("span",null,m["default"].createElement("small",null,m["default"].createElement(g.FormattedMessage,{id:"testBatchDetail.TotalExecutedTests",defaultMessage:"Total Executed Tests:"})," ",m["default"].createElement("b",null,s)," ~ "," ")),m["default"].createElement("span",null,m["default"].createElement("small",null,m["default"].createElement(g.FormattedMessage,{id:"testBatchDetail.TotalExecutingTests",defaultMessage:"Total Executing Tests:"})," ",m["default"].createElement("b",null,a))),m["default"].createElement(T.Line,{percent:n,strokeWidth:"2",strokeColor:"#87D0E8"}))}},{key:"getTestResults",value:function(){var t=this.getTestBatch().test_results,e=t.nb_failed_test,a=t.nb_succeeded_test,s=t.failed_tests;return m["default"].createElement("div",null,m["default"].createElement("h3",{className:N["default"]["section-header"]},m["default"].createElement(g.FormattedMessage,{id:"testBatchDetail.TestResults",defaultMessage:"Test Results"})," ",function(){return e?m["default"].createElement("span",{style:{color:"red"}},"(",e,")"):null}()," ",function(){return a?m["default"].createElement("span",{style:{color:"green"}},"(",a,")"):null}()),m["default"].createElement("ul",null,function(){return s.length?s.map(function(t,e){return m["default"].createElement("li",{key:e},m["default"].createElement("small",null,t.title))}):m["default"].createElement("li",null,m["default"].createElement("small",null,m["default"].createElement(g.FormattedMessage,{id:"testBatchDetail.NoTestFailed",defaultMessage:"No test failed"})))}()))}},{key:"getCrashes",value:function(){var t=this.getTestBatch().test_crashes,e=t.length||0,a={color:"green"};return e&&(a={color:"red"}),m["default"].createElement("div",null,m["default"].createElement("h3",{className:N["default"]["section-header"]},m["default"].createElement(g.FormattedMessage,{id:"testBatchDetail.Crashes",defaultMessage:"Crashes"})," ","(",m["default"].createElement("span",{style:a},e),"):"),m["default"].createElement("ul",null,function(){return t.length?t.map(function(t,e){return m["default"].createElement("li",{key:e},m["default"].createElement("small",null,t.title))}):m["default"].createElement("li",null,m["default"].createElement("small",null,m["default"].createElement(g.FormattedMessage,{id:"testBatchDetail.NoCrashes",defaultMessage:"No crashes"})))}()))}},{key:"getMilestone",value:function(){var t=this.getTestBatch().milestones;return m["default"].createElement("div",null,m["default"].createElement("h3",{className:N["default"]["section-header"]},m["default"].createElement(g.FormattedMessage,{id:"testBatchDetail.Milestone",defaultMessage:"Milestone:"})),m["default"].createElement("ul",null,function(){return t.length?t.map(function(t,e){return m["default"].createElement("li",{key:e},m["default"].createElement("small",null,m["default"].createElement(g.FormattedMessage,{id:"testBatchDetail."+t.msgId,defaultMessage:t.msgId,values:t.values})))}):m["default"].createElement("li",null,m["default"].createElement("small",null,m["default"].createElement(g.FormattedMessage,{id:"testBatchDetail.NoMilestone",defaultMessage:"No milestone"})))}()))}},{key:"getTool",value:function(t,e,a,s){var n=this,l=arguments.length<=4||void 0===arguments[4]?"":arguments[4],d="col-xs-12 col-sm-12 col-md-2 col-lg-2";return m["default"].createElement("div",{className:d},function(){return s?m["default"].createElement(b.Link,{className:"btn btn-default btn-link",to:t+"?testbatchuid="+n.getTestBatchUid()+l},m["default"].createElement("i",{className:"fa fa-"+a,"aria-hidden":"true"})," ",m["default"].createElement(g.FormattedMessage,{id:e.id,defaultMessage:e.defaultMessage,values:e.values})):m["default"].createElement("button",{className:"btn btn-default btn-link",disabled:!0},m["default"].createElement("i",{className:"fa fa-"+a,"aria-hidden":"true"})," ",m["default"].createElement(g.FormattedMessage,{id:e.id,defaultMessage:e.defaultMessage,values:e.values}))}())}},{key:"getToolbelt",value:function(){var t=this.getTestBatch(),e=t.features,a=this.getTool("testinstancelist",{id:"testBatchDetail.VideoCaptureLabel",defaultMessage:"Video Capture"},"video-camera",e.session_video_capture,"&path=testinstancevideo"),s=this.getTool("testinstancenetworkcapture",{id:"testBatchDetail.NetworkCaptureLabel",defaultMessage:"Network Capture"},"cubes",e.network_capture),n=this.getTool("testbatchtestresults",{id:"testBatchDetail.TestResultsLabel",defaultMessage:"Test Results ({nb_test_result})",values:{nb_test_result:t.test_results.nb_test_result.toString()}},"bar-chart",!!t.test_results.nb_test_result),l=this.getTool("testinstancedetaillist",{id:"testBatchDetail.TestInstanceDetailListLabel",defaultMessage:"Test Instances"},"list",!0),d=this.getTool("browseridslist",{id:"testBatchDetail.TestBatchScreenshots",defaultMessage:"Screenshots ({nb_screenshot})",values:{nb_screenshot:t.nb_screenshot.toString()}},"file-image-o",e.screenshots,"&path=testbatchscreenshots"),i=this.getTool("testbatchcrashes",{id:"testBatchDetail.TestInstanceCrashesLabel",defaultMessage:"Crash reports ({nb_crashes})",values:{nb_crashes:t.test_crashes.length.toString()}},"exclamation-triangle",!!t.test_crashes.length),r=this.getTool("testinstancelist",{id:"testBatchDetail.TestInstanceLogListLabel",defaultMessage:"Instances Logs"},"newspaper-o",!0,"&path=testinstancelog"),o=this.getTool("testbatchrunnerlog",{id:"testBatchDetail.TestRunnerLogLabel",defaultMessage:"Runner log"},"file-text-o",!0),u=this.getTool("testinstancelist",{id:"testBatchDetail.VncListLabel",defaultMessage:"Instance VNC"},"desktop",e.instance_vnc,"&path=testinstancevnc"),c=this.getTool("stylequality",{id:"testBatchDetail.StyleQualityLabel",defaultMessage:"Style Quality"},"eye",e.style_quality);return m["default"].createElement("div",{className:"row "+A["default"]["no-gutter"]},n,i,o,r,l,a,d,s,u,c)}},{key:"fetchTestBatchDetail",value:function(){var t=this;this._interval=setInterval(function(){t.props.actions.doLoadTestBatchDetail(t.props.state.session,t.getTestBatchUid())},2e3)}},{key:"getTestBatchUid",value:function(){return this.props.location.query.testbatchuid}},{key:"getTestBatch",value:function(){return this.props.state.testbatchdetail.testBatch[this.getTestBatchUid()]}},{key:"render",value:function(){var t=this.getTestBatch();return this.props.state.testbatchdetail.error?m["default"].createElement(x["default"],{msgId:this.props.state.testbatchdetail.error}):void 0===t?m["default"].createElement("div",{className:"container-fluid"},m["default"].createElement(M["default"],{style:{left:"50%"}})):this.props.state.testbatchdetail.deletedTestBatchSuccess?m["default"].createElement("div",{className:"container-fluid"},this.getNotification()):m["default"].createElement("div",{className:"container-fluid"},this.getActionToolbelt(),this.getNotification(),m["default"].createElement("h2",{className:"text-center"},m["default"].createElement(g.FormattedMessage,{id:"testBatchDetail.HeaderTitle",defaultMessage:"Test Batch Details"}),m["default"].createElement("small",null," (",t.friendly_name,") (",t.uid,")")),this.getRunningTime(),this.getProgress(),this.getToolbelt(),this.getTestResults(),this.getMilestone(),this.getCrashes())}}]),e}(R["default"]);t.exports=z},450:function(t,e,a){"use strict";function s(t){return t&&t.__esModule?t:{"default":t}}function n(t){return{state:t}}function l(t){return{actions:(0,i.bindActionCreators)(r.actions,t)}}Object.defineProperty(e,"__esModule",{value:!0});var d=a(17),i=a(21),r=a(209),o=a(449),u=s(o);e["default"]=(0,d.connect)(n,l)(u["default"])},553:function(t,e){t.exports={"feature-box":"ComponentStyle__feature-box___2nCxV","section-header":"ComponentStyle__section-header___3Di1B"}},620:function(t,e,a){"use strict";var s=a(16),n=a(1),l={strokeWidth:1,strokeColor:"#3FC7FA",trailWidth:1,trailColor:"#D9D9D9"},d=n.createClass({displayName:"Line",render:function(){var t=s({},this.props),e={strokeDasharray:"100px, 100px",strokeDashoffset:100-t.percent+"px",transition:"stroke-dashoffset 0.6s ease 0s, stroke 0.6s linear"};["strokeWidth","strokeColor","trailWidth","trailColor"].forEach(function(e){return"trailWidth"===e&&!t.trailWidth&&t.strokeWidth?void(t.trailWidth=t.strokeWidth):"strokeWidth"===e&&t.strokeWidth&&(!parseFloat(t.strokeWidth)||parseFloat(t.strokeWidth)>100||parseFloat(t.strokeWidth)<0)?void(t[e]=l[e]):void(t[e]||(t[e]=l[e]))});var a=t.strokeWidth,d=a/2,i=100-a/2,r="M "+d+","+d+" L "+i+","+d,o="0 0 100 "+a;return n.createElement("svg",{className:"rc-progress-line",viewBox:o,preserveAspectRatio:"none"},n.createElement("path",{className:"rc-progress-line-trail",d:r,strokeLinecap:"round",stroke:t.trailColor,strokeWidth:t.trailWidth,fillOpacity:"0"}),n.createElement("path",{className:"rc-progress-line-path",d:r,strokeLinecap:"round",stroke:t.strokeColor,strokeWidth:t.strokeWidth,fillOpacity:"0",style:e}))}}),i=n.createClass({displayName:"Circle",render:function(){var t=s({},this.props),e=t.strokeWidth,a=50-e/2,d="M 50,50 m 0,-"+a+"\n     a "+a+","+a+" 0 1 1 0,"+2*a+"\n     a "+a+","+a+" 0 1 1 0,-"+2*a,i=2*Math.PI*a,r={strokeDasharray:i+"px "+i+"px",strokeDashoffset:(100-t.percent)/100*i+"px",transition:"stroke-dashoffset 0.6s ease 0s, stroke 0.6s ease"};return["strokeWidth","strokeColor","trailWidth","trailColor"].forEach(function(e){return"trailWidth"===e&&!t.trailWidth&&t.strokeWidth?void(t.trailWidth=t.strokeWidth):void(t[e]||(t[e]=l[e]))}),n.createElement("svg",{className:"rc-progress-circle",viewBox:"0 0 100 100"},n.createElement("path",{className:"rc-progress-circle-trail",d:d,stroke:t.trailColor,strokeWidth:t.trailWidth,fillOpacity:"0"}),n.createElement("path",{className:"rc-progress-circle-path",d:d,strokeLinecap:"round",stroke:t.strokeColor,strokeWidth:t.strokeWidth,fillOpacity:"0",style:r}))}});t.exports={Line:d,Circle:i}},621:function(t,e,a){"use strict";t.exports=a(620)}});
//# sourceMappingURL=11.40d5304e931c4e6edd01.chunk.js.map