var last_source = ''

function make_id()
{
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for( var i=0; i < 5; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
}

function generate_formatted_chat_message(data){

	if (data.message_id){
		var message_id = data.message_id;
	}else{
		var message_id = 0;
	}

	// console.log(data);
	if(data.type == 'text'){

		message_text = data.text;
		
		
		message_text = '<span class="message-text">' + message_text + '</span>'
		
		return message_text;
	}

	return "I don't know how to deal with " + JSON.stringify(data);

}


function add_message_to_chat(data, formatted_div){
	var chat = $('#messages-container');
	var new_source = data["source"];
	if (new_source == "BOT"){
		
	
		chat.append('<div class="msg-row"><div class="col-xs-11 col-sm-11 col-md-11 col-lg-11 no-sides-padding msg-animate"><div class="bot-icon-div">Bot:</div><div class="panel message-panel bot-msg "><div class="panel-body bot-msg-body"><div><div class="message-text">'+formatted_div+'</div></div></div></div></div></div>');
	}else if(new_source == "CANDIDATE"){

		var child = $('<div class="msg-row">');
		$(child).append('<div class="row"><div class="col-xs-10 col-sm-10 col-md-10 col-lg-10  pull-right no-sides-padding msg-animate"><div class="panel message-panel user-msg"><div class="panel-body user-msg-body"><div class="message-text"><span></span></div></div></div><div class="user-msg-bubble">you</div></div>');
		$(child).find('span').html(formatted_div);
		chat.append(child);
	}
}



function check_and_display(content_data, formatted_div){
	
	var data_source = content_data['source'];

	if(formatted_div){
		add_message_to_chat(content_data, formatted_div);
	
	}

	$("#body-container").scrollTop( $('#body-container')[0].scrollHeight);	
}



function sendTextMessage() {
    if ($('#messageToSend').text() == "") {
        return
    }

    // $('#button-container').empty();
    message = {}
    message.text = $('#messageToSend').html().replace("</div>", "").replace("<div>", "\n").replace("<br>", "\n");
    
    message.command= 'send'
    
    message.timestamp = new Date();
    
    $('#messageToSend').text('');

    $("#body-container").scrollTop( $('#body-container')[0].scrollHeight );
    
    
	chatsock.send(JSON.stringify(message));
	$("#message").val('').focus();
    
    return false;
    
}

function processAndDisplayChatMessage(message){

	var content_data = JSON.parse(message.data);
	
	var formatted_div = generate_formatted_chat_message(
		content_data);

	var display_dict = {
		'content_data':content_data,
		'formatted_div':formatted_div
	};
	
	check_and_display(content_data,formatted_div);
	
}
		