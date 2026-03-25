/* ld google ads */
google_ad_client = 'ca-livedoor-blog_js';
google_max_num_ads = '3';
google_ad_channel = 'blog_2';
google_ad_output = 'js';
google_ad_type = 'text';
google_language = 'ja';
google_country = 'JP';
google_encoding = (typeof(ld_blog_vars) == 'object' ? ld_blog_vars.charset : 'euc-jp');
google_safe = 'high';
google_n_ads_rs = '2';

jlisting_mid = "10026062";
jlisting_chid = "0cf3d5e071477d0f97c29eddef9cd489";
jlisting_limit = "3";
jlisting_network = "contents";

ld_google_ad_format_func = function (ads, addiv, adtype){
   return '<div class="adbox" style="margin: 5px; padding: 2px 0 2px 18px;" onmouseover="adsHover(this,1);" onmouseout="adsHover(this,0);">' 
	  + '<div class="adtop" style="white-space: nowrap; overflow: hidden; width: 100%;"><a href="' + ads.url + '" onclick="javascript:'
	  + 'if(typeof(blog_counter_adtrk) == \'function\') { return blog_counter_adtrk(\''+addiv+'\', \'' + adtype + '\',\'' + ads.url + '\');}" class="adtitle" style="text-decoration:none;">'
	  + '<span style="font-size: 14px; font-weight: bold; text-decoration: underline; line-height:200%;">' + ads.line1 + '</span></a>' 
	  + '<a href="' + ads.url + '" onclick="javascript:'
	  + 'if(typeof(blog_counter_adtrk) == \'function\') { return blog_counter_adtrk(\''+addiv+'\', \'' + adtype + '\',\'' + ads.url + '\');}" class="adurl" style="text-decoration:none;margin-left:10px;">' 
	  + '<span style="font-size: 11px;">' + ads.visible_url + '</span></a></div>'
 	  + '<a class="addescription" style="text-decoration:none;">'
 	  + '<span style="font-size: 12px;">' + ads.line2 + '&nbsp;' + ads.line3 + '</span></a></div>';
};

ld_jlisting_ad_format_func = function (orig_ads, addiv, adtype){
    var ads = {};
    for (key in orig_ads) {
        ads[key] = orig_ads[key].replace(/&quot;/g, '"').replace(/&#39;/g, '\'').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
    }
    return '<div class="adbox" style="margin: 5px; padding: 2px 0 2px 18px;" onmouseover="adsHover(this,1);" onmouseout="adsHover(this,0);">' 
	  + '<div class="adtop" style="white-space: nowrap; overflow: hidden; width: 100%;"><a href="' + ads.clickurl + '" onclick="javascript:'
	  + 'if(typeof(blog_counter_adtrk) == \'function\') { return blog_counter_adtrk(\''+addiv+'\', \'' + adtype + '\',\'' + ads.clickurl + '\');}" class="adtitle" style="text-decoration:none;">'
	  + '<span style="font-size: 14px; font-weight: bold; text-decoration: underline; line-height:200%;">' + ads.title + '</span></a>' 
	  + '<a href="' + ads.clickurl + '" onclick="javascript:'
	  + 'if(typeof(blog_counter_adtrk) == \'function\') { return blog_counter_adtrk(\''+addiv+'\', \'' + adtype + '\',\'' + ads.clickurl + '\');}" class="adurl" style="text-decoration:none;margin-left:10px;">' 
	  + '<span style="font-size: 11px;">' + ads.url + '</span></a></div>'
 	  + '<a class="addescription" style="text-decoration:none;">'
 	  + '<span style="font-size: 12px;">' + ads.comment1 + ads.comment2 + '</span></a></div>';
};

var ld_blog_ads_switcher = {
    is_google: function() {
        return 1;
    },
    is_jlisting: function() {
        return 0;
    }
};

ld_category_ad_encoding = (typeof(ld_blog_vars) == 'object' ? ld_blog_vars.charset : '');
ld_category_ad_tag = "";

// next portion of this script based on:
// domready.js (http://snipplr.com/view/6029/domreadyjs/)
// copyright (c) 2007 Takanori Ishikawa (MIT-style license)
if (typeof Event == 'undefined') Event = new Object();Event.domReady = { add: function(fn) { if (Event.domReady.loaded) return fn(); var observers = Event.domReady.observers; if (!observers) observers = Event.domReady.observers = []; observers[observers.length] = fn; if (Event.domReady.callback) return; Event.domReady.callback = function() { if (Event.domReady.loaded) return; Event.domReady.loaded = true; if (Event.domReady.timer) { clearInterval(Event.domReady.timer); Event.domReady.timer = null; } var observers = Event.domReady.observers; for (var i = 0, length = observers.length; i < length; i++) { var fn = observers[i]; observers[i] = null; fn(); } Event.domReady.callback = Event.domReady.observers = null; }; var ie = !!(window.attachEvent && !window.opera); var webkit = navigator.userAgent.indexOf('AppleWebKit/') > -1; if (document.readyState && webkit) { Event.domReady.timer = setInterval(function() { var state = document.readyState; if (state == 'loaded' || state == 'complete') { Event.domReady.callback(); } }, 50); } else if (document.readyState && ie) { var src = (window.location.protocol == 'https:') ? '://0' : 'javascript:void(0)'; document.write( '<scr'+'ipt type="text/javascript" defer="defer" src="' + src + '" ' +  'onreadystatechange="if (this.readyState == \'complete\') { Event.domReady.timer = setInterval(function() { Event.domReady.callback(); }, 50); }"' +  '><\/scr'+'ipt>');} else { if (window.addEventListener) { document.addEventListener("DOMContentLoaded", Event.domReady.callback, false); window.addEventListener("load", Event.domReady.callback, false); } else if (window.attachEvent) { window.attachEvent('onload', Event.domReady.callback); } else { var fn = window.onload; window.onload = function() { Event.domReady.callback(); if (fn) fn(); } } } } };
Event.domReady.add(function(){});

(function(){
    var rs = document.getElementById('ad_rs');
	if (typeof(FromSearchEngine) == 'boolean' && FromSearchEngine) {
       // google_max_num_ads = '8';
       // google_n_ads_rs = '3';
       google_ad_channel = 'blog_search';
	} else {
       google_max_num_ads = '3';
    }
})();


function google_ad_request_done(google_ads) {
    var from_search_engine = (typeof(FromSearchEngine) == 'boolean' && FromSearchEngine) ? true : false;
       var formatter = function(){
	      var s = '';
	      var i;
	      if (google_ads.length == 0)  return;
	      var len = google_ads.length;

	      var rs = document.getElementById('ad_rs');

	      s +='<div class="gAdsense" id="gAdsense_google_jp" style="margin: 0 auto; padding: 5px; text-align: left;">'
	        + '<div style="margin:0 15px; font-size: 11px;"><a href="https://www.google.co.jp/intl/ja/ads/" class="adld" rel="nofollow">Ads by Google</a></div>';
	      for (var i = 0; i < len; i++) {
  	         s += ld_google_ad_format_func(google_ads[i], (from_search_engine ? 'ad_rs' : 'ad2'), 'google');
	      }
	      s +='</div>';
          s = '<div id="ad">' + s + '</div>';

          s += ld_category_ad_tag;
          
          var ad = document.getElementById('ad') || document.getElementById('ad2');
	      if (from_search_engine) {
		     if (rs) { 
                // image ad 2012/2/22 by okamoto
                rs.innerHTML = '<iframe id="ad_iframe" width="300" height="250" frameborder="0" marginheight="0" marginwidth="0" scrolling="no"></iframe>';
                rs.style['display'] = 'block';
                var ad_iframe = document.getElementById('ad_iframe');
                if (ad_iframe) {
                    ad_iframe.setAttribute('src', 'https://parts.blog.livedoor.jp/ad/afc_image_blog.html');
                }
	            if (ad) {
                   ad.innerHTML = s;
                   ad.style['display'] = 'block';
                }
             }
	         else if (ad) {
                ad.innerHTML = s;
                ad.style['display'] = 'block';
             }
	      }
	      else { 
             if (ad) {
                ad.innerHTML = s;
                ad.style['display'] = 'block';
             }
          }
	      return;

       };
       Event.domReady.loaded ? formatter() : Event.domReady.add(formatter);
}

function adsHover(e,f){
   e.style.background = f ? '#ffffbb' : '';
   e.style.border = f ? '1px solid #ffffbb' : '0';
   e.style.padding = f ? '1px 0 1px 17px' : '2px 0 2px 18px';
   e.className = f ? 'adhover' : 'adbox';
}

function adwires_api_result(jlisting_ads) {
       var formatter = function(){
           var s = '';
           var i;
           if (jlisting_ads.result.length == 0)  return;
           var len = jlisting_ads.result.length;

           s +='<div class="gAdsense" id="gAdsense_jlisting_jp" style="margin: 0 auto; padding: 5px; text-align: left;">';
           for (i=0; i < len; i++) {
               s += ld_jlisting_ad_format_func(jlisting_ads.result[i], 'ad2','jlisting');
           }
           s +='</div>';
           s = '<div id="ad">'+s+'</div>';

           var ad = document.getElementById('ad') || document.getElementById('ad2');
           if (ad) {
               ad.innerHTML = s;
               ad.style['display'] = 'block';
           }
           return;
       };
       Event.domReady.loaded ? formatter() : Event.domReady.add(formatter);
}

(function(){
    // 一部のカテゴリ時バナー
    var is_image_banner = true;
    var is_arms = false;
    var selected_arms_id;

    if (is_image_banner || is_arms) {
        window.onload = function(){
            var ad = document.getElementById('ad') || document.getElementById('ad2');
            if (ad) {
                var host = location.hostname.indexOf('blog-new.dev') !== -1 ? 'parts.blog-new.dev.livedoor.jp' : 'parts.blog.livedoor.jp';
                var src = 'https://' + host + '/ad/afc_image_c1.html';
                var ad_iframe = document.createElement('iframe');
                ad_iframe.setAttribute('width', '300');
                ad_iframe.setAttribute('height', '250');
                ad_iframe.setAttribute('frameborder', '0');
                ad_iframe.setAttribute('marginheight', '0');
                ad_iframe.setAttribute('marginwidth', '0');
                ad_iframe.setAttribute('scrolling', 'no');
                ad_iframe.setAttribute('src', src);
                ad.appendChild(ad_iframe);
                ad.style.display = 'block';
            }

            // from search engine 2012/04/20
            if (FromSearchEngine) {
                var rs = document.getElementById('ad_rs');
                if (rs) {
                    rs.innerHTML = '<iframe id="ad_iframe" width="300" height="250" frameborder="0" marginheight="0" marginwidth="0" scrolling="no"></iframe>';
                    rs.style.display = 'block';
                    var ad_iframe = document.getElementById('ad_iframe');
                    if (ad_iframe) {
                        ad_iframe.setAttribute('src', 'https://parts.blog.livedoor.jp/ad/afc_image_blog.html');
                    }
                }
            }
        };
    } else {
        document.write('<scr'+'ipt type="text/javascript" src="https://pagead2.googlesyndication.com/pagead/show_ads.js"></scr'+'ipt>');
    }
})();

/* end of google.js */
