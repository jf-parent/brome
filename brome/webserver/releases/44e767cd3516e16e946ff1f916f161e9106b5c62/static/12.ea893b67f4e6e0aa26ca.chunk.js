webpackJsonp([12],{13:function(e,t,n){"use strict";function a(e){return e&&e.__esModule?e:{"default":e}}Object.defineProperty(t,"__esModule",{value:!0});var i=n(3),l=a(i),s=n(4),r=a(s),o=n(5),u=a(o),d=n(7),h=a(d),c=n(6),p=a(c),f=n(2),m=a(f),g=n(9),y=n(15),b=a(y),v=function(e){function t(){return(0,r["default"])(this,t),(0,h["default"])(this,(0,l["default"])(t).apply(this,arguments))}return(0,p["default"])(t,e),(0,u["default"])(t,[{key:"render",value:function(){return m["default"].createElement("div",{className:"alert alert-danger "+b["default"]["err-msg"],role:"alert",name:this.props.name},m["default"].createElement(g.FormattedMessage,{id:"errorMsg.Error",defaultMessage:"{error}",values:{error:m["default"].createElement("strong",null,"Error: ")}}),m["default"].createElement(g.FormattedMessage,{id:this.props.msgId,defaultMessage:this.props.msgId}))}}]),t}(f.Component);v.propTypes={msgId:f.PropTypes.string.isRequired,name:f.PropTypes.string},t["default"]=v},15:function(e,t){e.exports={"err-msg":"ErrorMsgStyle__err-msg___WmKe1"}},25:function(e,t,n){"use strict";function a(e){return e&&e.__esModule?e:{"default":e}}Object.defineProperty(t,"__esModule",{value:!0});var i=n(3),l=a(i),s=n(4),r=a(s),o=n(5),u=a(o),d=n(7),h=a(d),c=n(6),p=a(c),f=n(2),m=a(f),g=n(9),y=n(19),b=function(e){function t(){return(0,r["default"])(this,t),(0,h["default"])(this,(0,l["default"])(t).apply(this,arguments))}return(0,p["default"])(t,e),(0,u["default"])(t,[{key:"render",value:function(){var e=this;return m["default"].createElement("div",{className:"row"},m["default"].createElement("div",{className:"col-xs-12 col-sm-12 col-md-12 col-lg-12"},m["default"].createElement("ol",{className:"breadcrumb"},function(){return e.props.routes.map(function(e,t){return e.disable?m["default"].createElement("li",{key:t,className:"active"},m["default"].createElement(g.FormattedMessage,{id:"nav."+e.msgId,defaultMessage:e.msgId})):m["default"].createElement("li",{key:t},m["default"].createElement(y.Link,{to:e.to},m["default"].createElement(g.FormattedMessage,{id:"nav."+e.msgId,defaultMessage:e.msgId})))})}())))}}]),t}(f.Component);b.propTypes={routes:f.PropTypes.array.isRequired},t["default"]=b},30:function(e,t,n){"use strict";function a(e){return e&&e.__esModule?e:{"default":e}}Object.defineProperty(t,"__esModule",{value:!0});var i=n(3),l=a(i),s=n(4),r=a(s),o=n(5),u=a(o),d=n(7),h=a(d),c=n(6),p=a(c),f=n(2),m=a(f);n(44);var g=function(e){function t(){return(0,r["default"])(this,t),(0,h["default"])(this,(0,l["default"])(t).apply(this,arguments))}return(0,p["default"])(t,e),(0,u["default"])(t,[{key:"title",value:function(e){return e.charAt(0).toUpperCase()+e.slice(1)}},{key:"render",value:function(){var e=this,t=this.props.browserIcon;return"phantomjs"===this.props.browserName.toLowerCase()?t="snapchat-ghost":"internet explorer"===this.props.browserName.toLowerCase()&&(t="internet-explorer"),m["default"].createElement("span",null," ",function(){return e.props.browserIcon?m["default"].createElement("i",{className:"fa fa-"+t,"aria-hidden":"true"}):null}(),m["default"].createElement("small",null,m["default"].createElement("b",null," ",this.title(this.props.browserName))),function(){return e.props.browserVersion?m["default"].createElement("i",null," ",e.props.browserVersion):null}(),function(){return e.props.platform?m["default"].createElement("small",null," - ",e.props.platform):null}())}}]),t}(f.Component);g.propTypes={browserName:f.PropTypes.string.isRequired,browserVersion:f.PropTypes.string,browserIcon:f.PropTypes.string,platform:f.PropTypes.string},t["default"]=g},313:function(e,t,n){"use strict";function a(e){return e&&e.__esModule?e:{"default":e}}function i(e){return function(t){t({type:c}),h["default"].post("/api/crud",e).then(function(n){m.debug("/api/crud (data) (response)",e,n),t(n.data.success?l(n.data):s(n.data.results[0].error))})}}function l(e){return{type:p,data:e}}function s(e){return{type:f,error:e}}function r(){var e=arguments.length<=0||void 0===arguments[0]?g:arguments[0],t=arguments[1];switch(t.type){case c:return(0,u["default"])({},g,{loading:!0});case p:return(0,u["default"])({},g,{screenshots:t.data.results[0].results,testBatch:t.data.results[1].results[0],loading:!1});case f:return(0,u["default"])({},g,{loading:!1,error:t.error});default:return e}}Object.defineProperty(t,"__esModule",{value:!0}),t.actions=t.LOADED_TEST_BATCH_SCREENSHOTS_ERROR=t.LOADED_TEST_BATCH_SCREENSHOTS_SUCCESS=t.LOADING_TEST_BATCH_SCREENSHOTS=void 0;var o=n(18),u=a(o);t.doFetchScreenshots=i,t["default"]=r;var d=n(24),h=a(d),c=t.LOADING_TEST_BATCH_SCREENSHOTS="LOADING_TEST_BATCH_SCREENSHOTS",p=t.LOADED_TEST_BATCH_SCREENSHOTS_SUCCESS="LOADED_TEST_BATCH_SCREENSHOTS_SUCCESS",f=t.LOADED_TEST_BATCH_SCREENSHOTS_ERROR="LOADED_TEST_BATCH_SCREENSHOTS_ERROR",m=n(22).getLogger("TestBatchScreenshots");m.setLevel("error");var g=(t.actions={doFetchScreenshots:i},{screenshots:[],testBatch:null,error:null,loading:!0})},459:function(e,t,n){"use strict";function a(e){return e&&e.__esModule?e:{"default":e}}var i=n(62),l=a(i),s=n(490),r=a(s),o=n(3),u=a(o),d=n(4),h=a(d),c=n(5),p=a(c),f=n(7),m=a(f),g=n(6),y=a(g),b=n(2),v=a(b),w=n(618),T=a(w);n(724);var S=n(25),_=a(S),x=n(30),E=a(x),k=n(34),I=a(k),P=n(13),C=a(P),N=n(553),O=a(N),R=n(11),L=a(R),M=function(e){function t(e){(0,h["default"])(this,t);var n=(0,m["default"])(this,(0,u["default"])(t).call(this,e));return n._initLogger(),n._bind("getBrowserId","getBrowserIcon","getBrowserName","getBrowserVersion","getPlatform","fetchScreenshots","fullScreen","playSlider","pauseSlider","handleInputChange","handleCheckboxChange"),n.state={isPlaying:!1,infinite:!0,showIndex:!0,slideOnThumbnailHover:!1,showBullets:!0,showThumbnails:!0,showNav:!0,slideInterval:2e3,fullscreen:!1},n}return(0,y["default"])(t,e),(0,p["default"])(t,[{key:"componentWillMount",value:function(){var e=this.props.location.query.testbatchuid;this.fetchScreenshots(e)}},{key:"componentWillUnmount",value:function(){this.debug("componentWillUnmount")}},{key:"fetchScreenshots",value:function(e){var t=this.getBrowserId(),n={token:this.props.state.session.token,actions:[{action:"read",model:"testscreenshot",filters:{test_batch_id:e,browser_id:t}},{action:"read",model:"testbatch",uid:e}]};this.props.actions.doFetchScreenshots(n)}},{key:"getBrowserId",value:function(){return this.props.location.query.browserId}},{key:"getBrowserName",value:function(){return this.props.location.query.browserName}},{key:"getBrowserIcon",value:function(){return this.props.location.query.browserIcon}},{key:"getBrowserVersion",value:function(){return this.props.location.query.browserVersion}},{key:"getPlatform",value:function(){return this.props.location.query.platform}},{key:"pauseSlider",value:function(){this.refs.imageGallery.pause(),this.setState({isPlaying:!1})}},{key:"playSlider",value:function(){this.refs.imageGallery.play(),this.setState({isPlaying:!0})}},{key:"fullScreen",value:function(){this.refs.imageGallery.fullScreen()}},{key:"onImageClick",value:function(){this.debug("onImageClick")}},{key:"onImageLoad",value:function(){this.debug("onImageLoad")}},{key:"onSlide",value:function(){this.debug("onSlide")}},{key:"onPause",value:function(){this.debug("onPause")}},{key:"onPlay",value:function(){this.debug("onPlay")}},{key:"handleInputChange",value:function(e){this.setState((0,r["default"])({},e.target.dataset.action,e.target.value))}},{key:"handleCheckboxChange",value:function(e){this.setState((0,r["default"])({},e.target.dataset.action,e.target.checked))}},{key:"render",value:function(){var e=this,t=this.props.state.testbatchscreenshots;if(t.loading)return v["default"].createElement("div",{className:"container-fluid"},v["default"].createElement(I["default"],{style:{left:"50%"}}));if(t.error)return v["default"].createElement(C["default"],{msgId:t.error});var n=function(){var n=[];t.screenshots.map(function(e,t){n.push({original:e.file_path,description:e.title,thumbnail:e.file_path})});var a=[{msgId:"TestBatchDetail",to:"/testbatchdetail?testbatchuid="+t.testBatch.uid},{msgId:"BrowserIdsList",to:"/browseridslist?path=testbatchscreenshots&testbatchuid="+t.testBatch.uid},{msgId:"TestBatchScreenshots",disable:!0}];return{v:v["default"].createElement("div",{className:"container-fluid"},v["default"].createElement(_["default"],{routes:a}),v["default"].createElement("h2",null,"Test Batch Screenshots"," - ",v["default"].createElement("small",null,"(",t.testBatch.friendly_name,") (",t.testBatch.uid,")")," - ",v["default"].createElement("small",null,v["default"].createElement(E["default"],{browserName:e.getBrowserName(),browserIcon:e.getBrowserIcon(),browserVersion:e.getBrowserVersion(),platform:e.getPlatform()}))),v["default"].createElement(T["default"],{ref:"imageGallery",items:n,lazyLoad:!1,infinite:e.state.infinite,showBullets:e.state.showBullets,showThumbnails:e.state.showThumbnails,showIndex:e.state.showIndex,showNav:e.state.showNav,slideInterval:parseInt(e.state.slideInterval),autoPlay:e.state.isPlaying,slideOnThumbnailHover:e.state.slideOnThumbnailHover}),v["default"].createElement("ul",{className:"nav nav-pills "+O["default"].toolbox},v["default"].createElement("li",null,v["default"].createElement("button",{className:"btn "+(e.state.isPlaying?"btn-primary":"btn-default"),onClick:e.playSlider},"Play")),v["default"].createElement("li",null,v["default"].createElement("button",{className:"btn "+(e.state.isPlaying?"btn-default":"btn-primary"),onClick:e.pauseSlider},"Pause")),v["default"].createElement("li",null,v["default"].createElement("button",{className:"btn btn-default",onClick:e.fullScreen},"Full Screen"))),v["default"].createElement("div",null,v["default"].createElement("ul",{className:"list-unstyled"},v["default"].createElement("li",null,v["default"].createElement("div",{className:"checkbox"},v["default"].createElement("label",null,v["default"].createElement("input",{id:"infinite",type:"checkbox","data-action":"infinite",onChange:e.handleCheckboxChange,checked:e.state.infinite}),"Infinite sliding"))),v["default"].createElement("li",null,v["default"].createElement("div",{className:"checkbox"},v["default"].createElement("label",null,v["default"].createElement("input",{id:"show_bullets","data-action":"showBullets",type:"checkbox",onChange:e.handleCheckboxChange,checked:e.state.showBullets}),"Show bullets"))),v["default"].createElement("li",null,v["default"].createElement("div",{className:"checkbox"},v["default"].createElement("label",null,v["default"].createElement("input",{id:"show_thumbnails",type:"checkbox","data-action":"showThumbnails",onChange:e.handleCheckboxChange,checked:e.state.showThumbnails}),"Show thumbnails"))),v["default"].createElement("li",null,v["default"].createElement("div",{className:"checkbox"},v["default"].createElement("label",null,v["default"].createElement("input",{id:"show_navigation",type:"checkbox","data-action":"showNav",onChange:e.handleCheckboxChange,checked:e.state.showNav}),"Show navigation"))),v["default"].createElement("li",null,v["default"].createElement("div",{className:"checkbox"},v["default"].createElement("label",null,v["default"].createElement("input",{id:"show_index",type:"checkbox","data-action":"showIndex",onChange:e.handleCheckboxChange,checked:e.state.showIndex}),"Show index"))),v["default"].createElement("li",null,v["default"].createElement("div",{className:"checkbox"},v["default"].createElement("label",null,v["default"].createElement("input",{id:"slide_on_thumbnail_hover",type:"checkbox","data-action":"slideOnThumbnailHover",onChange:e.handleCheckboxChange,checked:e.state.slideOnThumbnailHover}),"Slide on thumbnail hover (desktop)"))))))}}();return"object"===("undefined"==typeof n?"undefined":(0,l["default"])(n))?n.v:void 0}}]),t}(L["default"]);e.exports=M},460:function(e,t,n){"use strict";function a(e){return e&&e.__esModule?e:{"default":e}}function i(e){return{state:e}}function l(e){return{actions:(0,r.bindActionCreators)(o.actions,e)}}Object.defineProperty(t,"__esModule",{value:!0});var s=n(17),r=n(21),o=n(313),u=n(459),d=a(u);t["default"]=(0,s.connect)(i,l)(d["default"])},490:function(e,t,n){"use strict";function a(e){return e&&e.__esModule?e:{"default":e}}t.__esModule=!0;var i=n(319),l=a(i);t["default"]=function(e,t,n){return t in e?(0,l["default"])(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}},534:function(e,t,n){t=e.exports=n(8)(),t.push([e.id,".image-gallery{-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;-o-user-select:none;user-select:none}.image-gallery-content{position:relative}.image-gallery-content .image-gallery-left-nav,.image-gallery-content .image-gallery-right-nav{color:#fff;cursor:pointer;font-family:Arial,Helvetica Neue,Helvetica,sans-serif;font-size:6em;line-height:0;position:absolute;text-shadow:0 2px 2px #222;top:48%;transition:all .2s ease-out;z-index:4}@media (max-width:768px){.image-gallery-content .image-gallery-left-nav,.image-gallery-content .image-gallery-right-nav{font-size:3.4em}}@media (min-width:768px){.image-gallery-content .image-gallery-left-nav:hover,.image-gallery-content .image-gallery-right-nav:hover{color:#fff}}.image-gallery-content .image-gallery-left-nav{left:0}.image-gallery-content .image-gallery-left-nav:before{content:'\\2039';padding:50px 15px}.image-gallery-content .image-gallery-right-nav{right:0}.image-gallery-content .image-gallery-right-nav:before{content:'\\203A';padding:50px 15px}.image-gallery-slides{line-height:0;overflow:hidden;position:relative;white-space:nowrap}.image-gallery-slide{left:0;position:absolute;top:0;width:100%}.image-gallery-slide.center{position:relative}.image-gallery-slide img{width:100%}.image-gallery-slide .image-gallery-description{background:rgba(0,0,0,.4);bottom:70px;color:#fff;left:0;line-height:1;padding:10px 20px;position:absolute;transition:all .45s ease-out;white-space:normal}@media (max-width:768px){.image-gallery-slide .image-gallery-description{bottom:45px;font-size:.8em;padding:8px 15px}}.image-gallery-bullets{bottom:20px;position:absolute;text-align:center;width:100%;z-index:4}.image-gallery-bullets .image-gallery-bullets-container{margin:0;padding:0}.image-gallery-bullets .image-gallery-bullet{border:1px solid #fff;border-radius:50%;box-shadow:0 1px 0 #222;cursor:pointer;display:inline-block;margin:0 5px;padding:5px}@media (max-width:768px){.image-gallery-bullets .image-gallery-bullet{margin:0 3px;padding:3px}}.image-gallery-bullets .image-gallery-bullet.active{background:#fff}.image-gallery-thumbnails{background:#fff;overflow:hidden;padding-top:5px}.image-gallery-thumbnails .image-gallery-thumbnails-container{cursor:pointer;text-align:center;transition:all .45s ease-out;white-space:nowrap}.image-gallery-thumbnail{display:inline-block;padding-right:5px}.image-gallery-thumbnail img{border:4px solid transparent;transition:border .3s ease-out;vertical-align:middle;width:100px}@media (max-width:768px){.image-gallery-thumbnail img{border:3px solid transparent;width:75px}}.image-gallery-thumbnail.active img{border:4px solid #337ab7}@media (max-width:768px){.image-gallery-thumbnail.active img{border:3px solid #337ab7}}.image-gallery-index{background:rgba(0,0,0,.4);bottom:0;color:#fff;line-height:1;padding:10px 20px;position:absolute;right:0;z-index:4}",""])},553:function(e,t){e.exports={toolbox:"ComponentStyle__toolbox___2Oj9_"}},618:function(e,t,n){"use strict";function a(e){return e&&e.__esModule?e:{"default":e}}function i(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function l(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!=typeof t&&"function"!=typeof t?e:t}function s(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}function r(e,t){var n=void 0,a=void 0,i=void 0,l=null,s=0,r=function(){s=(new Date).getTime(),l=null,i=e.apply(n,a),l||(n=a=null)};return function(){var o=(new Date).getTime(),u=t-(o-s);return n=this,a=arguments,u<=0||u>t?(l&&(clearTimeout(l),l=null),s=o,i=e.apply(n,a),l||(n=a=null)):l||(l=setTimeout(r,u)),i}}function o(){var e=r.apply(void 0,arguments);return function(t){return t?(t.persist(),e(t)):e()}}Object.defineProperty(t,"__esModule",{value:!0});var u=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var a in n)Object.prototype.hasOwnProperty.call(n,a)&&(e[a]=n[a])}return e},d=function(){function e(e,t){for(var n=0;n<t.length;n++){var a=t[n];a.enumerable=a.enumerable||!1,a.configurable=!0,"value"in a&&(a.writable=!0),Object.defineProperty(e,a.key,a)}}return function(t,n,a){return n&&e(t.prototype,n),a&&e(t,a),t}}(),h=n(2),c=a(h),p=n(652),f=a(p),m=500,g=function(e){function t(e){i(this,t);var n=l(this,Object.getPrototypeOf(t).call(this,e));return n.state={currentIndex:e.startIndex,thumbsTranslateX:0,offsetPercentage:0,galleryWidth:0},n}return s(t,e),d(t,[{key:"componentDidUpdate",value:function(e,t){t.galleryWidth===this.state.galleryWidth&&e.showThumbnails===this.props.showThumbnails||this._setThumbsTranslateX(-this._getThumbsTranslateX(this.state.currentIndex>0?1:0)*this.state.currentIndex),t.currentIndex!==this.state.currentIndex&&(this.props.onSlide&&this.props.onSlide(this.state.currentIndex),this._updateThumbnailTranslateX(t))}},{key:"componentWillMount",value:function(){this._slideLeft=o(this._slideLeft.bind(this),m,!0),this._slideRight=o(this._slideRight.bind(this),m,!0),this._handleResize=this._handleResize.bind(this),this._handleKeyDown=this._handleKeyDown.bind(this),this._thumbnailDelay=300}},{key:"componentDidMount",value:function(){var e=this;window.setTimeout(function(){return e._handleResize()},500),this.props.autoPlay&&this.play(),this.props.disableArrowKeys||window.addEventListener("keydown",this._handleKeyDown),window.addEventListener("resize",this._handleResize)}},{key:"componentWillUnmount",value:function(){this.props.disableArrowKeys||window.removeEventListener("keydown",this._handleKeyDown),window.removeEventListener("resize",this._handleResize),this._intervalId&&(window.clearInterval(this._intervalId),this._intervalId=null)}},{key:"play",value:function(){var e=this,t=arguments.length<=0||void 0===arguments[0]||arguments[0];if(!this._intervalId){var n=this.props.slideInterval;this._intervalId=window.setInterval(function(){e.state.hovering||(e.props.infinite||e._canSlideRight()?e.slideToIndex(e.state.currentIndex+1):e.pause())},n>m?n:m),this.props.onPlay&&t&&this.props.onPlay(this.state.currentIndex)}}},{key:"pause",value:function(){var e=arguments.length<=0||void 0===arguments[0]||arguments[0];this._intervalId&&(window.clearInterval(this._intervalId),this._intervalId=null),this.props.onPause&&e&&this.props.onPause(this.state.currentIndex)}},{key:"fullScreen",value:function(){var e=this._imageGallery;e.requestFullscreen?e.requestFullscreen():e.msRequestFullscreen?e.msRequestFullscreen():e.mozRequestFullScreen?e.mozRequestFullScreen():e.webkitRequestFullscreen&&e.webkitRequestFullscreen()}},{key:"slideToIndex",value:function(e,t){t&&(t.preventDefault(),this._intervalId&&(this.pause(!1),this.play(!1)));var n=this.props.items.length-1,a=e;e<0?a=n:e>n&&(a=0),this.setState({previousIndex:this.state.currentIndex,currentIndex:a,offsetPercentage:0,style:{transition:"transform .45s ease-out"}})}},{key:"getCurrentIndex",value:function(){return this.state.currentIndex}},{key:"_handleResize",value:function(){this._imageGallery&&this.setState({galleryWidth:this._imageGallery.offsetWidth})}},{key:"_handleKeyDown",value:function(e){var t=37,n=39,a=parseInt(e.keyCode||e.which||0);switch(a){case t:this._canSlideLeft()&&!this._intervalId&&this._slideLeft();break;case n:this._canSlideRight()&&!this._intervalId&&this._slideRight()}}},{key:"_handleMouseOverThumbnails",value:function(e){var t=this;this.props.slideOnThumbnailHover&&(this.setState({hovering:!0}),this._thumbnailTimer&&(window.clearTimeout(this._thumbnailTimer),this._thumbnailTimer=null),this._thumbnailTimer=window.setTimeout(function(){t.slideToIndex(e)},this._thumbnailDelay))}},{key:"_handleMouseLeaveThumbnails",value:function(){this._thumbnailTimer&&(window.clearTimeout(this._thumbnailTimer),this._thumbnailTimer=null,this.props.autoPlay===!0&&this.play(!1)),this.setState({hovering:!1})}},{key:"_handleMouseOver",value:function(){this.setState({hovering:!0})}},{key:"_handleMouseLeave",value:function(){this.setState({hovering:!1})}},{key:"_handleImageError",value:function(e){this.props.defaultImage&&e.target.src.indexOf(this.props.defaultImage)===-1&&(e.target.src=this.props.defaultImage)}},{key:"_handleOnSwiped",value:function(e,t,n,a){this.setState({isFlick:a})}},{key:"_handleOnSwipedTo",value:function(e){var t=this.state.currentIndex;(Math.abs(this.state.offsetPercentage)>30||this.state.isFlick)&&(t+=e),e<0?this._canSlideLeft()||(t=this.state.currentIndex):this._canSlideRight()||(t=this.state.currentIndex),this.slideToIndex(t)}},{key:"_handleSwiping",value:function(e,t,n){var a=e*(n/this.state.galleryWidth*100);this.setState({offsetPercentage:a,style:{}})}},{key:"_canNavigate",value:function(){return this.props.items.length>=2}},{key:"_canSlideLeft",value:function(){return!!this.props.infinite||this.state.currentIndex>0}},{key:"_canSlideRight",value:function(){return!!this.props.infinite||this.state.currentIndex<this.props.items.length-1}},{key:"_updateThumbnailTranslateX",value:function(e){if(0===this.state.currentIndex)this._setThumbsTranslateX(0);else{var t=Math.abs(e.currentIndex-this.state.currentIndex),n=this._getThumbsTranslateX(t);n>0&&(e.currentIndex<this.state.currentIndex?this._setThumbsTranslateX(this.state.thumbsTranslateX-n):e.currentIndex>this.state.currentIndex&&this._setThumbsTranslateX(this.state.thumbsTranslateX+n))}}},{key:"_setThumbsTranslateX",value:function(e){this.setState({thumbsTranslateX:e})}},{key:"_getThumbsTranslateX",value:function(e){if(this.props.disableThumbnailScroll)return 0;if(this._thumbnails){if(this._thumbnails.scrollWidth<=this.state.galleryWidth)return 0;var t=this._thumbnails.children.length,n=this._thumbnails.scrollWidth-this.state.galleryWidth,a=n/(t-1);return e*a}}},{key:"_getAlignmentClassName",value:function(e){var t=this.state.currentIndex,n="",a="left",i="center",l="right";switch(e){case t-1:n=" "+a;break;case t:n=" "+i;break;case t+1:n=" "+l}return this.props.items.length>=3&&this.props.infinite&&(0===e&&t===this.props.items.length-1?n=" "+l:e===this.props.items.length-1&&0===t&&(n=" "+a)),n}},{key:"_getSlideStyle",value:function(e){var t=this.state,n=t.currentIndex,a=t.offsetPercentage,i=-100*n,l=this.props.items.length-1,s=i+100*e+a,r=1;this.props.infinite&&this.props.items.length>2&&(0===n&&e===l?s=-100+a:n===l&&0===e&&(s=100+a)),e===n?r=3:e===this.state.previousIndex&&(r=2);var o="translate3d("+s+"%, 0, 0)";return{WebkitTransform:o,MozTransform:o,msTransform:o,OTransform:o,transform:o,zIndex:r}}},{key:"_getThumbnailStyle",value:function(){var e="translate3d("+this.state.thumbsTranslateX+"px, 0, 0)";return{WebkitTransform:e,MozTransform:e,msTransform:e,OTransform:e,transform:e}}},{key:"_slideLeft",value:function(e){this.slideToIndex(this.state.currentIndex-1,e)}},{key:"_slideRight",value:function(e){this.slideToIndex(this.state.currentIndex+1,e)}},{key:"_renderItem",value:function(e){var t=this.props.onImageError||this._handleImageError;return c["default"].createElement("div",{className:"image-gallery-image"},c["default"].createElement("img",{src:e.original,alt:e.originalAlt,srcSet:e.srcSet,sizes:e.sizes,onLoad:this.props.onImageLoad,onError:t.bind(this)}),e.description&&c["default"].createElement("span",{className:"image-gallery-description"},e.description))}},{key:"render",value:function(){var e=this,t=this.state.currentIndex,n=this._getThumbnailStyle(),a=this._slideLeft.bind(this),i=this._slideRight.bind(this),l=[],s=[],r=[];return this.props.items.map(function(n,a){var i=e._getAlignmentClassName(a),o=n.originalClass?" "+n.originalClass:"",d=n.thumbnailClass?" "+n.thumbnailClass:"",h=n.renderItem||e.props.renderItem||e._renderItem.bind(e),p=c["default"].createElement("div",{key:a,className:"image-gallery-slide"+i+o,style:u(e._getSlideStyle(a),e.state.style),onClick:e.props.onClick},h(n));e.props.lazyLoad?i&&l.push(p):l.push(p);var f=e._handleImageError;e.props.onThumbnailError&&(f=e.props.onThumbnailError),e.props.showThumbnails&&s.push(c["default"].createElement("a",{onMouseOver:e._handleMouseOverThumbnails.bind(e,a),onMouseLeave:e._handleMouseLeaveThumbnails.bind(e,a),key:a,className:"image-gallery-thumbnail"+(t===a?" active":"")+d,onTouchStart:function(t){return e.slideToIndex.call(e,a,t)},onClick:function(t){return e.slideToIndex.call(e,a,t)}},c["default"].createElement("img",{src:n.thumbnail,alt:n.thumbnailAlt,onError:f.bind(e)}))),e.props.showBullets&&r.push(c["default"].createElement("li",{key:a,className:"image-gallery-bullet "+(t===a?"active":""),onTouchStart:function(t){return e.slideToIndex.call(e,a,t)},onClick:function(t){return e.slideToIndex.call(e,a,t)}}))}),c["default"].createElement("section",{ref:function(t){return e._imageGallery=t},className:"image-gallery"},c["default"].createElement("div",{onMouseOver:this._handleMouseOver.bind(this),onMouseLeave:this._handleMouseLeave.bind(this),className:"image-gallery-content"},this._canNavigate()?[this.props.showNav&&c["default"].createElement("span",{key:"navigation"},this._canSlideLeft()&&c["default"].createElement("a",{className:"image-gallery-left-nav",onTouchStart:a,onClick:a}),this._canSlideRight()&&c["default"].createElement("a",{className:"image-gallery-right-nav",onTouchStart:i,onClick:i})),c["default"].createElement(f["default"],{className:"image-gallery-swipe",key:"swipeable",delta:1,onSwipingLeft:this._handleSwiping.bind(this,-1),onSwipingRight:this._handleSwiping.bind(this,1),onSwiped:this._handleOnSwiped.bind(this),onSwipedLeft:this._handleOnSwipedTo.bind(this,1),onSwipedRight:this._handleOnSwipedTo.bind(this,-1)},c["default"].createElement("div",{className:"image-gallery-slides"},l))]:c["default"].createElement("div",{className:"image-gallery-slides"},l),this.props.showBullets&&c["default"].createElement("div",{className:"image-gallery-bullets"},c["default"].createElement("ul",{className:"image-gallery-bullets-container"},r)),this.props.showIndex&&c["default"].createElement("div",{className:"image-gallery-index"},c["default"].createElement("span",{className:"image-gallery-index-current"},this.state.currentIndex+1),c["default"].createElement("span",{className:"image-gallery-index-separator"},this.props.indexSeparator),c["default"].createElement("span",{className:"image-gallery-index-total"},this.props.items.length))),this.props.showThumbnails&&c["default"].createElement("div",{className:"image-gallery-thumbnails"},c["default"].createElement("div",{ref:function(t){return e._thumbnails=t},className:"image-gallery-thumbnails-container",style:n},s)))}}]),t}(c["default"].Component);t["default"]=g,g.propTypes={items:c["default"].PropTypes.array.isRequired,showNav:c["default"].PropTypes.bool,autoPlay:c["default"].PropTypes.bool,lazyLoad:c["default"].PropTypes.bool,infinite:c["default"].PropTypes.bool,showIndex:c["default"].PropTypes.bool,showBullets:c["default"].PropTypes.bool,showThumbnails:c["default"].PropTypes.bool,slideOnThumbnailHover:c["default"].PropTypes.bool,disableThumbnailScroll:c["default"].PropTypes.bool,disableArrowKeys:c["default"].PropTypes.bool,defaultImage:c["default"].PropTypes.string,indexSeparator:c["default"].PropTypes.string,startIndex:c["default"].PropTypes.number,slideInterval:c["default"].PropTypes.number,onSlide:c["default"].PropTypes.func,onPause:c["default"].PropTypes.func,onPlay:c["default"].PropTypes.func,onClick:c["default"].PropTypes.func,onImageLoad:c["default"].PropTypes.func,onImageError:c["default"].PropTypes.func,onThumbnailError:c["default"].PropTypes.func,renderItem:c["default"].PropTypes.func},g.defaultProps={items:[],showNav:!0,autoPlay:!1,lazyLoad:!1,infinite:!0,showIndex:!1,showBullets:!1,showThumbnails:!0,slideOnThumbnailHover:!1,disableThumbnailScroll:!1,disableArrowKeys:!1,indexSeparator:" / ",startIndex:0,slideInterval:3e3}},652:function(e,t,n){"use strict";var a=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var a in n)Object.prototype.hasOwnProperty.call(n,a)&&(e[a]=n[a])}return e},i=n(2),l=i.createClass({displayName:"Swipeable",propTypes:{onSwiped:i.PropTypes.func,onSwiping:i.PropTypes.func,onSwipingUp:i.PropTypes.func,onSwipingRight:i.PropTypes.func,onSwipingDown:i.PropTypes.func,onSwipingLeft:i.PropTypes.func,onSwipedUp:i.PropTypes.func,onSwipedRight:i.PropTypes.func,onSwipedDown:i.PropTypes.func,onSwipedLeft:i.PropTypes.func,flickThreshold:i.PropTypes.number,delta:i.PropTypes.number,preventDefaultTouchmoveEvent:i.PropTypes.bool,nodeName:i.PropTypes.string},getInitialState:function(){return{x:null,y:null,swiping:!1,start:0}},getDefaultProps:function(){return{flickThreshold:.6,delta:10,preventDefaultTouchmoveEvent:!0,nodeName:"div"}},calculatePos:function(e){var t=e.changedTouches[0].clientX,n=e.changedTouches[0].clientY,a=this.state.x-t,i=this.state.y-n,l=Math.abs(a),s=Math.abs(i),r=Date.now()-this.state.start,o=Math.sqrt(l*l+s*s)/r;return{deltaX:a,deltaY:i,absX:l,absY:s,velocity:o}},touchStart:function(e){e.touches.length>1||this.setState({start:Date.now(),x:e.touches[0].clientX,y:e.touches[0].clientY,swiping:!1})},touchMove:function(e){if(this.state.x&&this.state.y&&!(e.touches.length>1)){var t=!1,n=this.calculatePos(e);n.absX<this.props.delta&&n.absY<this.props.delta||(this.props.onSwiping&&this.props.onSwiping(e,n.deltaX,n.deltaY,n.absX,n.absY,n.velocity),n.absX>n.absY?n.deltaX>0?(this.props.onSwipingLeft||this.props.onSwipedLeft)&&(this.props.onSwipingLeft&&this.props.onSwipingLeft(e,n.absX),t=!0):(this.props.onSwipingRight||this.props.onSwipedRight)&&(this.props.onSwipingRight&&this.props.onSwipingRight(e,n.absX),t=!0):n.deltaY>0?(this.props.onSwipingUp||this.props.onSwipedUp)&&(this.props.onSwipingUp&&this.props.onSwipingUp(e,n.absY),t=!0):(this.props.onSwipingDown||this.props.onSwipedDown)&&(this.props.onSwipingDown&&this.props.onSwipingDown(e,n.absY),t=!0),this.setState({swiping:!0}),t&&this.props.preventDefaultTouchmoveEvent&&e.preventDefault())}},touchEnd:function(e){if(this.state.swiping){var t=this.calculatePos(e),n=t.velocity>this.props.flickThreshold;this.props.onSwiped&&this.props.onSwiped(e,t.deltaX,t.deltaY,n),t.absX>t.absY?t.deltaX>0?this.props.onSwipedLeft&&this.props.onSwipedLeft(e,t.deltaX,n):this.props.onSwipedRight&&this.props.onSwipedRight(e,t.deltaX,n):t.deltaY>0?this.props.onSwipedUp&&this.props.onSwipedUp(e,t.deltaY,n):this.props.onSwipedDown&&this.props.onSwipedDown(e,t.deltaY,n)}this.setState(this.getInitialState())},render:function(){var e=a({},this.props,{onTouchStart:this.touchStart,onTouchMove:this.touchMove,onTouchEnd:this.touchEnd});return delete e.onSwiped,delete e.onSwiping,delete e.onSwipingUp,delete e.onSwipingRight,delete e.onSwipingDown,delete e.onSwipingLeft,delete e.onSwipedUp,delete e.onSwipedRight,delete e.onSwipedDown,delete e.onSwipedLeft,delete e.flickThreshold,delete e.delta,delete e.preventDefaultTouchmoveEvent,delete e.nodeName,delete e.children,i.createElement(this.props.nodeName,e,this.props.children)}});e.exports=l},724:function(e,t,n){var a=n(534);"string"==typeof a&&(a=[[e.id,a,""]]);n(23)(a,{});a.locals&&(e.exports=a.locals)}});
//# sourceMappingURL=12.ea893b67f4e6e0aa26ca.chunk.js.map