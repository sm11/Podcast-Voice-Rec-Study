function getParamFromURL( name )
 {
      name = name.replace(/[\[]/,"\\[").replace(/[\]]/,"\\]");
      var regexS = "[\?&]"+name+"=([^&#]*)";
      var regex = new RegExp( regexS );
      var results = regex.exec( window.location.href );
      if( results == null )
        return "";
      else
        return results[1];
}


var usernameFromParamString = getParamFromURL( 'workerId' );
var assignmentIdFromParamString = getParamFromURL( 'assignmentId' );
var hitIdFromParamString = getParamFromURL( 'hitId' );

//CREATE AND POST LINK TO REAL HIT
//var link = "${survey}" + "&workerId=" + usernameFromParamString + "&assignmentId=" + assignmentIdFromParamString + "&hitId=" + hitIdFromParamString; 
//$('#surv_link').attr('href', link);
var link = $('#surv_link').attr('href') + "?workerId=" + usernameFromParamString + "&assignmentId=" + assignmentIdFromParamString + "&hitId=" + hitIdFromParamString; 
$('#surv_link').attr('href', link);

//CREATE AND POST LINK TO REAL HIT
//var link = "http://127.0.0.1:5000?" + "workerId=" + usernameFromParamString + "&assignmentId=" + assignmentIdFromParamString + "&hitId=" + hitIdFromParamString; 
//$('#surv_link').attr('href', link);
//console.log($('#surv_link'))