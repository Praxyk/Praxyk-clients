//Praxyk API Javascript Interface

class Praxyk{
	//all of the urls
	var URL = function() {
		var BASE_URL = "api.praxyk.com/v1/"
		var TLP_URL = BASE_URL + "tlp/";
		var POD_URL = BASE_URL + "pod/";
		var globals = {
			USER_URL: BASE_URL + "users/";
			TOKEN_URL: BASE_URL + "tokens/";
			PAYMENT_URL: BASE_URL + "payment/";
			COUPON_URL: BASE_URL + "coupon/"; 
			OCR_URL: POD_URL + "ocr/";
			SPAM_URL: POD_URL + "bayes_spam/";
			FACE_DETECTION_URL: POD_URL + "/";
			TRANSACTION_URL: BASE_URL + "transactions/";
			RESULTS_URL: BASE_URL + "results/";
		}
		return { getURL : function(s) {
			return URL[s];
			}
		}
	}();

	var username = null;
	var password = null;
	var userid = null;
	var token = null;

	constructor(email,password){
		api_call(URL.getURL("TOKEN_URL"),"POST".
	}

	function api_call(url,method,payload,content_type,callback){
		var xhr = new XMLHttpRequest();

		xhr.onreadystatechange = function (){
			if(xhr.readyState==4 && xhr.status==200){
				callback(xhr.responseText);
			} 
		}
			
		xhr.open(method,url,true);
		if(payload!=null){
			if(content_type!=null) xhr.setRequestHeader('Content-Type',content_type);
				xhr.send(payload);
			}else{
				xhr.send();
			}
		}

}
