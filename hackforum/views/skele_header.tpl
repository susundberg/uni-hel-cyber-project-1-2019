<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">

		<title>PWWND FORUM</title>

		<link href="/static/min.css" rel="stylesheet" type="text/css">
	</head>
	<body>
		<nav class="nav" tabindex="-1" onclick="this.focus()">
			<div class="container">
				<a class="pagename current" href="/">PWWN FORUM</a>
				
				% if defined( "user" ):
				<a href="/logout">Logout</a>
				
				% if user["level"] >= 5:
				<a href="/admin">ADMIN</a>
				% end
				% end
			</div>
		</nav>

		
		
