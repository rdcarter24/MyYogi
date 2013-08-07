function save(){
    $('#save_feedback').html('your profile has been update!');
    $('#save_feedback').fadeIn(500);
    $('#save_feedback').delay(2000);
    $('#save_feedback').fadeOut(500);
}





<!doctype html>
<html lang="en">
<head>
  
  <script src="http://code.jquery.com/jquery-1.9.1.js"></script>

</head>
<body>
  
<input type="button" value="Save" onclick="save();"/>
<!-- loop thru name_list in jquery and display each item using save function -->
<div id = "save_feedback"></div>
{% for item in name_list %}

<script>
function save(){
// // jquery for loop here

    $('#save_feedback').html("{{item}}");
    $('#save_feedback').fadeIn(500);
    $('#save_feedback').delay(2000);
    $('#save_feedback').fadeOut(500);

}
</script>
{% endfor %}
</body>
</html>