var URL = function(s) {
	var BASE_URL = "http://api.praxyk.com/v1/"
	var TLP_URL = BASE_URL + "tlp/";
	var POD_URL = BASE_URL + "pod/";
	var globals = {
		USERS: BASE_URL + "users/",
		TOKENS: BASE_URL + "tokens/",
		PAYMENT: BASE_URL + "payment/",
		COUPON: BASE_URL + "coupon/", 
		OCR: POD_URL + "ocr/",
		BAYES_SPAM: POD_URL + "bayes_spam/",
		FACE_DETECTION: POD_URL + "face_detect/",
		TRANSACTION: BASE_URL + "transactions/",
		RESULTS: BASE_URL + "results/"
	};
	
	return globals[s];
};

function api_call(url,method,payload,content_type,prog,callback){
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function (){
		if(xhr.readyState==4 && xhr.status==200){
			return callback(xhr.responseText);
		}else if(xhr.readyState==4 && xhr.status!=200){
			return callback(null);
		}
	}
	if(prog != null){
		xhr.upload.onprogress = function(e) {
			var percentComplete = (e.loaded / e.total) * 100;
			prog(percentComplete)
		};
	}
	
	xhr.open(method,url,true);
	
	if(payload!=null){
		if(content_type!=null) xhr.setRequestHeader('Content-Type',content_type);
		xhr.send(payload);
	}else{
		xhr.send();
	}
}

function USERS_POST(email,name,password,callback){
	var users_post_data = new Object();
   users_post_data.email = email;
   users_post_data.password = password;
   users_post_data.name = name;
   
   var json_data = JSON.stringify(users_post_data);
	
	return api_call(URL('USERS'),"POST",json_data,"application/json",null,function(result) {
       if(result!=null){
			return callback($.parseJSON(result));
		 }else{
			 return callback(null);
		 }
   });
}

function USERS_PUT(token,userid,email,password,callback){
	var user_put_data = new Object();
	user_put_data.token = token;
	user_put_data.email = email;
	user_put_data.password = password;
	
	var json_data = JSON.stringify(users_put_data);
	
	return api_call(URL('USERS')+userid,"PUT",json_data,"application/json",null,function(result){
		if(result!=null){
			return callback($.parseJSON(result));
		 }else{
			 return callback(null);
		 }
	});
}

function USERS_GET(token,userid,email,password,callback){
	var user_get_data = new Object();
	user_get_data.token = token;
	user_get_data.email = email;
	user_get_data.password = password;
	
	var json_data = JSON.stringify(users_get_data);
	
	return api_call(URL('USERS')+userid,"GET",json_data,"application/json",null,function(result){
		if(result!=null){
			return callback($.parseJSON(result));
		 }else{
			 return callback(null);
		 }
	});
}

function USERS_DELETE(token,userid,callback){
	var user_get_data = new Object();
	user_get_data.token = token;
	
	var json_data = JSON.stringify(users_get_data);
	
	return api_call(URL('USERS')+userid,"DELETE",json_data,"application/json",null,function(result){
		if(result!=null){
			return callback($.parseJSON(result));
		 }else{
			 return callback(null);
		 }
	});
}

function TOKENS_GET(token,callback){
	var token_get_data = new Object();
	token_get_data.token = token;
	
	var json_data = JSON.stringify(token_get_data);
	
	return api_call(URL('TOKENS'),"GET",json_data,"application/json",null,function(result){
		if(result!=null){
			return callback($.parseJSON(result));
		 }else{
			 return callback(null);
		 }
	});
}

function TOKENS_POST(email,password,callback){
	var tokens_post_data = new Object();
	tokens_post_data.email = email;
	tokens_post_data.password = password;
	
	var json_data = JSON.stringify(tokens_post_data);
	
	return api_call(URL('TOKENS'),"POST",json_data,"application/json",null,function(result){
		if(result!=null){
			return callback($.parseJSON(result));
		 }else{
			 return callback(null);
		 }
	});
}

function PAYMENT_GET(token,userid,callback){
	var payment_get_data = new Object();
	payment_get_data.token = token;
	
	var json_data = JSON.stringify(tokens_post_data);
	
	return api_call(URL('PAYMENT')+userid,"GET",json_data,"application/json",null,function(result){
		if(result!=null){
			return callback($.parseJSON(result));
		 }else{
			 return callback(null);
		 }
	});
}

function PAYMENT_POST(token,user_id,name,card_number,exp_month,exp_year,cvc,address1,address2,city,state,zip,callback){
	var payment_post_data = new Object();
	payment_post_data.token = token;
	payment_post_data.name = name;
	payment_post_data.card_number = card_number;
	payment_post_data.exp_month = exp_month;
	payment_post_data.exp_year = exp_year;
	payment_post_data.cvc = cvc;
	payment_post_data.address1 = address1;
	payment_post_data.address2 = address2;
	payment_post_data.city = city;
	payment_post_data.state	=	state;
	payment_post_data.zip = zip;
	
	var json_data = JSON.stringify(payment_post_data);
	
		return api_call(URL('PAYMENT')+userid,"POST",json_data,"application/json",null,function(result){
		if(result!=null){
			return callback($.parseJSON(result));
		 }else{
			 return callback(null);
		 }
	});
}

function PAYMENT_DELETE(token,userid,callback){
	var payment_delete_data = new Object();
	payment_delete_data.token = token;
	
	var json_data = JSON.stringify(payment_delete_data);
	
	return api_call(URL('PAYMENT')+userid,"DELETE",json_data,"application/json",null,function(result){
		if(result!=null){
			return callback($.parseJSON(result));
		 }else{
			 return callback(null);
		 }
	});
}

function COUPON_POST(token,userid,coupon){
	var coupon_post_data = new Object();
	coupon_post_data.token = token;
	coupon_post_data.coupon = coupon;
	
	var json_data = JSON.stringify(coupon_post_data);
	
	return api_call(URL('COUPON')+userid,"POST",json_data,"application/json",null,function(result){
		if(result!=null){
			return callback($.parseJSON(result));
		 }else{
			 return callback(null);
		 }
	});
}

function OCR_POST(token,fileinputid,name,progress,callback){
	var input = $("#"+fileinputid).prop("files");
	var ocr_post_data = new FormData();
	for(var i=0;i<input.length;++i){
		var file = input[i];
		ocr_post_data.append("files",file,file.name);
	}
	
	return api_call(URL('OCR')+"?token="+token+"&name="+name,"POST",ocr_post_data,null,progress,function(result){
		if(result!=null){
			return callback($.parseJSON(result));
		 }else{
			 return callback(null);
		 }
	});
}

/*function OCR_GET(){
}*/

function FACE_DETECTION_POST(token,fileinputid,name,progress,callback){
	var input = $("#"+fileinputid).prop("files");
	var face_detection_post_data = new FormData();
	for(var i=0;i<input.length;++i){
		var file = input[i];
		face_detection_post_data.append("files",file,file.name);
	}
	
	return api_call(URL('FACE_DETECTION')+"?token="+token+"&name="+name,"POST",face_detection_post_data,null,progress,function(result){
		if(result!=null){
			return callback($.parseJSON(result));
		 }else{
			 return callback(null);
		 }
	});
}

/*function FACE_DETECTION_GET(){
}

function BAYES_SPAM_POST(){
}

function BAYES_SPAM_GET(){
}*/

function TRANSACTIONS_GET_ALL(){
}

function TRANSACTIONS_GET_SINGLE(){
}

function TRANSACTIONS_PUT(){
}

function RESULTS_GET(){
}

function CUSTOM_CALL(){
}