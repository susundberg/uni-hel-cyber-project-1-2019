% include('skele_header.tpl')


  <div class="container">
  <form action="/admin" method="post">
    <h1>Create new user</h1>
    <b>Username</b>
    
    <input class="smooth" type="text" placeholder="Enter Username" name="username" required>
    
    <b>Password</b>
    <input class="smooth" type="text" placeholder="Enter Password" name="password" required>
     
    <b>Access level </b> 
     <input class="smooth" type="number" placeholder="0" name="level" required>
     
    <button class="btn btn-sm btn-b" type="submit">Create</button>
  </form>
  </div>
  
  
% include('skele_footer.tpl')

