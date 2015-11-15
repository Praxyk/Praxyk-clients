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
			FACE_DETECTION_URL: POD_URL + "face_detect/";
			TRANSACTION_URL: BASE_URL + "transactions/";
			RESULTS_URL: BASE_URL + "results/";
		};
		return { getURL : function(s) {
			return URL[s];
			}
		}
	}();
	
	var userid = null;
	var token = null;
	var email = null;
	var password = null;

	constructor(email,password){
		//get data ready
		var login_data = new Object();
		login_data.email = username;
		login_data.password = password;

		var json_data = JSON.stringify(login_data);

		api_call(URL.getURL("TOKEN_URL"),"POST",login_data,"text/json",function(result){
			if(typeof result != "number"){
				var login_json = $.parseJSON(result);
				if(login_json.code == 200) {
					this.userid = login_json.user.user_id;
					this.token = login_json.token;
					this.email = email;
					this.password = password;
				}
			});
		}else{
			throw {
				name: "Auth Error",
				message: "Invalid Login Credentials!"
			};
		}
	}
	
	var requires_auth = function(){
		if(this.token == null && this.userid == null){
			throw {
				name: "Auth Error",
				message: "No Valid Token!"
			};
		}
		api_call(URL.getURL("TOKEN_URL")+"?token="+this.token,"GET",null,function(result){
			if(typeof result == "number"){
				if(this.email != null && this.password != null){
					api_call(URL.getURL("TOKEN_URL"),"POST",login_data,"text/json",function(result){
						if(typeof result != number){
							var login_json = $.parseJSON(result);
							if(login_json.code == 200) {
								this.userid = login_json.user.user_id;
								this.token = login_json.token;
							}
						}
					});
				}
			}
		});
	}

	function api_call(url,method,payload,content_type,callback){
		var xhr = new XMLHttpRequest();

		xhr.onreadystatechange = function (){
			if(xhr.readyState==4 && xhr.status==200){
				callback(xhr.responseText);
			}else{
					callback(xhr.status)
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
