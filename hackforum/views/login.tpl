% include('skele_header.tpl')


  <div class="container">
  <form action="/login" method="post">
    <h1>Hello there!</h1>
    <b>Username</b>
    
    <input class="smooth" type="text" placeholder="Enter Username" name="username" required>
    
    <b>Password</b>
    <input class="smooth" type="password" placeholder="Enter Password" name="password" required>
     
    <button class="btn btn-sm btn-b" type="submit">Login</button>
  </form>
  </div>
  
  
% include('skele_footer.tpl')
